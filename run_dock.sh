#!/bin/bash

###############################################
# Author: SG Langer Jul 2021
# Purpose: put all the Docker commands to build/run 
#	ddw-gway in one easy place
#
# Notes: If you are building from scratch, run this whole thing
#	If pulling from Docker hub, just run the RUN and EXEC lines
##########################################
clear

vmtype=$(sudo virt-what|grep virtualbox)
if [ $vmtype ] ; then
	# Vbox
	echo $vmtype
	host="10.0.2.15"
	#host="10.0.2.2"
else
	# VMware
	echo $vmtype
	host="172.17.0.1"
fi
ROOT="/home/site"

image="jodogne/orthanc-plugins"
instance="plotter"
srvc="plotter"

case "$1" in
	build)
		# clone the plotter code and site direcotry structure
		git clone https://github.com/sglanger/$srvc.git

		# install as a service
  		# https://computingforgeeks.com/how-to-run-java-jar-application-with-systemd-on-linux/
		sudo cp $ROOT/$srvc/$srvc.service /usr/lib/systemd/system/$srvc.service
		sudo systemctl daemon-reload
		sudo systemctl enable $srvc

		$0 start
	;;

	conn)
		#sudo docker run -it $instance /bin/bash $image
		sudo docker exec  -it $instance /bin/bash 
	;;


	restart)
		$0 stop
		$0 start
	;;

	status)
		sudo systemctl status $srvc 
	;;

	stop)
		# stops but does not remove image from DOcker engine
		sudo systemctl stop $srvc
	;;

	start)
		sudo systemctl start $srvc
	;;


	*)
		echo "invalid option"
		echo "valid options: build/start/stop/status/conn"
		exit
	;;
esac
