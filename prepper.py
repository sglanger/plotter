#!/usr/bin/python3

#################################### prepper.py
# Purpose: take a files dropped into /pipeline/input, 
#	maake sure it is a SR, if so fetch related priors and 
#	pass to the next link in the pipeline
#
# Author: SG Langer 
# Date : July 2021
##################################
 
import time, os, sys
import pydicom

def checkDICOM(path):
#############################
# Purpose: see if DICOM, if yes dispatch prefetch
# tasks, else delete.
############################

  try :
    ds = pydicom.dcmread(path)
    tags = getDemog(ds)
    tmpDir = mkTmpDir (tags, path)
  except :
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
    if 'Patient ID' in str(i): 
      PatID=i[i.index('LO:') +5 : -1]

  tmpDir = os.getcwd() + '/tmp/'  + PatID
  print (tmpDir)

  try:
    # make tmp folder for this patient
    os.system('mkdir ' +tmpDir)
    os.system('mkdir ' +tmpDir +'/priors')
    # and now move DICOM from input to /tmp/patID
    os.system('mv ' + file +' ' + tmpDir)  
  except: 
    print('could not make  folder ' + tmpDir)
    pass

  return tmpDir


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

