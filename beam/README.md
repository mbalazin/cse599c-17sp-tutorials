# Beam Installation Instructions:

## Creating a Google Cloud Account 
The majority of our demo will be done locally on the EC2 instances we set up, but a small part shows how you can run on the Google Cloud.  You can sign up for a year-long free trial, which gives you $300 in credit, but you do need to enter your credit card information.  If you don't want to do that, feel free to skip this step and just watch that part of the tutorial! 

### Here's how to sign up: 

- [Go to the Google Cloud homepage](https://cloud.google.com/)
- Select "TRY IT FREE" in the upper righthand corner 
- Agree to terms 
- Fill out information for your payments profile
    - Create an individual account 
    - Enter your name and address 
    - Enter your credit card (they swear they won't charge you!)
- Complete the profile 

### Create a Google Cloud Credentials File

Next, you'll need to generate a file that contains your service credentials for the Google Cloud API.  To do this, perform the following steps:

1. [Open the list of credentials](https://console.cloud.google.com/apis/credentials) in the Google Cloud Platform Console.
2. Click *Create credentials*.
3. Select *Service account key*.  A _Create service account key_ window will open.
4. Click the drop-down box below _Service account_, then click *New service account*.
5. Enter any name for the service account in *Name*, or use the default.
6. Use the default *Service account ID* or generate a different one.
7. Select *Project->Owner* for the role.
8. Select the key type: *JSON*.
9. Click *Create*.  A *Service account created* window is displayed and the private key file is downloaded automatically.
10. Remember where you saved this file, because you will need it on Wednesday!

### Enable Dataflow on your Google Cloud Service Account

1. Visit the [Dataflow API manager](https://console.developers.google.com/apis/api/dataflow.googleapis.com/overview).
2. Select a project from the dropdown near the top-left of the screen.  If you don't have a project, create a new one by clicking the *plus*.
3. Click *Enable* in the main window to enable Dataflow for this project.

## Disabling your account:
If you want to disable your account after the tutorial is over, follow the instructions [here](
https://support.google.com/cloud/answer/6288653?hl=en).