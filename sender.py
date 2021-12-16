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
    print (">./sender.py patID ")
    sys.exit(1)

  filePath = "pipeline/pending/" + sys.argv[1]

  # now do a send to the Laurel Bridge path to PS360
  # remember this will be a CIFS push of a PNG or JPG
  # below DICOM stuff is not applicable
  LBip = "a.b.c.d"
  LBport = "104"
  LBaet = "fake"
  cmdStr = "dcmsnd " + LBport +"@"+ LBip +":"+ LBport  +" "+ filePath
  print (cmdStr)

  sys.exit()

