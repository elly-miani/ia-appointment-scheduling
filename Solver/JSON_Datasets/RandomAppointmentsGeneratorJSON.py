from random import sample
import random
import json
import sys



appointments = dict()

days = ["mon", "tue", "wed", "thu", "fri"]
#days = ["mon", "tue", "wed"]

#hours = ["08.00", "08.50", "09.00", "09.50", "10.00", "10.50", "11.00", "11.50",
#"13.00", "13.50", "14.00", "14.50", "15.00", "15.50", "16.00", "16.50", "17.00",
#"17.50"]
#hours = ["08.00", "08.50", "09.00", "09.50", "10.00", "10.50", "11.00", "11.50",
#"13.00", "13.50", "14.00", "14.50", "15.00", "15.50", "16.00", "16.50"]

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
# qui si usava una lista, ma è più comodo passare la dimensione da terminale
datasetDimensions=[20]#int(sys.argv[1])]#, 10, 15, 20, 25, 30]
indexes=['A', 'B', 'C', 'D', 'E']
x = 0
for k in datasetDimensions:
    for i in range(k):
        # y = 2
        y = random.randint(2, 3)
        d = sample(days, y)
        app = []
        
        for a in range(y):
          newApp = (days[random.randint(0, len(days)-1)], prefs[random.randint(0, len(prefs)-1)])
          if newApp not in app:
            app.append(newApp)
          else:
            a-=1
        appointment = {
          "Name": names[random.randint(0, len(names)-1)],
          "Surname": surnames[random.randint(0, len(surnames)-1)],
          "House" : locations[random.randint(0, len(locations)-1)],
          "Day" : app,
        }
        appointments[str(i)] = appointment

    # print(appointments)
    print("Creating JSON file with " + str(k) + " appointments.")

    with open('Solver/JSON_Datasets/'+str(k)+'/RandomAppointments'+ indexes[x]+str(k)+'.json', 'w') as json_file:
      json.dump(appointments, json_file, indent=4)
      # json.dump(appointments, json_file)
    x+=1