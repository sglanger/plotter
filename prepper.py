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
# Purpose: if DICOM dispatch prefetch
# tasks, else delete
############################

  try :
    ds = pydicom.dcmread(path)
    tags = getDemog(ds)
    mkTmpDir (tags, path)
  except e:
    print (e)
    print('not dicom, deleting it and exiting')
    os.system('rm ' + path)
    sys.exit(1)

  return


def getDemog(file):
############################
# Purpose: get Patient ID and 
#  exam info
###########################
  tags = []

  for tag in file:
    #print (tag)
    if 'Study Description' in str(tag): tags.append(str(tag)) 
    if 'Patient\s Name' in str(tag): tags.append(str(tag)) 
    if 'Patient ID' in str(tag): tags.append(str(tag)) 
    if 'SOP Class UID' in str(tag): tags.append(str(tag)) 

  #  this not working
  #tags.append(file.PatientsName)
  #tags.append(file.SOPClassUID)
  #tags.append(file.PatientID)
  #tags.append(file.StudyDescription)

  #print (tags)
  return tags

def mkTmpDir(list, file):
############################
# Purpose: use PatId to make 
#  a temp Dir
###########################

  for i in list:
    print (i)
    #if 'ID' in str(i): PatID=str(i)

  tmpDir = os.getcwd() + '/tmp/' # + PatID
  print (tmpDir)
  
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

