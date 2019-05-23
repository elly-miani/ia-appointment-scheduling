from constraint import Problem
import pprint as pp
import random
import csv
import time
import sys
import json
import itertools
import networkx as nx

current_milli_time = lambda: int(round(time.time() * 1000))


def constraintFunction():
    def innerFunction (x, y):
        # [0] is 'Day': if they are in different days there's no needed constraint 
        if x[0] != y[0]:
            return True
        bothMorning = float(x[1]) <= 11.5 and float(y[1]) <= 11.5
        bothAfternoon = float(x[1]) > 12.0 and float(y[1]) > 12.0
        isSamePeriod = bothMorning or bothAfternoon
        if (x[2] != y[2] and isSamePeriod and abs(float(x[1])-float(y[1])) < distance(x[2], y[2])*0.5 + 1):
            return False
        if (x[2] == y[2] and isSamePeriod and abs(float(x[1])-float(y[1])) != 1):
            return False
        else:
            return True
    return innerFunction


def distance(a, b):
    if (a=='A' and b=='B') or (b=='A' and a=='B'):
        return 1
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


def takeSecond(elem):
    return elem[1]



# intialize a generic domain with all possible combinations of days, hours and locations
def initDomain():
    days = ["mon", "tue", "wed", "thu", "fri", "sat"]

    hours = ["08.00", "08.50", "09.00", "09.50", "10.00", "10.50", "11.00", "11.50",
             "14.00", "14.50", "15.00", "15.50", "16.00", "16.50", "17.00", "17.50"]

    locations = ["A", "B", "C", "D"]

    #prefs = ["Morning", "Afternoon"]


    dominio = []
    count = 0

    for i in days:
        for y in hours:
            for loc in locations:
                dominio.append([i])
                dominio[count].append(y)
                dominio[count].append(loc)
                count += 1

    return dominio


# load appointments from a csv file in *filePath*
# load appointments from a csv file in *filePath*
def loadAppointments(filePath):
    appointments = {}

    with open(filePath, 'r') as f:
        appointments = json.load(f)

    # pp.pprint(appointments)
    # print(appointments['8'])
    return appointments

# def loadAppointments(filePath):
#     appointments = {}

#     with open(filePath, 'r') as f:
#         reader = csv.reader(f)
#         for row in reader:
#             a = iter(row[1:])
#             appointments[row[0]] = dict(zip(a, a))

#     return appointments


def solver(domain, appointments):
    problem = Problem()
    ConstraintGraphCost = nx.Graph()
    variablesName = []
    # for each appointment (iterate on the numerical key of the appointments)
    for x in appointments:
        dom = []
        # check which elements of the generic domain are necessary for this appointment
        for y in domain:
            hour , minutes = y[1].split(".")
            hour = int(hour)
            #print(appointments[x])
            #print(appointments[x]["Day"])
            
            for a in appointments[x]["Day"]:
                if "Morning" == a[1] and hour < 12 and y[0] in a[0] and y[2] in appointments[x]["House"]:
                    dom.append(y)

                if "Afternoon" == a[1] and hour > 12 and y[0] in a[0] and y[2] in appointments[x]["House"]:
                    dom.append(y)
            
        #Aggiungo la variabile corrente con il domain aggiustato
    #    print(dom)
        variablesName.append(x)
        ConstraintGraphCost.add_node(x, domain = dom)
        problem.addVariable(x, dom)
        
    a = itertools.combinations(variablesName, 2)

    for i in a:
        #print("Considero ", i)
        stop = False
        for domItem1 in ConstraintGraphCost.nodes[i[0]]['domain']:
            if(stop):
                break
            else:
                for domItem2 in ConstraintGraphCost.nodes[i[1]]['domain']:
                    if domItem1[0] == domItem2[0] and domItem1[1] == domItem2[1] and domItem1!="notScheduled" :
                        #print("creo edge")
                        ConstraintGraphCost.add_edge(i[0], i[1])
                        problem.addConstraint(constraintFunction(), (i[0], i[1]))
                        stop = True
                        break

    start = current_milli_time()
    solution = problem.getSolution()
    end = current_milli_time()
    print("\n\n###########Time spent to find the first solution = ", end-start, " ms.\n\n")
    
    # pp.pprint(solution)

    return solution


# print function to print a solution in a clean way
def printSolution(solution):
    ordApp = [[], [], [], [], [], []]

    days = ["mon", "tue", "wed", "thu", "fri", "sat"]

    for x in solution:
        if solution[x][0] == days[0]:
            ordApp[0].append([x, solution[x]])
        if solution[x][0] == days[1]:
            ordApp[1].append([x, solution[x]])
        if solution[x][0] == days[2]:
            ordApp[2].append([x, solution[x]])
        if solution[x][0] == days[3]:
            ordApp[3].append([x, solution[x]])
        if solution[x][0] == days[4]:
            ordApp[4].append([x, solution[x]])
        if solution[x][0] == days[5]:
            ordApp[5].append([x, solution[x]])

    for x in ordApp:
        x.sort(key=takeSecond)

    index = 0
    for x in ordApp:
        print("\n\nGiorno: ", days[index])
        print("\nMattina:")
        cond = True
        for y in x:
            if (cond and float(y[1][1]) > 12):
                print("\nPomeriggio:")
                cond = False
            print("Ore: ", y[1][1], "Casa: ", y[1][2], " Appuntamento con: ",
                  appointments[y[0]]["Name"], " ", appointments[y[0]]["Surname"])
        index += 1





# main 
domain = initDomain()
appointments = loadAppointments(sys.argv[1])

solution = solver(domain, appointments) 
printSolution(solution)
