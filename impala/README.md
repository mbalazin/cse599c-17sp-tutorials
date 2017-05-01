## Impala Tutorial

We will be using the following tools to facilitate our tutorials:
1. [Oracle VirtualBox](https://www.virtualbox.org/wiki/Downloads)
2. [Cloudera Quickstart VM](https://www.cloudera.com/downloads/quickstart_vms/5-10.html)
	

**Configuring the VM image setup**
1. Install Oracle VirtualBox
2. Unzip the VM image
3. Open VirtualBox and click on the New option
4. Give a name for the image, select "Linux" and appropirate version (64/32 bit). Click next
5. Select memory size as 4GB (4096 MB) (8GB recommended 8192MB). Click Next
6. Select the option "Use an existing virtual hard disk file". Here browse to the location where we have unziped the VM image. Select the image and click create.
7. Now you can see the image created in the left hand panel. Click on the cog wheel to change the network settings.
8. Go to the network tab and select the Bridged network
 ![Alt text](https://github.com/mbalazin/cse599c-17sp-tutorials/blob/master/impala/network_adapters.png "Network Adapters")

9. Boot the VM. The initial boot can take up to ~15 to 20 mins. It is recommended that you save the state of the machine. Saving the state of the machine saves time in case you want to reuse the VM later on.

 
###### Tweaks
- In case you want to increase your memory assignment

Before booting the VM, configure the image with the following settings:
 - Assign the memory atleast 4GB (8GB is highly recommended)
 ![Alt text](https://github.com/mbalazin/cse599c-17sp-tutorials/blob/master/impala/memory.jpg "Memory Setup")
 - In the network tab, change the Adapter 1 to Bridged Adapter
 ![Alt text](https://github.com/mbalazin/cse599c-17sp-tutorials/blob/master/impala/network_adapters.png "Network Adapters")
 

**Installing client environment on the host machine (Windows/Mac)**
We will be interacting with Impala databases(Cent OS) on our host machine(Windows /Mac). The Python library that needs to be installed on host machine(Windows/Mac) is **[Impyla](https://github.com/cloudera/impyla)** 

* Run the following command: 

```
pip install impyla
```
* To use the host machine completely as native sql queries run the following command:

```
pip install git+https://github.com/LucaCanali/ipython-sql.git
```

#### Tableau Demo

If you want to follow along the Tableau Demo on host (Windows/Mac) , please download the Tableau from the following link:
- [Tableau](https://itconnect.uw.edu/wares/uware/tableau-software/)

Download the [Tableau ODBC connector](https://www.cloudera.com/downloads/connectors/impala/odbc/2-5-36.html)

