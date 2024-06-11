# Copyright (C) 2022 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions
# and limitations under the License.
import datetime
import json
import logging
import os
import shutil
from typing import Any, Dict, List, Optional, Union

import attr
import numpy as np
from model_api.models import Model as OMZModel

from geti_sdk.data_models import (
    Annotation,
    Label,
    Prediction,
    Project,
    ScoredLabel,
    Task,
    TaskType,
)
from geti_sdk.data_models.shapes import Rectangle
from geti_sdk.deployment.data_models import ROI, IntermediateInferenceResult
from geti_sdk.rest_converters import ProjectRESTConverter

from .deployed_model import DeployedModel
from .inference_hook_interfaces import PostInferenceHookInterface
from .utils import OVMS_README_PATH, generate_ovms_model_name


@attr.define(slots=False)
class Deployment:
    """
    Representation of a deployed Intel® Geti™ project that can be used to run
    inference locally
    """

    project: Project
    models: List[DeployedModel]

    def __attrs_post_init__(self):
        """
        Initialize private attributes.
        """
        self._is_single_task: bool = len(self.project.get_trainable_tasks()) == 1
        self._are_models_loaded: bool = False
        self._inference_converters: Dict[str, Any] = {}
        self._path_to_temp_resources: Optional[str] = None
        self._requires_resource_cleanup: bool = False
        self._post_inference_hooks: List[PostInferenceHookInterface] = []
        self._empty_label: Optional[Label] = None

    @property
    def is_single_task(self) -> bool:
        """
        Return True if the deployment represents a project with only a single task.

        :return: True if the deployed project contains only one trainable task, False
            if it is a pipeline project
        """
        return self._is_single_task

    @property
    def are_models_loaded(self) -> bool:
        """
        Return True if all inference models for the Deployment are loaded and ready
        to infer.

        :return: True if all inference models for the deployed project are loaded in
            memory and ready for inference
        """
        return self._are_models_loaded

    def save(self, path_to_folder: Union[str, os.PathLike]) -> bool:
        """
        Save the Deployment instance to a folder on local disk.

        :param path_to_folder: Folder to save the deployment to
        :return: True if the deployment was saved successfully, False otherwise
        """
        project_dict = ProjectRESTConverter.to_dict(self.project)
        deployment_folder = os.path.join(path_to_folder, "deployment")

        os.makedirs(deployment_folder, exist_ok=True, mode=0o770)

        # Save model for each task
        for task, model in zip(self.project.get_trainable_tasks(), self.models):
            model_dir = os.path.join(deployment_folder, task.title)
            os.makedirs(model_dir, exist_ok=True, mode=0o770)
            success = model.save(model_dir)
            if not success:
                logging.exception(
                    f"Saving model '{model.name}' failed. Unable to save deployment."
                )
                return False

        # Save project data
        project_filepath = os.path.join(deployment_folder, "project.json")
        with open(project_filepath, "w") as project_file:
            json.dump(project_dict, project_file, indent=4)

        # Save post inference hooks, if any
        if self.post_inference_hooks:
            hook_config_file = os.path.join(deployment_folder, "hook_config.json")
            hook_configs: List[Dict[str, Any]] = []
            for hook in self.post_inference_hooks:
                hook_configs.append(hook.to_dict())
            with open(hook_config_file, "w") as file:
                json.dump({"post_inference_hooks": hook_configs}, file)

        # Clean up temp resources if needed
        if self._requires_resource_cleanup:
            self._remove_temporary_resources()
            self._requires_resource_cleanup = False

        return True

    @classmethod
    def from_folder(cls, path_to_folder: Union[str, os.PathLike]) -> "Deployment":
        """
        Create a Deployment instance from a specified `path_to_folder`.

        :param path_to_folder: Path to the folder containing the Deployment data
        :return: Deployment instance corresponding to the deployment data in the folder
        """
        deployment_folder = path_to_folder
        if not isinstance(path_to_folder, str):
            path_to_folder = str(path_to_folder)
        if not path_to_folder.endswith("deployment"):
            if "deployment" in os.listdir(path_to_folder):
                deployment_folder = os.path.join(path_to_folder, "deployment")
            else:
                raise ValueError(
                    f"No `deployment` folder found in the directory at "
                    f"`{path_to_folder}`. Unable to load Deployment."
                )
        project_filepath = os.path.join(deployment_folder, "project.json")
        with open(project_filepath, "r") as project_file:
            project_dict = json.load(project_file)
        project = ProjectRESTConverter.from_dict(project_dict)
        task_folder_names = [task.title for task in project.get_trainable_tasks()]
        models: List[DeployedModel] = []
        for task_folder in task_folder_names:
            models.append(
                DeployedModel.from_folder(os.path.join(deployment_folder, task_folder))
            )
        deployment = cls(models=models, project=project)

        # Load post inference hooks, if any
        hook_config_file = os.path.join(deployment_folder, "hook_config.json")
        if os.path.isfile(hook_config_file):
            available_hooks = {
                subcls.__name__: subcls
                for subcls in PostInferenceHookInterface.__subclasses__()
            }
            with open(hook_config_file, "r") as file:
                hook_dict = json.load(file)
            for hook_data in hook_dict["post_inference_hooks"]:
                for hook_name, hook_args in hook_data.items():
                    target_hook = available_hooks[hook_name]
                    hook = target_hook.from_dict(hook_args)
                deployment.add_post_inference_hook(hook)
        return deployment

    def load_inference_models(self, device: str = "CPU"):
        """
        Load the inference models for the deployment to the specified device.

        Note: For a list of devices that are supported for OpenVINO inference, please see:
        https://docs.openvino.ai/latest/openvino_docs_OV_UG_supported_plugins_Supported_Devices.html

        :param device: Device to load the inference models to (e.g. 'CPU', 'GPU', 'AUTO', etc)
        """
        for model in self.models:
            model.load_inference_model(device=device, project=self.project)

        # Extract empty label for the upstream task
        upstream_labels = self.models[0].label_schema.get_labels(include_empty=True)
        self._empty_label = next(
            (label for label in upstream_labels if label.is_empty), None
        )

        self._are_models_loaded = True
        logging.info(f"Inference models loaded on device `{device}` successfully.")

    def infer(self, image: np.ndarray, name: Optional[str] = None) -> Prediction:
        """
        Run inference on an image for the full model chain in the deployment.

        :param image: Image to run inference on, as a numpy array containing the pixel
            data. The image is expected to have dimensions [height x width x channels],
            with the channels in RGB order
        :param name: Optional name for the image, if specified this will be used in
            any post inference hooks belonging to the deployment.
        :return: inference results
        """
        self._check_models_loaded()

        # Single task inference
        if self.is_single_task:
            prediction = self._infer_task(
                image, task=self.project.get_trainable_tasks()[0], explain=False
            )
        # Multi-task inference
        else:
            prediction = self._infer_pipeline(image=image, explain=False)

        # Empty label is not generated by prediction postprocessing correctly, append
        # it here if there are no other predictions
        height, width = image.shape[0:2]
        if len(prediction.annotations) == 0:
            if self._empty_label is not None:
                prediction.append(
                    Annotation(
                        shape=Rectangle(x=0, y=0, width=width, height=height),
                        labels=[
                            ScoredLabel.from_label(self._empty_label, probability=1)
                        ],
                    )
                )
        self._execute_post_inference_hooks(
            image=image, prediction=prediction, name=name
        )
        return prediction

    def explain(self, image: np.ndarray, name: Optional[str] = None) -> Prediction:
        """
        Run inference on an image for the full model chain in the deployment. The
        resulting prediction will also contain saliency maps and the feature vector
        for the input image.

        :param image: Image to run inference on, as a numpy array containing the pixel
            data. The image is expected to have dimensions [height x width x channels],
            with the channels in RGB order
        :param name: Optional name for the image, if specified this will be used in
            any post inference hooks belonging to the deployment.
        :return: inference results
        """
        self._check_models_loaded()

        # Single task inference
        if self.is_single_task:
            prediction = self._infer_task(
                image, task=self.project.get_trainable_tasks()[0], explain=True
            )
        # Multi-task inference
        else:
            prediction = self._infer_pipeline(image=image, explain=True)
        self._execute_post_inference_hooks(
            image=image, prediction=prediction, name=name
        )
        return prediction

    def _check_models_loaded(self) -> None:
        """
        Check if models are loaded and ready for inference.

        :raises: ValueError in case models are not loaded
        """
        if not self.are_models_loaded:
            raise ValueError(
                f"Deployment '{self}' is not ready to infer, the inference models are "
                f"not loaded. Please call 'load_inference_models' first."
            )

    def _infer_task(
        self, image: np.ndarray, task: Task, explain: bool = False
    ) -> Prediction:
        """
        Run pre-processing, inference, and post-processing on the input `image`, for
        the model associated with the `task`.

        :param image: Image to run inference on
        :param task: Task to run inference for
        :param explain: True to get additional outputs for model explainability,
            including saliency maps and the feature vector for the image
        :return: Inference result
        """
        model = self._get_model_for_task(task)
        return model.infer(image, explain)

    def _infer_pipeline(self, image: np.ndarray, explain: bool = False) -> Prediction:
        """
        Run pre-processing, inference, and post-processing on the input `image`, for
        all models in the task chain associated with the deployment.

        Note: If `explain=True`, a saliency map, feature vector and active score for
        the first task in the pipeline will be included in the prediction output

        :param image: Image to run inference on
        :param explain: True to get additional outputs for model explainability,
            including saliency maps and the feature vector for the image
        :return: Inference result
        """
        previous_labels: Optional[List[Label]] = None
        intermediate_result: Optional[IntermediateInferenceResult] = None
        rois: Optional[List[ROI]] = None
        image_views: Optional[List[np.ndarray]] = None

        # Pipeline inference
        for task in self.project.pipeline.tasks[1:]:
            # First task in the pipeline generates the initial result and ROIs
            if task.is_trainable and previous_labels is None:
                task_prediction = self._infer_task(image, task=task, explain=explain)
                rois: Optional[List[ROI]] = None
                if not task.is_global:
                    rois = [
                        ROI.from_annotation(annotation)
                        for annotation in task_prediction.annotations
                    ]
                intermediate_result = IntermediateInferenceResult(
                    image=image, prediction=task_prediction, rois=rois
                )
                previous_labels = [label for label in task.labels if not label.is_empty]

            # Downstream trainable tasks
            elif task.is_trainable:
                if rois is None or image_views is None or intermediate_result is None:
                    raise NotImplementedError(
                        "Unable to run inference for the pipeline in the deployed "
                        "project: A flow control task is required between each "
                        "trainable task in the pipeline."
                    )
                new_rois: List[ROI] = []
                for roi, view in zip(rois, image_views):
                    view_prediction = self._infer_task(view, task)
                    if task.is_global:
                        # Global tasks add their labels to the existing shape in the ROI
                        intermediate_result.extend_annotations(
                            view_prediction.annotations, roi=roi
                        )
                    else:
                        # Local tasks create new shapes in the image coordinate system,
                        # and generate ROI's corresponding to the new shapes
                        for annotation in view_prediction.annotations:
                            intermediate_result.append_annotation(annotation, roi=roi)
                            new_rois.append(ROI.from_annotation(annotation))
                        intermediate_result.rois = [
                            new_roi.to_absolute_coordinates(parent_roi=roi)
                            for new_roi in new_rois
                        ]
                previous_labels = [label for label in task.labels if not label.is_empty]

            # Downstream flow control tasks
            else:
                if previous_labels is None:
                    raise NotImplementedError(
                        f"Unable to run inference for the pipeline in the deployed "
                        f"project: First task in the pipeline after the DATASET task "
                        f"has to be a trainable task, found task of type {task.type} "
                        f"instead."
                    )
                # CROP task
                if task.type == TaskType.CROP:
                    rois = intermediate_result.filter_rois(label=None)
                    image_views = intermediate_result.generate_views(rois)
                else:
                    raise NotImplementedError(
                        f"Unable to run inference for the pipeline in the deployed "
                        f"project: Unsupported task type {task.type} found."
                    )
        return intermediate_result.prediction

    def _get_model_for_task(self, task: Task) -> DeployedModel:
        """
        Get the DeployedModel instance corresponding to the input `task`.

        :param task: Task to get the model for
        :return: DeployedModel corresponding to the task
        """
        try:
            task_index = self.project.get_trainable_tasks().index(task)
        except ValueError as error:
            raise ValueError(
                f"Task {task.title} is not in the list of trainable tasks for project "
                f"{self.project.name}."
            ) from error
        return self.models[task_index]

    def _remove_temporary_resources(self) -> bool:
        """
        If necessary, clean up any temporary resources associated with the deployment.

        :return: True if temp files have been deleted successfully
        """
        if self._path_to_temp_resources is not None and os.path.isdir(
            self._path_to_temp_resources
        ):
            try:
                shutil.rmtree(self._path_to_temp_resources)
            except PermissionError:
                logging.warning(
                    f"Unable to remove temporary files for deployment at path "
                    f"`{self._path_to_temp_resources}` because the files are in "
                    f"use by another process. "
                )
                return False
        else:
            logging.debug(
                f"Unable to clean up temporary resources for deployment {self}, "
                f"because the resources were not found on the system. Possibly "
                f"they were already deleted."
            )
            return False
        return True

    def __del__(self):
        """
        If necessary, clean up any temporary resources associated with the deployment.
        This method is called when the Deployment instance is deleted.
        """
        if self._requires_resource_cleanup:
            self._remove_temporary_resources()

    def generate_ovms_config(self, output_folder: Union[str, os.PathLike]) -> None:
        """
        Generate the configuration files needed to push the models for the
        `Deployment` instance to OVMS.

        :param output_folder: Target folder to save the configuration files to
        """
        # First prepare the model config list
        if os.path.basename(output_folder) != "ovms_models":
            ovms_models_dir = os.path.join(output_folder, "ovms_models")
        else:
            ovms_models_dir = output_folder
            output_folder = os.path.dirname(ovms_models_dir)
        os.makedirs(ovms_models_dir, exist_ok=True)

        model_configs: List[Dict[str, Dict[str, Any]]] = []
        for model in self.models:
            # Create configuration entry for model
            model_name = generate_ovms_model_name(
                project=self.project, model=model, omit_version=True
            )
            config = {
                "name": model_name,
                "base_path": f"/models/{model_name}",
                "plugin_config": {"PERFORMANCE_HINT": "LATENCY"},
            }
            model_configs.append({"config": config})

            # Copy IR model files to the expected OVMS format
            if model.version is not None:
                model_version = str(model.version)
            else:
                # Fallback to version 1 if no version info is available
                model_version = "1"

            ovms_model_dir = os.path.join(ovms_models_dir, model_name, model_version)

            # Load the model to embed preprocessing for inference with OVMS adapter
            embedded_model = OMZModel.create_model(
                model=os.path.join(model.model_data_path, "model.xml")
            )
            embedded_model.save(
                xml_path=os.path.join(ovms_model_dir, "model.xml"),
                bin_path=os.path.join(ovms_model_dir, "model.bin"),
            )
            logging.info(f"Model `{model.name}` prepared for OVMS inference.")

        # Save model configurations
        ovms_config_list = {"model_config_list": model_configs}
        config_target_filepath = os.path.join(ovms_models_dir, "ovms_model_config.json")
        with open(config_target_filepath, "w") as file:
            json.dump(ovms_config_list, file)

        # Copy resource files
        shutil.copy2(OVMS_README_PATH, os.path.join(output_folder))

        logging.info(
            f"Configuration files for OVMS model deployment have been generated in "
            f"directory '{output_folder}'. This folder contains a `OVMS_README.md` "
            f"file with instructions on how to launch OVMS, connect to it and run "
            f"inference. Please follow the instructions outlined there to get started."
        )

    @property
    def post_inference_hooks(self) -> List[PostInferenceHookInterface]:
        """
        Return the currently active post inference hooks for the deployment

        :return: list of PostInferenceHook objects
        """
        return self._post_inference_hooks

    def clear_inference_hooks(self) -> None:
        """
        Remove all post inference hooks for the deployment
        """
        n_hooks = len(self.post_inference_hooks)
        self._post_inference_hooks = []
        if n_hooks != 0:
            logging.info(
                f"Post inference hooks cleared. {n_hooks} hooks were removed "
                f"successfully"
            )

    def add_post_inference_hook(self, hook: PostInferenceHookInterface) -> None:
        """
        Add a post inference hook, which will be executed after each call to
        `Deployment.infer`

        :param hook: PostInferenceHook to be added to the deployment
        """
        self._post_inference_hooks.append(hook)
        logging.info(f"Hook `{hook}` added.")
        logging.info(
            f"Deployment now contains {len(self.post_inference_hooks)} "
            f"post inference hooks."
        )

    def _execute_post_inference_hooks(
        self, image: np.ndarray, prediction: Prediction, name: Optional[str] = None
    ) -> None:
        """
        Execute all post inference hooks

        :param image: Numpy image which was inferred
        :param prediction: Prediction for the image
        :param name: Optional name for the image
        """
        timestamp = datetime.datetime.now()
        for hook in self._post_inference_hooks:
            hook.run(image, prediction, name, timestamp)
