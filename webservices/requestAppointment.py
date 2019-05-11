'''
 module to handle appointment requests
 # receives a dictionary from the webserver
 # loads the current requested appointments from `data/requestedAppointments.json`
 # adds the new request with a ordered key
 # writes to `data/requestedAppointments.json`
'''

import json
import pprint as pp


# path to the json file storing the requested appointments
requestedAppointmentsFile = "data/requestedAppointments.json"

# function to load the json file to a dict 
def loadAppointments(filePath):
    appointments = {}

    with open(filePath, 'r') as f:
      try:
        appointments = json.load(f)
      except:
        appointments = {}

    return appointments

# function to write a dict to the json file
def writeAppointments(filePath, content):
  with open(filePath, 'w') as json_file:
    json.dump(content, json_file, indent=4)


# webservice function called by the webserver to add a new appointment request
def requestAppointment(request):

  # load the appointments already requested
  requestedAppointments = loadAppointments(requestedAppointmentsFile)

  # find the new ordered key to add a new request
  if requestedAppointments:
    key = int(list(requestedAppointments.keys())[-1]) + 1
  else:
    key = 0

  # add the new request passed by the webserver
  requestedAppointments[key] = request

  # write to the file storing the requested appointments
  writeAppointments(requestedAppointmentsFile, requestedAppointments)

  #TODO: delete temporary print
  print("####### Updated Requests:\n")
  pp.pprint(requestedAppointments)

  


  
  






