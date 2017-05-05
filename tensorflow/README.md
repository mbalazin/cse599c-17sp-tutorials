# Tensorflow - Local installation, CPU-only

## 1. Getting Started
To follow along in class, you'll need to install Tensorflow locally at the very minimum. The full installation guide for Tensorflow is [here](https://www.tensorflow.org/install/).
For this installation guide, we're assuming you have pip and virtualenv installed already.

First create a virtual environment
```
$ virtualenv --system-site-packages <virtual_env_directory>
```
(We recommend picking this repository's tensorflow directory)

Activate the virtual environment
```
$ source ~/tensorflow/bin/activate # bash, sh, ksh, or zsh
$ source ~/tensorflow/bin/activate.csh  # csh or tcsh
```

Then run the following instructions to install Tensorflow:
```
(tensorflow)$ pip install --upgrade tensorflow # for Python 2.7
(tensorflow)$ pip3 install --upgrade tensorflow # for Python 3.n
```
If that didn't work, try
```
(tensorflow)$ pip install --upgrade TF_PYTHON_URL   # Python 2.7
(tensorflow)$ pip3 install --upgrade TF_PYTHON_URL  # Python 3.N 
```
where you have to look up the appropriate TF_PYTHON_URL for your system:
[Linux](https://www.tensorflow.org/install/install_linux#the_url_of_the_tensorflow_python_package)
,
[MacOS](https://www.tensorflow.org/install/install_mac#the_url_of_the_tensorflow_python_package)

