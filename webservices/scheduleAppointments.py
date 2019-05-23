'''
 module to handle appointment requests
 # receives a dictionary from the webserver
 # loads the current requested appointments from `data/requestedAppointments.json`
 # adds the new request with a ordered key
 # writes to `data/requestedAppointments.json`
'''

import sys
import json
import pprint as pp

sys.path.append('./Solver')
from SolverWithBacktrack import scheduler 



# path to the json file storing the requested and scheduled appointments
requestedAppointmentsFile = "data/requestedAppointments.json"
scheduledAppointmentsFile = "data/scheduledAppointments.json"

# function to load the json file to a dict 
def loadAppointments(filePath):
    appointments = {}

    with open(filePath, 'r') as f:
      try:
        appointments = json.load(f)
      except:
        appointments = {}

    return appointments



# webservice function called by the webserver to schedule and load appointments
def scheduleAppointments():

  scheduler(requestedAppointmentsFile)
  # load the appointments already requested
  scheduledAppointments = loadAppointments(scheduledAppointmentsFile)

  

  #TODO: delete temporary print
  print("####### Scheduled appointments:\n")
  pp.pprint(scheduledAppointments)
  return scheduledAppointments

  


  
  






