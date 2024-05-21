# RPA for creating and configuring a TIA Portal project     
>This project consists of a GUI developed in Python, using tkinter and pythonnet, to manage the creation of a TIA Portal project
><hr>
## 
    
> This project was inspired by the following repository
https://github.com/Maroder1/TIA-openness
> <hr>


 


## Installation of TIA Openness

 1. Install TIA v15.1 professional, make sure openness is checked [default]
	[Link to TIA v15.1 trail](https://support.industry.siemens.com/cs/ww/en/view/109761045)
 2. Right clik "My computer" -> Manage -> System tools -> Local users and groups - > Groups-> Double click “Siemens TIA Openness” and add your username
 3. Edit the file path in the example file to match your installation of Siemens.Engineering.dll

More details can be found in the Tia Openness [documentation](https://support.industry.siemens.com/cs/document/109792902/tia-portal-openness-automation-of-engineering-workflows?dti=0&lc=en-WW)

## Python installation
 1. [Download the Python installation wizard](https://www.python.org/downloads)
 2. Make sure Python is configured within the PATH 


## Option 1, running directly (not recommended)

 1. in the windows search bar type "command prompt" to open Command Promt (CMD)
 2. Install pythonnet by typing: *pip install pythonnet*
 3. Browse to the location of the *Screen.py* file and run it
