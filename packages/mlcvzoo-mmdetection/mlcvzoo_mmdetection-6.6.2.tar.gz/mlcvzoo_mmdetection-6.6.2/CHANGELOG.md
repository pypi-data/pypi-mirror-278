# MLCVZoo mlcvzoo_mmdetection module Versions:

6.6.2 (2024-06-11):
------------------
Fix package dependencies:
- Move tensorrt to optional dependencies
- State panopticapi dependency as extra without git to be pypi conformant

6.6.1 (2024-06-04):
------------------
Adapt python package management:
- Replace poetry by uv as dependency resolver and installer
- Replace poetry by the python native build package for building the python package
- Optimize dependency installation

6.6.0 (2024-04-30):
------------------
Integrate MMDeploy for TensorRT
- Add MMDetectionMMDeployTensorRTConfig class
- Extend MMDeployConverter class for converting models to TensorRT

6.5.1 (2024-02-07):
------------------
Update links in pyproject.toml and git link in README.md

6.5.0 (2024-02-06):
------------------
Integrate MMDeploy for ONNX Runtime
- Add MMDetectionMMDeployConfig class
- Add MMDetectionMMDeployOnnxruntimeConfig class
- Add runtime attribute to MMDetectionModel, MMObjectDetectionModel and MMSegmentationModel
- Add MMDeployConverter class for converting models using MMDeploy
- Add MMDeployInferencer class for prediction of deployed models
- Extend existing functions so that they take the runtime attribute into account and are backwards compatible

6.4.0 (2023-11-16):
------------------
Automatically set class-mapping config for nested datasets

6.3.0 (2023-09-25):
------------------
Add logging of a summary message that informs about
the number of Bounding-Boxes and Segmentations per class
in a MLCVZooMMDetDataset

6.2.0 (2023-08-21):
------------------
Allow to use bounding boxes of Segmentations for training Object Detection models:
- Add configuration option "include_segmentation_as_bbox" to MLCVZooMMDetDataset
- Fix backward compatibility for cfg-options usage

6.1.1 (2023-08-09):
------------------
Enhance mm configuration creation:
- Introduce the MMConfig class as central configuration attribute
- Add additional mm configuration option via a dictionary

6.0.1 (2023-07-25):
------------------
Fix MLCVZooMMDetDataset: Ensure correct parsing of annotations

6.0.0 (2023-05-10):
------------------
MMDetection 3 and relicense to OLFL-1.3 which succeeds the previous license

5.1.1 (2023-05-10):
------------------
Add the MMSegmentationModel model

5.0.1 (2023-05-03):
------------------
Python 3.10 compatibility

5.0.0 (2023-02-14):
------------------
Implement API changes introduces by mlcvzoo-base version 5.0.0
- Remove detector-config and use the feature of the single ModelConfiguration
- Remove duplicate attributes

4.0.2 (2022-10-17):
------------------
Fix bug in restore method: Ensure that the checkpoint is used which is passed to the method

4.0.1 (2022-09-09):
------------------
Ensure ConfigBuilder version 7 compatibility

4.0.0 (2022-08-08):
------------------
- Adapt to mlcvzoo-base 4.0.0
- Refactor and enhance mlcvzoo_mmdetection
  - The MMDetectionModel is now the base of all models of open-mmlab
  - Add MMObjectDetectionModel as dedicated model for object detection
  - Remove the CSVDataset and replace it with the MLCVZooMMDetDataset
  - Add latest commandline parameter for training mmdet models

3.0.1 (2022-07-11):
------------------
Prepare package for PyPi

3.0.0 (2022-05-16):
------------------
Use new features from AnnotationClassMapper that have been added with mlcvzoo_base v3.0.0

2.0.1 (2022-05-16)
------------------
Changed python executable for distributed training
- It can happen that the system python and python for running code are not the same. When starting distributed training, the system python was called.
- Now the python executable that runs the code is also executed when starting distributed (multi gpu) training.

2.0.0 (2022-04-05)
------------------
- initial release of the package
