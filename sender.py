#!/usr/bin/python3

#################################### sender.py
# Purpose: take a patID folder  dropped into /pipeline/pending, 
#	classify what kind of exam it is and call proper hander, 
#	then pass to the next link in the pipeline
#
# Author: SG Langer 
# Date : July 2021
##################################
 
import time, os, sys
import pydicom



if __name__ == "__main__":
#############################################################
# Purpose: be called by fwatcher.py, create a /patID folder 
#  from pipeline/pending to /tmp, call proper handler,
#  then pass reults to pipeline/send
#
############################################################
  #os.system('clear')
  print ('in sender')

  # use cmd line arg to locate projectDir
  if len(sys.argv ) != 2 :
    print ("Incorrect Usage: Must include -input file path- ") 
    print (">./dispatcher.py file_path ")
    sys.exit(1)

  filePath = sys.argv[1]
  checkDICOM(filePath)

  sys.exit()

