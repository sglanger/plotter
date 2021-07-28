# plotter
* Author sg langer July 2021

# Intro
* Purpose: Proof of concept repository to do the elementary steps needed to 
	* take an incoming DICOM SR
	* Crack its header and get patient and study demographics
	* use the above to fetch relevent priot SR's from a VNA
	* [OPTIONAL phase 1] Assure compliance of SR to ACR RADS
	* perform math or plotting
	* Send result to LBnet for injection into PS360

* Assumptions
	* this repo is standalone, but for POC purpose is running on a VM under the /home/site acct
	* host VM libs provided: dcmtk, python, pydicom, etc
	* host VM services provided: DICOM receiver, file watching service, VNA (Orthanc) for test data

# Details
* fwatcher: a python watchdog process that monitors a ROOT folder (and below) for new files drops. When it finds same it bases the action taken based on the folder the file was dropped into see fwatcher:call_analytic for details. Can be installed as a service or run manually. 
* DICOM receiver info: AET=PLOTTER, port=9010
* ssh in: port=2200, site/sitePass
* Orthanc DICOM info: AET=
* Landing page: on virtualbox VM, http://localhost:7500


# HOWTO
* Adding new functions: 
	* For example, the /input handler (prepper.py) when called by fwatcher should: 
		* check the file is an SR, delete if not 
		* make a /tmp/patID folder above /pipeline, move the /input/SR to it 
		* crack the header for demographics and pull priors to it (eg. /tmp/patID/new and /tmp/patID/priors
		* pass the loaded patID folder to /pipeline/pending folder for pickup by the next handler

