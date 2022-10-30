# ai-vms
## Introduction
VMS system with ability to process analytics and GUI. Software could be used to display up to 4 CCTV cameras and to process basic face/people detection and advanced face/people detection.

## Installing

>!git clone https://github.com/Viva-Fidel/ai-vms.git

Additionally install CUDA if you want to use GPU for processing

## Requirements

PySide6~=6.3.2  
opencv-python~=4.6.0.66  
mediapipe~=0.8.11  
numpy~=1.23.2  

>!pip install -r requirements.txt

## Usage

#### Adding CCTV camera
To add CCTV camera open menu and choose "Add camera"
<p></p>
<img src="https://user-images.githubusercontent.com/98227548/198890012-bcb5b188-84a2-4cc2-8667-1a995d72d550.png" height="240" width="426">
<p></p>
Add RTSP link
<img src="https://user-images.githubusercontent.com/98227548/198890243-1ca46631-1e02-4eaa-901d-ad4d18a2bb21.png" height="240" width="426">

#### Deleting CCTV camera
To delete camera, open menu and choose "Delete camera". The last added camera would be deleted
<p></p>
<img src="https://user-images.githubusercontent.com/98227548/198890134-8c06b54d-ddbf-4526-91d9-cd2432f62aae.png" height="240" width="426">

#### Using analytics
To switch on analytics, right click on a camera where the analytcis would be used. Choose the analytics that you need. To wsitch off, choose "None"
<p></p>
<img src="https://user-images.githubusercontent.com/98227548/198890291-c47ed46c-5358-4428-a5e5-6d0e88e3e112.png" height="240" width="426">

#### Additional features
* The software saves configuration and RTSP links. Every new start, it will upload the las saved configuration
* The application saves last window position
* Double click on camera will switch on or off full screen option of that camera and hide others cameras






