# NSFW Content Filter for OBS

A script for automatically hiding the screen in OBS when NSFW content is detected on the user's screen.

## Installation

1. **Install Python**
   - Download and install [Python](https://www.python.org/downloads /).

3. **Clone or download the repository**:
   - ``git clone https://github.com/Serfetto/NSFW-Classification ``
3. **Install dependencies**
   - ``pip install -r path\to\requirements.txt ``
5. **Select the launch method**
   - On a graphics card (GPU): Make sure that you have PyTorch installed with CUDA support. Follow the PyTorch instructions to install the desired version.
   - On the processor (CPU): No additional settings are required.
## Launch
1. **Add the video source to OBS**
   - Note: the script takes a screenshot of the entire screen, and does not use direct interaction with OBS.
3. **Configure Python in OBS**
   - Open OBS, go to the Tools → Scripts tab.
   - In the scripts window, go to the Python Settings tab and specify the path to python.exe . It is usually located along the path: ``C:\Users \<name>\AppData\Local\Programs\Python\Python<version>``
   - After successfully adding Python, you will see a message about the Python version (for example, "Python version 3.10 has been downloaded").
3. **Add the script**
   - In the Scripts tab, click on the `+` icon and select the file ``ScriptWithUI.py ``.
5. **Model and scene settings**
   - After adding the script, you will be prompted to specify the path to the model and the scene where the filter will be created to hide the screen (the source `Background color` is added).
5. **Download the model**
   - The model is available for download at this [link] (https://drive.google.com/file/d/1Vl5pY9ERFb-L5eF73Qt9Dumkmlrgykyk/view ?usp=drive_link).
7. **Specify the path to the model**
   - Example of a path: ``C:\Users \<name>\Downloads\512old.pt ``
7. **Start filtering**
   - Click the `Start filtering` button so that the script creates a "Background Color (filter nsfw)" source. After clicking on the `Stop filtering` button, the script will automatically delete the created source and finish its work
   - The script will launch a model that will hide the screen when NSFW content is detected. Depending on your settings, the startup can take place on the GPU or CPU (see the section "Installation", point 4).
