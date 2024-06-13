from prslink.g_Log import Log
import subprocess
import os
import numpy as np 

def _show_version(log=Log(), verbose=True):
    # show version when loading sumstats
    log.write("PRSLink v{} ".format(prslink_info()["version"]),verbose=verbose)
    log.write("(C) 2023-2024, Yunye He, Kamatani Lab, MIT License, gwaslab@gmail.com",verbose=verbose)

def _get_version():
    # return short version string like v3.4.33
    return "v{}".format(prslink_info()["version"])

def prslink_info():
    # version meta information
    dic={
   "version":"0.0.1",
   "release_date":"20240613"
    }
    return dic   