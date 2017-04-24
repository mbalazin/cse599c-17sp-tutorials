## Impala Tutorial

We will be using the following tools to facilitate our tutorials:
1. [Oracle VirtualBox](https://www.virtualbox.org/wiki/Downloads)
2. [Cloudera Quickstart VM](https://www.cloudera.com/downloads/quickstart_vms/5-10.html)
3. [Tableau](https://itconnect.uw.edu/wares/uware/tableau-software/)
	

**Configuring the VM image setup**
1. Install Oracle VirtualBox
2. Unzip the VM image
3. Before booting the VM, configure the VM with the following settings:
 - Assign the memory atleast 4GB (8GB is highly recommended)
 - In the network tab, change the Adapter 1 to Bridged Adapter
4. Boot the VM. The initial boot can take up to ~15 to 20 mins. It is recommended that you save the state of the machine. Saving the state of the machine saves time in case you want to reuse the VM later on.

**Installing client environment on the host machine**
We will be interacting with Impala databases on our host machine. The Python library that needs to be installed is **[Impyla](https://github.com/cloudera/impyla)** 

* Run the following command: 

```
pip install impyla
```
* To use the host machine completely as native sql queries run the following command:

```
pip install git+https://github.com/LucaCanali/ipython-sql.git
```




