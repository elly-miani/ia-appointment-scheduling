from random import sample
import random
import csv





appointments = dict()

"""
appointment1 = {
  "Name": "Ford",
  "Surname": "Mustang",
  "House" : "A",
  "Day" : ["mon", "wed", "fri"],
  "Day" : ["mon"],
  "Pref" : ["Morning"]
}

appointment2 = {
  "Name": "Ford",
  "Surname": "Mustang",
  "House" : "A",
  "Day" : ["mon"],
  "Pref" : ["Morning"]
}


appointments["1"] = appointment1
appointments["2"] = appointment2
"""

days = ["mon", "tue", "wed", "thu", "fri", "sat"]

hours = ["08.00", "08.50", "09.00", "09.50", "10.00", "10.50", "11.00", "11.50",
"13.00", "13.50", "14.00", "14.50", "15.00", "15.50", "16.00", "16.50", "17.00",
"17.50"]

locations = ["A", "B", "C", "D"]

surnames = [ "Smith", "Jones", "Taylor", "Williams", "Brown", "Davies", "Evans",
"Wilson", "Thomas", "Roberts", "Johnson", "Lewis", "Walker", "Robinson", "Wood",
"Thompson", "White", "Watson", "Jackson", "Wright", "Green", "Harris", "Cooper",
"King", "Lee", "Martin", "Clarke", "James", "Morgan", "Hughes"]

names = ["Liam", "Emma", "Noah", "Olivia", "William", "Ava", "James",
"Isabella", "Logan", "Sophia", "Benjamin", "Mia", "Mason", "Charlotte",
"Elijah", "Amelia", "Oliver", "Evelyn", "Jacob", "Abigail", "Lucas", "Harper",
"Michael", "Emily", "Alexander", "Elizabeth", "Ethan", "Avery", "Daniel",
"Sofia"]

prefs = ["Morning", "Afternoon"]

datasetDimensions=[5, 10, 15, 20, 25, 30]
for k in datasetDimensions:
    for i in range(k):
        y = 3 # random.randint(1, 3)
        appointment = {
          "Name": names[random.randint(0, len(names)-1)],
          "Surname": surnames[random.randint(0, len(surnames)-1)],
          "House" : locations[random.randint(0, len(locations)-1)],
          "Day" : [sample(days, y)],
          "Pref" : [prefs[random.randint(0, len(prefs)-1)]]
        }
        appointments[str(i)] = appointment

    print(appointments)
    """
    with open('RandomAppointments.csv', 'w') as f:
        for key in appointments.keys():
            f.write("%s,%s\n"%(key, appointments[key]))
    """
    with open('Datasets/RandomAppointments'+str(k)+'.csv', 'w') as f:
        writer = csv.writer(f)
        for key, values in appointments.items():
            row = [key] + [value for item in values.items() for value in item]
            writer.writerow(row)
