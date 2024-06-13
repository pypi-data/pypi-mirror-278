# MLCVZoo MMDetection

The MLCVZoo is an SDK for simplifying the usage of various (machine learning driven)
computer vision algorithms. The package **mlcvzoo_mmdetection** is the wrapper module for
the [mmdetection framework](https://github.com/open-mmlab/mmdetection).

## Install

NOTE: For some panoptic segmentation models of mmdetection you need to have the panopticapi installed.
      How this is handled in mlcvzoo-mmdetection is listed below. Otherwise you will get an ImportError.

### Install for developer

#### Clone repository

```bash
cd YOUR_PATH
git clone git@git.openlogisticsfoundation.org:silicon-economy/base/ml-toolbox/mlcvzoo-models/mlcvzoo-mmdetection.git
cd mlcvzoo-mmdetection
```

#### Create and install python environment
```bash
virtualenv .venv
source .venv/bin/activate

# Install dependencies with all extras (including panopticapi)
source build.sh
```

For VSCode IDE add the relevant environment variables in .venv/bin/activate.

```bash
export PYTHONPATH=PARENT_OF_YOUR_REPOSITORY
# The MMDETECTION_DIR is needed in our unit tests for defining the
# path to the configuration files of mmdetection. Since mmdet v2.15.0
# the configuration are stored in the mmdet/.mim/ folder of the installed
# mmdet package in your python environment. For older versions a specific checkout
# is needed.
export MMDETECTION_DIR="$VIRTUAL_ENV/lib/python3.10/site-packages/mmdet/.mim/"
```

## Install for package users

The following command installs the mlcvzoo-mmdetection package, however we
recommend to have a look at the ./build.sh script. It is gathering all fixes
that are needed to setup a running python environment.

```bash
pip install mlcvzoo-mmdetection
```

NOTE: In order to use panoptic segmentations you have to install the following, as specified by mmdetection:

```bash
pip install panopticapi @ git+https://github.com/cocodataset/panopticapi.git@7bb4655548f98f3fedc07bf37e9040a992b054b0
```

# Further documentation
[comment]: <> (TODO: Fix links to main branch)
- [Ar42 Documentation](https://git.openlogisticsfoundation.org/silicon-economy/base/ml-toolbox/mlcvzoo-models/mlcvzoo-mmdetection/-/blob/main/documentation/index.adoc)
- [Installation guide](https://git.openlogisticsfoundation.org/silicon-economy/base/ml-toolbox/mlcvzoo-models/mlcvzoo-mmdetection/-/blob/main/documentation/12_tutorial.adoc#user-content-setup-the-mlcvzoo-models)
- [Configuration Usage](https://git.openlogisticsfoundation.org/silicon-economy/base/ml-toolbox/mlcvzoo-models/mlcvzoo-mmdetection/-/blob/main/documentation/12_tutorial.adoc#user-content-configure-mmdetection)


## Technology stack

- Python
