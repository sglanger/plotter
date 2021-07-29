#!/usr/bin/python3

#################################### prepper.py
# Purpose: take a files dropped into /pipeline/input, 
#	maake sure it is a SR, if so  fetch priors and 
#	pass to the next link in the pipeline
#
# Author: ???
# Date : ???
##################################
 
import time, os, sys
import pydicom

def checkDICOM(path):
#############################
#
#
############################

  try :
    ds = pydicom.dcmread(path)
  except:
    print('not dicom, deleting it and exiting')
    os.system('rm ' + path)
    sys.exit(1)

  return


if __name__ == "__main__":
#############################################################
# Purpose: be called by fwatcher.py, create a /patID folder 
#  in /tmp, stuff it with priors if any, then move whole
#  /patID to pipeline/pending	
#
# Advice, this does not need to be a class
############################################################
  #os.system('clear')
  print ('in prepper')

  # use cmd line arg to locate projectDir
  if len(sys.argv ) != 2 :
    print ("Incorrect Usage: Must include -input file path- ") 
    print (">./prepper.py file_path ")
    sys.exit(1)

  filePath = sys.argv[1]
  checkDICOM(filePath)

  sys.exit()

