from random import sample
import random
import json
import sys

requestedAppointmentsFile = "data/requestedAppointments.json"


days = ["mon", "tue", "wed", "thu", "fri"]

locations = ["A", "B", "C", "D"]

surnames = ["Smith", "Jones", "Taylor", "Williams", "Brown", "Davies", "Evans",
            "Wilson", "Thomas", "Roberts", "Johnson", "Lewis", "Walker", "Robinson", "Wood",
            "Thompson", "White", "Watson", "Jackson", "Wright", "Green", "Harris", "Cooper",
            "King", "Lee", "Martin", "Clarke", "James", "Morgan", "Hughes"]

names = ["Liam", "Emma", "Noah", "Olivia", "William", "Ava", "James",
         "Isabella", "Logan", "Sophia", "Benjamin", "Mia", "Mason", "Charlotte",
         "Elijah", "Amelia", "Oliver", "Evelyn", "Jacob", "Abigail", "Lucas", "Harper",
         "Michael", "Emily", "Alexander", "Elizabeth", "Ethan", "Avery", "Daniel",
         "Sofia"]

prefs = ["Morning", "Afternoon"]


def generateRandomRequests(numAppointments):
  appointments = dict()

  datasetDimensions = [numAppointments]  # , 10, 15, 20, 25, 30]
  for k in datasetDimensions:
    for i in range(k):
      y = random.randint(2, 3)
      d = sample(days, y)
      app = []
      for a in range(y):
        newApp = (days[random.randint(0, len(days)-1)],
                  prefs[random.randint(0, len(prefs)-1)])
        if newApp not in app:
          app.append(newApp)
      appointment = {
          "Name": names[random.randint(0, len(names)-1)],
          "Surname": surnames[random.randint(0, len(surnames)-1)],
          "House": locations[random.randint(0, len(locations)-1)],
          "Day": app,
      }
      appointments[str(i)] = appointment

    # # print(appointments)
    # print("Creating JSON file with " + str(k) + " appointments.")

    with open(requestedAppointmentsFile, 'w') as json_file:
      json.dump(appointments, json_file, indent=4)
