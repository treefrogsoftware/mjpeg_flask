# Mjpeg simple flask web server demo

## Python Flask example using a raspberry pi camera to generate mjpeg over http

Use standard installations for pip3 to install the python packages

## Pi/Ubuntu and pip installs
```bash
sudo apt-get install python3
sudo apt-get install python3-pip
sudo pip3 install flask
sudo pip3 install picamera # only on pi
sudo apt install python3-opencv # on ubuntu and possibly the pi using a usb camera
```
## Non Pi or Ubuntu solution

To use the code on another platform/os other than PI or Ubuntu you will need to create \<name\>MjpegCamera in the mjpegcamera package or it will just show you an image of a swimming pool from the default implementation.  The CV2MjpegCamera should work on any linux installs so to differentiate you would have to tweak the logic in the header for your OS.
```python
if "Ubuntu" in platform._syscmd_uname('-a'):
```
These modules inherit the abstract class MjpegCamera (Python 3 required) - once created you will also need to add
the module to the package by adding into the mjpegcamera/\_\_init\_\_.py file

```python
__all__ = [
        'PiMjpegCamera',
        'CV2MjpegCamera', # added and tested on ubuntu
        'MjpegCamera' # abstract class in package used to expand for platforms
        ]
```
The MjpegCamera is an abstract class which has three methods that will need to be implemented - start, stop and get_frame

```python
class PiMjpegCamera(MjpegCamera):
.
.
def start(self):
    PiMjpegCamera.camera.start_recording(PiMjpegCamera.output, format='mjpeg')
    return "started"

def stop(self):
    PiMjpegCamera.camera.stop_recording()
    return "stopped"

def get_frame(self):
    self.initialize()
    with PiMjpegCamera.output.condition:
        PiMjpegCamera.output.condition.wait()
        return PiMjpegCamera.output.frame

```
To use your python camera source there are two ways to initialise your camera, the first one is ByName so request the Class that you have created \<Name\>MjpegCamera or if you're running with a Pi Camera specify PiMjpegCamera.

```python
from flask import Flask, render_template, Response
from MjpegCameraFactory import MjpegCameraFactory

camera = MjpegCameraFactory().getCameraByName("DefaultMjpegCamera")
```

The getCameraForPlatform method will try and get the first non default camera it finds available if none are found it will return the default demo camera

```python
from flask import Flask, render_template, Response
from MjpegCameraFactory import MjpegCameraFactory

camera = MjpegCameraFactory().getCameraForPlatform()
```

## Running it
To start the server on the command line type
```bash

python3 app.py
```
To see it get the address of your pi or server and type into your browser http://\<address of pi or server\>:5001
