# Copyright Open Logistics Foundation
#
# Licensed under the Open Logistics Foundation License 1.3.
# For details on the licensing terms, see the LICENSE file.
# SPDX-License-Identifier: OLFL-1.3

"""Module for defining MMDeploy related structs."""

from enum import Enum


class MMDeployBackendType(str, Enum):
    """Defines backend types used in MMDeploy."""

    ONNXRUNTIME = "onnxruntime"
    TENSORRT = "tensorrt"
