#!/usr/bin/python3

#################################### prepper.py
# Purpose: take a files dropped into /pipeline/input, 
#	maake sure it is a SR, if so  fetch priors and 
#	pass to the next link in the pipeline
#
# Author: ???
# Date : ???
#

 
import time, os
import pydicom


if __name__ == "__main__":
#############################################################
# Purpose: be called by fwatcher.py, create a /patID folder 
#  above /pipeline, stuff it with priors if any, then move whole
#  /patIT to pipeline/pending	
#
# Advice, this does not need to be a class
############################################################
      os.system('clear')


