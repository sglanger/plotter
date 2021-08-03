#!/usr/bin/python3

#################################### prepper.py
# Purpose: take a patID folder  dropped into /pipeline/pending, 
#	classify what kind of exam it is and call proper hander, 
#	then pass to the next link in the pipeline
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

  tmp = os.getcwd() + '/tmp/'
  patID = path[path.index('pending')+8 : ]

  try :
    os.system('mv -f ' + path + ' ' + tmp)
    tags = getDemog(tmp + patID)
    classify(tags, tmp + patID)
  except :
    print('some error ')
    #os.system('rm ' + path)
    pass

  return


def getDemog(file):
############################
# Purpose: get Patient ID and 
#  exam info needed to classify a handler
###########################
  tags = []
  #print ('file = '+  file)
  for i in os.listdir(file) :
    #print (i)
    if 'dcm' in i : break

  ds = pydicom.dcmread(i)
  
  for tag in ds:
    #print (tag)
    if 'Study Description' in str(tag): tags.append(str(tag)) 
    if 'Patient\s Name' in str(tag): tags.append(str(tag)) 
    if 'Patient ID' in str(tag): tags.append(str(tag)) 
    if 'SOP Class UID' in str(tag): tags.append(str(tag)) 

  #print (tags)
  return tags

def classify(list, file):
############################
# Purpose: use PatId to make 
#  a temp Dir
###########################

  for i in list:
    i = str(i)
    #print (i)
    if 'Patient ID' in i: PatID=i[i.index('LO:') +5 : -1]
    if 'Description' in i: Descrip=i[i.index('LO:') +5 : -1]

  print (PatID)
  print (Descrip)
  
  # now in here call some handler for this exam type
  return 



if __name__ == "__main__":
#############################################################
# Purpose: be called by fwatcher.py, create a /patID folder 
#  from pipeline/pending to /tmp, call proper handler,
#  then pass reults to pipeline/send
#
############################################################
  #os.system('clear')
  print ('in dispatcher')

  # use cmd line arg to locate projectDir
  if len(sys.argv ) != 2 :
    print ("Incorrect Usage: Must include -input file path- ") 
    print (">./prepper.py file_path ")
    sys.exit(1)

  filePath = sys.argv[1]
  checkDICOM(filePath)

  sys.exit()

