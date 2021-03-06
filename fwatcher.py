#!/usr/bin/python3

import time, os
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

	
class fWatcher(FileSystemEventHandler):
#############################################
# from https://stackoverflow.com/questions/18599339/python-watchdog-monitoring-file-for-changes#18599427
# fixed lots of bugs in above
# https://programtalk.com/python-examples/watchdog.events.FileSystemEventHandler/
# look at example 4 above


    def __init__(self, path):
    ###################################
    # Purpose: setup global class vars
    ###################################
      self.last_modified = time.time()   
      self.path=path
	
      return


    def call_analytic(self, path):
    ########################################
    #
    ######################################

        out_dir = self.path + '/output'
        ana_path = '/home/site/plotter/'
        #print ("in call_ana " + path)

        if 'input' in path :
          sr_path=self.path  + '/input'
          cmd_str= ana_path + 'prepper.py'

        if 'pending' in path :
          sr_path = self.path + '/pending'
          cmd_str= ana_path + 'dispatcher.py'

        if 'sending' in path :
          sr_path = self.path + '/sending'
          cmd_str= ana_path + 'sender.py'


        for f in os.listdir(sr_path):        
            #print (f)
            x = 1

        try:
          cmd_str = cmd_str  + ' ' + sr_path + '/' +f   # out_dir
          #print (cmd_str )
          os.system(cmd_str)
          #ret = subprocess.check_output(cmd_str)
          #print (ret.decode('utf-8'))
        except:
          print (ret.decode('utf-8'))
          pass
       
        return 

    def on_modified(self, event):
    ###############################################
    # Purpose: event handler callback
    # Caller: main event_handler
    ########################################
        print (event)
        res=str(event)
        res=res[1:res.index(":")]
       	#print(f'Event type: {event.event_type}  path : {event.src_path}')

        if (res != 'FileModifiedEvent' and 'pending' not in str(event)  ) :
            print ("early return event=" + str(event))
            return
 
        else:
            self.last_modified = time.time()
            self.call_analytic(event.src_path)

        return


    def start(self, handle):
    ##################################
    # Purpose: put event handling inside
    #  a class func
    ##################################

      observer = Observer()
      self.observer = observer
      res = observer.schedule(handle, path=self.path, recursive=True)
      print (res)
      observer.start()

      try:
        while True:
          time.sleep(1)
      except KeyboardInterrupt:
        observer.stop()
        observer.join()

      return


if __name__ == "__main__":
#############################################################
# Purpose: listen to the  'input' folder, if a file
#	drops in, call the ANalytic to run on it
#
# Caller: this is a service started when the Docker/VM launches
############################################################
      os.system('clear')

      ret = subprocess.check_output('pwd')
      cwd = ret.decode('utf-8') 
      path = cwd.rstrip() + '/pipeline'
      print (cwd)

      event_handler = fWatcher(path)
      event_handler.start(event_handler)
