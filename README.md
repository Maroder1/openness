# RPA for creating and configuring a TIA Portal project   
This project aims to develop a user-friendly data input interface for automating project generation on the TIA Portal, leveraging the TIA Openness API. It consists of a GUI built in Python, utilizing tkinter and pythonnet, to facilitate the management of TIA Portal project creation.
>
    
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

## Before build
Before building, you must edit the "project_dll" variable, in Core/openness.py, so that it reflects the directory where the Siemens.Engineering.dll is saved on your machine

## How to build
 1. in the windows search bar type "command prompt" to open Command Promt (CMD)
 2. Browse to the location of the **build.py** file and run it with the following command


```
 python build.py
```
Your program will be in core/build/exe.win-amd64-3.12
