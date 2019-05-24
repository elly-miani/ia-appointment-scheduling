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


# path to the json file storing the requested and scheduled appointments
requestedAppointmentsFile = "data/requestedAppointments.json"
scheduledAppointmentsFile = "data/scheduledAppointments.json"


def emptySchedule():
  f = open(scheduledAppointmentsFile, "w")
  f.write("")
  f.close()

def emptyRequests():
  f = open(requestedAppointmentsFile, "w")
  f.write("")
  f.close()
