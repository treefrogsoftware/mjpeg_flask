# Mjpeg simple flask web server demo

## Python Flask example using a raspberry pi camera to generate mjpeg over http

Use standard installations for pip3 to install the python packages

## Pi and pip installs
```bash
sudo apt-get install python3
sudo apt-get install python3-pip
sudo pip3 install flask
sudo pip3 install picamera
sudo pip3 install flask.jsontools
```
## Non Pi solution

To use the code on another architecture you will need to edit the camerabridge.py
and ensure that the get_frame is implemented to produce jpeg streams using the 
output stream provided or another way.  This will require a different camera interface in the class
threading method which starts the camera and starts writing to the output stream

```python

    def get_frame(self):
        self.initialize()
        with camerabridge.output.condition:
            camerabridge.output.condition.wait()
            return camerabridge.output.frame

    @classmethod
    def _thread(cls):
        camerabridge.camera = picamera.PiCamera(resolution='640x480', framerate=24)
        camerabridge.camera.start_recording(camerabridge.output, format='mjpeg')
        while camerabridge.run:
            time.sleep(20)
```

## Running it
To start the server on the command line type
```bash

python3 app.py
```
