# Old appointment dictionary creations: now it's done by importing a csv
"""
surnames = [ "Smith", "Jones", "Taylor", "Williams", "Brown", "Davies", "Evans",
"Wilson", "Thomas", "Roberts", "Johnson", "Lewis", "Walker", "Robinson", "Wood",
"Thompson", "White", "Watson", "Jackson", "Wright", "Green", "Harris", "Cooper",
"King", "Lee", "Martin", "Clarke", "James", "Morgan", "Hughes"]

names = ["Liam", "Emma", "Noah", "Olivia", "William", "Ava", "James",
"Isabella", "Logan", "Sophia", "Benjamin", "Mia", "Mason", "Charlotte",
"Elijah", "Amelia", "Oliver", "Evelyn", "Jacob", "Abigail", "Lucas", "Harper",
"Michael", "Emily", "Alexander", "Elizabeth", "Ethan", "Avery", "Daniel",
"Sofia"]
"""

"""
appointments = dict()


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

"""
for i in range(30):
    appointment = {
      "Name": names[random.randint(0, len(names)-1)],
      "Surname": surnames[random.randint(0, len(surnames)-1)],
      "House" : locations[random.randint(0, len(locations)-1)],
      "Day" : [days[random.randint(0, len(days)-1)], days[random.randint(0, len(days)-1)], days[random.randint(0, len(days)-1)]],
      "Pref" : [prefs[random.randint(0, len(prefs)-1)]]
    }
    appointments[str(i)] = appointment
"""
