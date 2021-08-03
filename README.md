# plotter
* Author sg langer July 2021

# Intro
* Purpose: Proof of concept repository to do the elementary steps needed to 
	* take an incoming DICOM SR
	* Crack its header and get patient and study demographics
	* use the above to fetch relevent prior SR's from a VNA
	* perform math or plotting
	* Send result to LBnet for injection into PS360

* Assumptions
	* this repo is standalone, but for POC purpose is running on a VM under the /home/site acct
	* host VM libs provided: dcmtk, python, pydicom, etc
	* host VM services provided: DICOM receiver, file watching service, VNA (Orthanc) for test data
	* We assumme we are downstrream of the LBnet SR normalizer and tags have ACR-RADS names

# Sequence of Events
* a new SR hits port 9010, DICOM listener drops it into /home/site/pipeline/input
* fwatcher sees this and calls prepper.py
* prepper takes /input/DICOM_SR and 
	* checks that its a DICOM SR, deletes and exits if not
	* if yes, makes a new folder under /tmp with that patientID
	* moves input/DICOM-SR to /tmp/patID
	* searches VNA for relevent prior SRs, puts them in /tmp/patID/priors, 
	* mv patID/ to pipeline/pending, then exits
* dispatcher.py, this is where the magic happens
	* based on study description (and other info) decides what handler to call
	* handler does things, assembles the package as new SR and/or plot
	* moves that result to /pipeline/sending/patID
* fwatcher sees new folder in /pipeline/sending and calls sender.py
* sender.py sends the package to LBnet via a C-Store, purges /pipeline/pending/patID, exits


# Details
* fwatcher: a python watchdog process that monitors a ROOT folder (and below) for new files drops. When it finds same it bases the action taken based on the folder the file was dropped into see fwatcher:call_analytic for details. Can be installed as a service or run manually. 
* DICOM receiver info: AET=PLOTTER, port=9010
* ssh in: port=2200, site/sitePass
* Orthanc DICOM info: AET=
* Orthanc Web page: on virtualbox VM, http://localhost:8042

# Websequnece steps
* from here down paste into websequence.com

title Plotter Data flow

participant SRsource
participant LBnet
participant dcmRcv
participant input
participant pending
participant fwatcher


SRsource->LBnet: dcm SRsource
LBnet->LBnet: norm value \n names
LBnet->dcmRcv: dcm normed SR
dcmRcv->input: fileSys
fwatcher->input: event-handler new SR
fwatcher-->prepper: launches to SRsource

prepper->input: fileSys fetch SR
prepper->prepper: reads demog
prepper->VNA: dcm fetches priors
prepper->pending: fileSys new SR \n with priors

fwatcher->pending: event-handler new pkg
fwatcher-->dispatcher: launches to pkg
dispatcher->pending: fileSys fetch pkg
dispatcher->dispatcher: classify study type
dispatcher->handler: fileSys pkg
handler->handler: make plots
handler->sending: fileSys plots, results

fwatcher->sending: event_handler ready pkg
fwatcher-->sender: launches to pkg
sender->sending: fileSys results pkg
sender->LBnet: dcm or fileSys results
LBnet->PS360: webAPI






