# Package Name

=====

Introduction
------------
This repositories contains script that can be used to transform the fits file from the SPIDER - 300 telescope into a txt file and a plot of the calibrated spectrum.


Requirements
------------
The code requires full installation of:

    python v3.8 or higher
    


[python](https://www.python.org/)


Installation
------------

Download the source code from the Github and then simply install with pip as:

  	pip install <path_to_FPraktium601>

Where <path_to_FPraktium601> is the full directory path to the directory downloaded from GitHub. Normally this directory is called FPraktikum_601. This should also install all required python dependencies.

We recommend the use of python virtual environments. If so desired a FPraktikum_601 installation would look like:

  	python3 -m venv FPraktikum_601_venv

  	source FPraktikum_601_venv/bin/activate.csh

    pip install <path_to_FPraktium601>

(In case of bash the correct middle line is FPraktikum_601_venv/bin/activate)
You might have to restart the env:

  	source FPraktikum_601_venv/bin/activate.csh

Once you have installed FPraktikum_601 you can check that it has been installed properly by running FPraktikum_601 as.

  	raw_to_clean_spectrum -v 


Running FPraktikum_601 
------------------
You  can run FPraktikum_601 by typing:

    raw_to_clean_spectrum "file_names=[name_file_1,name_file_2,...]"

You can also run FPraktikum_601 by providing a configuration file by 

    raw_to_clean_spectrum configuration_file=input_file.yml

an example yaml file with all parameters can be printed by running

    raw_to_clean_spectrum print_examples=true 


Sometime there is a shift on the frequency calibration you can apply this shift with

    raw_to_clean_spectrum "file_names=[name_file_1,name_file_2,...] apply_shift=True shift=10

where the shift is in channels.

