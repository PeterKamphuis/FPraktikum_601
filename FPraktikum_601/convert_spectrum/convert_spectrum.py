# -*- coding: future_fstrings -*-
# Functions commonly used in the package

import os 
import numpy as np
from astropy.io import fits
import matplotlib.pyplot as plt

def convert_spectrum(file_name,base_name):
    '''function to convert a single file'''
    spectrum = fits.open(file_name)
    found_spectrum = get_spectrum(spectrum[1].data)
    header = spectrum[1].header
    spectrum.close()
    #Create the xaxis
    xaxis = (float(header['BASEFREQ'])+\
              np.arange(len(found_spectrum))*float(header['BNDRES']))/1e6
 
    plot_spectrum(xaxis,found_spectrum,base_name)
    write_spectrum(xaxis,found_spectrum,header,base_name)
    
   
def create_directory(directory,base_directory):
    split_directory = [x for x in directory.split('/') if x]
    split_directory_clean = [x for x in directory.split('/') if x]
    split_base = [x for x in base_directory.split('/') if x]
    #First remove the base from the directory but only if the first directories are the same
    if split_directory[0] == split_base[0]:
        for dirs,dirs2 in zip(split_base,split_directory):
            if dirs == dirs2:
                split_directory_clean.remove(dirs2)
            else:
                if dirs != split_base[-1]:
                    raise InputError(f"You are not arranging the directory input properly ({directory},{base_directory}).")
    for new_dir in split_directory_clean:
        if not os.path.isdir(f"{base_directory}/{new_dir}"):
            os.mkdir(f"{base_directory}/{new_dir}")
        base_directory = f"{base_directory}/{new_dir}"
    return f'{base_directory}/'
create_directory.__doc__ =f'''
 NAME:
    create_directory

 PURPOSE:
    create a directory recursively if it does not exists and strip leading directories when the same fro the base directory and directory to create

 CATEGORY:
    support_functions

 INPUTS:
    directory = string with directory to be created
    base_directory = string with directory that exists and from where to start the check from

 OPTIONAL INPUTS:


 OUTPUTS:

 OPTIONAL OUTPUTS:
    The requested directory is created but only if it does not yet exist

 PROCEDURES CALLED:
    Unspecified

 NOTE:
'''

def get_spectrum(data):
    '''Get the combined and calibrated spectrum'''    
    spectra_raw = [[],[]]
    spectra_off = [[],[]]
    spectra_cal = [[],[]]
    for i in range(len(data)):
        line = data[i]
        if line[9] == 'on':
            spectra_raw[0].append(line[7])
            spectra_raw[1].append(line[8])
        elif line[9] == 'off':
            spectra_off[0].append(line[7])
            spectra_off[1].append(line[8])
        elif line[9] == 'cal': 
            spectra_cal[0].append(line[7])
            spectra_cal[1].append(line[8])           
    spectra_lr = np.array(spectra_raw,dtype=float )/ np.array(spectra_cal,dtype=float) - \
                 np.array(spectra_off,dtype=float )/ np.array(spectra_cal,dtype=float) 
    spectrum = []
    for i in range(len(spectra_lr)):
        spectrum.append((spectra_lr[0][i]+spectra_lr[1][i])/2.)
    spectrum = np.array(spectrum,dtype=float)
    return np.mean(spectrum,axis = 0)

def plot_spectrum(x,y,base_name):
    fig = plt.figure()
    plt.plot(x,y)  
    plt.savefig(f'{base_name}.png')
    plt.close()

def raw_to_clean(cfg):
    '''MAin function for converting all input files'''
    cfg.output_directory = create_directory(cfg.output_directory,\
                                            cfg.input_directory)
   
    for file in cfg.file_names:
        file_name = f'{cfg.input_directory}/{file}'
        if not os.path.isfile(file_name):
            print(f'''We can not find the file {file_name}.
Please check its name.''')
            continue
        stripped_file_name = os.path.splitext(file)[0]
        base_name=f'{cfg.output_directory}{stripped_file_name}_cleaned'
        convert_spectrum(file_name,base_name)

def write_spectrum(x,y,header,base_name):
    with open(f'{base_name}.txt','w') as file:
        file.write(f'# The header information. \n ')
        for key in header:
            file.write(f'# {key} = {header[key]}\n')
        file.write(f'#!!!!!!!!!The Spectrum !!!!!!!!!!!!!!!\n ')
        file.write(f'''# {'Freq (Mhz)':<9s}  {'Intensity (ADU)':<10s}\n''')
        for i,val in enumerate(y):
            file.write(f'''{x[i]:10.5f}  {val:10.5f}\n''')
