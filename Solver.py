from constraint import *
import random


def constraintFunction():
    def innerFunction (x, y):
        if x[0] != y[0]:
            return True
        # se sono qui sono sicuro che sto considerando due appuntamenti che avvengono nello stesso giorno.
        #print("x = ", x, "   y = ", y)
        if (x[2] != y[2] and abs(float(x[1])-float(y[1])) < distance(x[2], y[2])*0.5 + 1):
            return False
        if (x[2] == y[2] and abs(float(x[1])-float(y[1])) < 1):
            return False
        else:
            return True
    return innerFunction

def takeSecond(elem):
    return elem[1]

def distance(a, b):
    if (a=='A' and b=='B') or (b=='A' and a=='B'):
        return 2
    if (a=='A' and b=='C') or (b=='A' and a=='C'):
        return 1
    if (a=='A' and b=='D') or (b=='A' and a=='D'):
        return 2
    if (a=='B' and b=='C') or (b=='B' and a=='C'):
        return 2
    if (a=='C' and b=='D') or (b=='C' and a=='D'):
        return 1
    if (a=='B' and b=='D') or (b=='B' and a=='D'):
        return 1
    if (a == b):
        return 0




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
hours = ["08.00", "08.50", "09.00", "09.50", "10.00", "10.50", "11.00", "11.50", "13.00", "13.50", "14.00", "14.50", "15.00", "15.50", "16.00", "16.50", "17.00", "17.50"]
locations = ["A", "B", "C", "D"]
surnames = [
"Smith",
"Jones",
"Taylor",
"Williams",
"Brown",
"Davies",
"Evans",
"Wilson",
"Thomas",
"Roberts",
"Johnson",
"Lewis",
"Walker",
"Robinson",
"Wood",
"Thompson",
"White",
"Watson",
"Jackson",
"Wright",
"Green",
"Harris",
"Cooper",
"King",
"Lee",
"Martin",
"Clarke",
"James",
"Morgan",
"Hughes"
]
names = [
"Liam",	"Emma",
"Noah","Olivia",
"William","Ava",
"James","Isabella",
"Logan","Sophia",
"Benjamin","Mia",
"Mason","Charlotte",
"Elijah","Amelia",
"Oliver","Evelyn",
"Jacob","Abigail",
"Lucas","Harper",
"Michael","Emily",
"Alexander","Elizabeth",
"Ethan","Avery",
"Daniel", "Sofia"]
prefs = ["Morning", "Afternoon"]
for i in range(30):
    appointment = {
      "Name": names[random.randint(0, len(names)-1)],
      "Surname": surnames[random.randint(0, len(surnames)-1)],
      "House" : locations[random.randint(0, len(locations)-1)],
      "Day" : [days[random.randint(0, len(days)-1)], days[random.randint(0, len(days)-1)], days[random.randint(0, len(days)-1)]],
      "Pref" : [prefs[random.randint(0, len(prefs)-1)]]
    }
    appointments[str(i)] = appointment

dominio = []
count = 0


for i in days:
    for y in hours:
        for loc in locations:
            dominio.append([i])
            dominio[count].append(y)
            dominio[count].append(loc)
            count += 1

#print(dominio)
#print(appointments)

problem = Problem()

# sto iterando su tutte le chiavi
for x in appointments:
    dom = []

    for y in dominio:
        hour , minutes = y[1].split(".")
        hour = int(hour)

        if "Morning" in appointments[x]["Pref"] and hour < 12 and y[0] in appointments[x]["Day"] and y[2] in appointments[x]["House"]:
                dom.append(y)

        if "Afternoon" in appointments[x]["Pref"] and hour > 12 and y[0] in appointments[x]["Day"] and y[2] in appointments[x]["House"]:
                dom.append(y)

    #print(dom)
    problem.addVariable(x, dom)

for x in appointments:
    for y in appointments:
        if(x != y):
            #print("Aggiungo un constraint")
            problem.addConstraint(constraintFunction(), (x, y))

solution = problem.getSolution()
print(solution)

ordApp = [[],[],[],[],[],[]]
for x in solution:
    if solution[x][0]==days[0]:
        ordApp[0].append([x, solution[x]])
    if solution[x][0]==days[1]:
        ordApp[1].append([x, solution[x]])
    if solution[x][0]==days[2]:
        ordApp[2].append([x, solution[x]])
    if solution[x][0]==days[3]:
        ordApp[3].append([x, solution[x]])
    if solution[x][0]==days[4]:
        ordApp[4].append([x, solution[x]])
    if solution[x][0]==days[5]:
        ordApp[5].append([x, solution[x]])

print(ordApp)
for x in ordApp:
    x.sort(key =  takeSecond)

index = 0
for x in ordApp:
    print("\n\nGiorno: ", days[index])
    print("\nMattina:")
    cond = True
    for y in x:
        if (cond and float(y[1][1])>12):
            print("\nPomeriggio:")
            cond = False
        print("Ore: ", y[1][1], "Casa: ", y[1][2], " Appuntamento con: ", appointments[y[0]]["Name"], " ", appointments[y[0]]["Surname"])
    index+=1
