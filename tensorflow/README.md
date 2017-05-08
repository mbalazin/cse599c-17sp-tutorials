# Tensorflow Installation instructions

## 1. Local installation, CPU-only
To follow along in class, you'll need to install Tensorflow locally at the very minimum. The full installation guide for Tensorflow is [here](https://www.tensorflow.org/install/).
For this installation guide, we're assuming you have pip installed already.

Then run the following instructions to install Tensorflow:
```
$ pip install --upgrade tensorflow # for Python 2.7
$ pip3 install --upgrade tensorflow # for Python 3.n
```
If that didn't work, try
```
$ pip install --upgrade TF_PYTHON_URL   # Python 2.7
$ pip3 install --upgrade TF_PYTHON_URL  # Python 3.N 
```
where you have to look up the appropriate TF_PYTHON_URL for your system:
[Linux](https://www.tensorflow.org/install/install_linux#the_url_of_the_tensorflow_python_package)
,
[MacOS](https://www.tensorflow.org/install/install_mac#the_url_of_the_tensorflow_python_package)

## 2. Running Tensorflow on AWS
The other option is to run Tensorflow on AWS. You will need to sign up for AWS Free Tier [here](https://aws.amazon.com/free/).

To run Tensorflow in an EC2 instance, the easiest way is to launch a Deep Learning AMI on a micro instance [here](https://aws.amazon.com/marketplace/pp/B06VSPXKDX?qid=1494286814487&sr=0-2&ref_=srh_res_product_title).
Use the one-click launch with the defaults, but make sure you choose the t2.micro instance type. If you do not have a key-pair, you will need to create one in your AWS management console. Make sure to save the key file. Launch the instance.

Modify the permissions on the key file:
```
chmod 400 /path/my-key-pair.pem
```

After you launch the instance, go into your management console and wait until your instance is ready. When it is, ssh into the machine by specifying your private key and user_name@public_dns_name.
For example:
```
ssh -L localhost:8888:localhost:8888 -i /path/my-key-pair.pem ubuntu@ec2-198-51-100-1.compute-1.amazonaws.com
```

Once you log into your instance, you should be able to run tensorflow!

If you would like to run a Jupyter notebook on this EC2 instance, follow the instructions [here](https://aws.amazon.com/blogs/ai/the-aws-deep-learning-ami-now-with-ubuntu/).

Open Jupyter using the command:
```
jupyter notebook
```

Wait until you are given a URL to connect to this notebook. Navigate to the URL on your browser.


# Running Tensorflow

## 3. Distributed training
Training with distributed Tensorflow has a dispatcher-worker architecture. We give an example to train the MNIST digit recognition model on EC2. 

First, create a security policy that exposes TCP port 2222. Create 3 EC2 instances with the provided image and the security policy. 

Then, after the instances are assigned, modify the hardcoded IP addresses in dist-tf.py. 

Execute the following command on each EC2 instance:

```
(EC2-instance1)$ python example.py --job_name="ps" --task_index=0 
(EC2-instance2)$ python example.py --job_name="worker" --task_index=0 
(EC2-instance3)$ python example.py --job_name="worker" --task_index=1 
```

The first EC2 instance serves as the job dispatcher and parameter server, and the next two EC2 instances run as workers. 

# 4. Compare Tensorflow to Spark

We compare Tensorflow with Spark by applying multilayer perceptron (MLP) with two hidden layers on MNIST handwritten digit dataset ([MNIST](http://yann.lecun.com/exdb/mnist/)). This session uses Jupyter Notebook and requires local installation of Tensorflow and Spark. 

First, navigate to this directory of the cloned repository and open a Jupyter Notebook:
```
jupyter notebook
```
In your browser, open ``tensorflow_mlp_mnist_notebook.ipynb'', run the cells in it and get the training time and accuracy.

In your browser, open ``spark_mlp_mnist_notebook.ipynb'', in the cell of ``Spark'', change the memory and master address according to your machine setting.
```
#set memory to 3/4 memory of your machine
conf.set("spark.executor.memory", "12g")
```
```
master="spark://Administrators-MacBook-Pro.local:7077"
```

Start spark by running script provided in Spark directory, for example,
```
./sbin/start-all.sh
```

Then run the cells in it and get the training time and accuracy.
