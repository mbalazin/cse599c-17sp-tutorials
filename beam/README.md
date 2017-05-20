# Beam Installation Instructions:

## 1. Installing Beam 
- make sure you have python 2.7 

```
python --version 
```

- cd into the "beam" folder in the github directory
- run:

```
virtualenv env27
source env27/bin/activate
pip install -r requirements.txt
```

You should now be able to run:

```
python -m apache_beam.examples.wordcount --input env27/lib/python2.7/site-packages/pbr/tests/testpackage/MANIFEST.in --output counts
```

## 1. Creating a Google Cloud Account 
The majority of our demo will be done locally, but a small part shows how you can run on the cloud.  You can sign up for a year-long free trial, which gives you $300 in credit, but you do need to enter your credit card information.  If you don't want to do that, feel free to skip this step and just watch that part of the tutorial! 

- [Go to the google cloud homepage](https://cloud.google.com/)
- Select "TRY IT FREE" in the upper righthand corner 
- Agree to terms 
- Fill out information for your payments profile
    - Create an individual account 
    - Enter your name and address 
    - Enter your credit card (they swear they won't charge you!)
- Complete the profile 
