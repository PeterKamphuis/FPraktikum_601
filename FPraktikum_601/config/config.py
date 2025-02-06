# OmegaConf setups

from dataclasses import dataclass, field

from omegaconf import MISSING,OmegaConf
from typing import List, Optional
import os
import sys
import FPraktikum_601

@dataclass
class defaults:
    print_examples: bool = False
    configuration_file: Optional[str] = None
    verbose: bool = True
    input_directory: str = os.getcwd()
    file_names: List = field(default_factory=lambda: [None])
    output_directory: str='Cleaned_Spectra'
 

def process_input(argv):
    if '-v' in argv or '--version' in argv:
        print(f"This is version {FPraktikum_601.__version__} of the program.")
        sys.exit()
    file_name = 'raw_to_clean_spectrum_defaults.yml'
    program = 'raw_to_clean_spectrum'
    
    if '-h' in argv or '--help' in argv:      
        print(return_help_message(program,file_name))
        sys.exit()
    #First import the defaults 
    cfg = OmegaConf.structured(defaults)
    
    # read command line arguments anything list input should be set in brackets '' e.g. pyROTMOD 'rotmass.MD=[1.4,True,True]'
    inputconf = OmegaConf.from_cli(argv)
    cfg_input = OmegaConf.merge(cfg,inputconf)

    # Print examples if requested
    if cfg_input.print_examples:
        with open(file_name,'w') as default_write:
            default_write.write(OmegaConf.to_yaml(cfg_input))
        print(f'''We have printed the file {file_name} in {os.getcwd()}.
''')
        sys.exit()

    #if a configuration file is provided read it
    if not cfg_input.configuration_file is None:
        succes = False
        while not succes:
            try:
                yaml_config = OmegaConf.load(cfg_input.configuration_file)
        #merge yml file with defaults
                cfg = OmegaConf.merge(cfg,yaml_config)
                succes = True
            except FileNotFoundError:
                cfg_input.configuration_file = input(f'''
You have provided a config file ({cfg_input.configuration_file}) but it can't be found.
If you want to provide a config file please give the correct name.
Else press CTRL-C to abort.
configuration_file = ''')
    # make sure the command line overwrite the file
    cfg = OmegaConf.merge(cfg,inputconf)
    
   
    return cfg

def return_help_message(program, file_name):
    help_message = f'''
Use {program} in this way:
{program} configuration_file=inputfile.yml   where inputfile is a yaml config file with the desired input settings.
{program} -h print this message
{program} print_examples=true print a yaml file ({file_name}) with the default setting in the current working directory.
in this file values designated ??? indicated values without defaults.

All config parameters can be set directly from the command line by setting the correct parameters, e.g:
{program}  "file_names=[name_file_1,name_file_2,...]" 
'''
    return help_message   