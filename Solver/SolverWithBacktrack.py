import networkx as nx
import itertools
import matplotlib.pyplot as plt
import time
import sys
import json
from copy import deepcopy
import pprint as pp

from Backtracking_Appointments import backtrackingSearch
from Backtracking_Appointments import backtrackingSearchAllSolutions


current_milli_time = lambda: int(round(time.time() * 1000))


def takeSecond(elem):
    return elem[1]


# load appointments from a csv file in *filePath*
def loadAppointments(filePath):
    appointments = {}

    with open(filePath, 'r') as f:
        appointments = json.load(f)
    
    return appointments

# def loadAppointments(filePath):
#     appointments = {}

#     with open(filePath, 'r') as f:
#         reader = csv.reader(f)
#         for row in reader:
#             a = iter(row[1:])
#             appointments[row[0]] = dict(zip(a, a))

#     return appointments


# intialize a generic domain with all possible combinations of days, hours and locations
def initDomainR():
    '''
    Data per il dominio
    '''
    #days = ["mon", "tue", "wed", "thu", "fri", "sat"]
    days = ["mon", "tue", "wed"]

    #hours = ["08.00", "08.50", "09.00", "09.50", "10.00", "10.50", "11.00", "11.50",
    #"13.00", "13.50", "14.00", "14.50", "15.00", "15.50", "16.00", "16.50", "17.00",
    #"17.50"]
    #hours = ["08.00", "08.50", "09.00", "09.50", "10.00", "10.50", "11.00", "11.50",
    #"13.00", "13.50", "14.00", "14.50", "15.00", "15.50", "16.00", "16.50"]


    hours = ["08.00", "08.50", "09.00", "09.50", "15.00", "15.50", "16.00", "16.50"]

    locations = ["A", "B", "C", "D"]

    domain = []
    count = 0

    for i in days:
        for y in hours:
            for loc in locations:
                domain.append([i])
                domain[count].append(y)
                domain[count].append(loc)
                count += 1

    return domain

# intialize a generic domain with all possible combinations of days, hours and locations
def initDomain():
    '''
    Data per il dominio
    '''
    days = ["mon", "tue", "wed", "thu", "fri", "sat"]
    
    hours = ["08.00", "08.50", "09.00", "09.50", "10.00", "10.50", "11.00", "11.50",
    "13.00", "13.50", "14.00", "14.50", "15.00", "15.50", "16.00", "16.50", "17.00",
    "17.50"]
    
    locations = ["A", "B", "C", "D"]

    domain = []
    count = 0

    for i in days:
        for y in hours:
            for loc in locations:
                domain.append([i])
                domain[count].append(y)
                domain[count].append(loc)
                count += 1

    return domain

# print function to print a solution in a clean way
def printSolution(solution):
    days = ["mon", "tue", "wed", "thu", "fri", "sat"]

    ordApp = [[], [], [], [], [], []]
    notSched = []

    for x in solution:
        if solution[x] != "notScheduled":
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
        else:
            notSched.append([x, solution[x]])
    # print(ordApp)
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
    print(notSched)


# print function to print a solution in a clean way
def printSolutionR(solution):
    days = ["mon", "tue", "wed"]

    ordApp = [[], [], []]
    notSched = []

    for x in solution:
        if solution[x] != "notScheduled":
            if solution[x][0] == days[0]:
                ordApp[0].append([x, solution[x]])
            if solution[x][0] == days[1]:
                ordApp[1].append([x, solution[x]])
            if solution[x][0] == days[2]:
                ordApp[2].append([x, solution[x]])
        else:
            notSched.append([x, solution[x]])
    # print(ordApp)
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
    print(notSched)



appointments = loadAppointments(sys.argv[1])
#print(appointments)
domain = initDomain()
#print(domain)


# Invece che problem faccio un grafo dei vincoli, aggiungo un nodo per ciascuna variabile e relativo domino.
ConstraintGraph = nx.Graph()
ConstraintGraphCost = nx.Graph() 

variablesName = []

# for each appointment (iterate on the numerical key of the appointments)
for x in appointments:
    dom = []
    # check which elements of the generic domain are necessary for this appointment
    for y in domain:
        hour , minutes = y[1].split(".")
        hour = int(hour)

        if "Morning" in appointments[x]["Pref"] and hour < 12 and y[0] in appointments[x]["Day"] and y[2] in appointments[x]["House"]:
            dom.append(y)

        if "Afternoon" in appointments[x]["Pref"] and hour > 12 and y[0] in appointments[x]["Day"] and y[2] in appointments[x]["House"]:
            dom.append(y)
    
    ConstraintGraph.add_node(x, domain = deepcopy(dom))
    dom.append("notScheduled")
    #Aggiungo la variabile corrente con il domain aggiustato
    ConstraintGraphCost.add_node(x, domain = dom)
    variablesName.append(x)

# Add edges to the constraint graph only if the two variables share at least one element of the domain, it is possible to make this part better
a =itertools.combinations(variablesName, 2)

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
                    stop = True
                    break

                    
                

ConstraintGraph.add_edges_from(itertools.combinations(variablesName, 2))

#ConstraintGraphCost.add_edges_from(itertools.combinations(variablesName, 2))


'''
nx.draw(ConstraintGraph)
ax = plt.gca()
ax.collections[0].set_edgecolor("#ffffff")
plt.show()

nx.draw(ConstraintGraphCost)
ax = plt.gca()
ax.collections[0].set_edgecolor("#ffffff")
plt.show()
'''

#solution = problem.getSolutions()
#Chiamo il solutore fatto in casa...
'''
start = current_milli_time()
solution = backtrackingSearch(ConstraintGraph)
end = current_milli_time()
print("\n\n###########Time spent to find the first solution = ", end-start," ms.\n\n")
#print(solution)
printSolution(solution)
'''



start = current_milli_time()
sol = backtrackingSearchAllSolutions(ConstraintGraphCost, 30000)
end = current_milli_time()
print("\n\n###########Time spent to find all solution = ", end-start," ms.\n\n")
print(sol[0])
printSolution(sol[0])
print("With cost = ", sol[1])

