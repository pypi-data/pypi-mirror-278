# Copyright Open Logistics Foundation
#
# Licensed under the Open Logistics Foundation License 1.3.
# For details on the licensing terms, see the LICENSE file.
# SPDX-License-Identifier: OLFL-1.3

"""Wrapper to convert MMDetection models using MMDeploy."""

import copy
import os
import shutil
from typing import List, cast

from mmdeploy.apis import torch2onnx
from mmdeploy.apis.utils import to_backend
from mmdeploy.backend.sdk.export_info import export2SDK
from mmdeploy.utils import get_backend, get_ir_config
from mmengine.config import Config

from mlcvzoo_mmdetection.configuration import (
    MMDetectionMMDeployConfig,
    MMDetectionMMDeployOnnxruntimeConfig,
)
from mlcvzoo_mmdetection.mlcvzoo_mmdeploy.structs import MMDeployBackendType
from mlcvzoo_mmdetection.utils import init_mm_config


class MMDeployConverter:  # pylint: disable=too-few-public-methods
    """Converter for MMDetection models using MMDeploy."""

    def __init__(
        self,
        model_config: Config,
        checkpoint_path: str,
        mmdeploy_config: MMDetectionMMDeployConfig,
    ) -> None:
        self.model_config = model_config
        self.checkpoint_path = checkpoint_path
        self.mmdeploy_config = mmdeploy_config
        self.mmdeploy_cfg: Config = init_mm_config(mm_config=mmdeploy_config)

    def run(self) -> None:
        """Run a deployment.

        Raises:
            KeyError: If configuration key 'backend_config' or 'backend_config.type' is missing in
                the MMDeploy configuration.
            NotImplementedError: If the value for key 'backend_config.type' in the MMDeploy
                configuration is not supported.

        Returns:
            None
        """

        try:
            backend_type = self.mmdeploy_cfg["backend_config"]["type"]
        except KeyError as exc:
            raise KeyError(
                "Invalid MMDeploy configuration. Key 'backend_config.type' is not specified."
            ) from exc

        if backend_type == MMDeployBackendType.ONNXRUNTIME:
            return self.__deploy_onnxruntime()

        if backend_type == MMDeployBackendType.TENSORRT:
            return self.__deploy_tensorrt()

        raise NotImplementedError(
            f"Invalid MMDeploy configuration. The backend type '{backend_type}' is not supported."
        )

    def __deploy_onnxruntime(self) -> None:
        """Run a deployment for backend type onnxruntime.

        Raises:
            ValueError: If the value for 'device_string' in the MMDeploy configuration is not
                'cpu'.
        """

        # Narrow type
        mmdeploy_config = cast(
            MMDetectionMMDeployOnnxruntimeConfig, self.mmdeploy_config
        )

        if self.mmdeploy_config.device_string != "cpu":
            raise ValueError("Backend onnxruntime is only supported on CPU.")

        checkpoint_paths = self.__deploy_common()

        # For the onnxruntime backend only one is file generated
        # Move generated end2end.onnx to the correct location
        shutil.move(src=checkpoint_paths[0], dst=mmdeploy_config.checkpoint_path)

    def __deploy_tensorrt(self) -> None:
        """Run a deployment for backend type tensorrt.

        Raises:
            ValueError: If the value for 'device_string' in the MMDeploy configuration does not
                start with 'cuda'.
        """

        # Narrow type
        mmdeploy_config = cast(
            MMDetectionMMDeployOnnxruntimeConfig, self.mmdeploy_config
        )

        if not self.mmdeploy_config.device_string.startswith("cuda"):
            raise ValueError("Backend tensorrt is only supported on GPU.")

        checkpoint_paths = self.__deploy_common()

        # For the tensorrt backend only one file is generated
        # Move generated end2end.engine to the correct location
        shutil.move(src=checkpoint_paths[0], dst=mmdeploy_config.checkpoint_path)

    def __deploy_common(self) -> List[str]:
        """Run common steps for a MMdeploy deployment.

        Returns:
            List[str]: A list of generated backend specific model filepaths.
        """

        if self.mmdeploy_config.dump_info:
            export2SDK(
                deploy_cfg=self.mmdeploy_cfg,
                # Use a deep copy to prevent changes in the model config
                model_cfg=copy.deepcopy(self.model_config),
                work_dir=self.mmdeploy_config.work_dir,
                pth=self.checkpoint_path,
                device=self.mmdeploy_config.device_string,
            )

        # Convert to IR
        ir_config = get_ir_config(self.mmdeploy_cfg)
        ir_save_file = ir_config["save_file"]

        torch2onnx(
            img=self.mmdeploy_config.test_image_path,
            work_dir=self.mmdeploy_config.work_dir,
            save_file=ir_save_file,
            deploy_cfg=self.mmdeploy_cfg,
            model_cfg=self.model_config,
            model_checkpoint=self.checkpoint_path,
            device=self.mmdeploy_config.device_string,
        )

        # Convert to backend
        backend = get_backend(self.mmdeploy_cfg)

        # MMdeploy always returns a list of backend files
        checkpoint_paths: List[str] = to_backend(
            backend_name=backend,
            ir_files=[os.path.join(self.mmdeploy_config.work_dir, ir_save_file)],
            work_dir=self.mmdeploy_config.work_dir,
            deploy_cfg=self.mmdeploy_cfg,
            device=self.mmdeploy_config.device_string,
        )

        return checkpoint_paths
