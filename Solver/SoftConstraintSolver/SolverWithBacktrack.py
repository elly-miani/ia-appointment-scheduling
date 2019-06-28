import networkx as nx
from networkx.drawing.layout import shell_layout, circular_layout, spectral_layout, spring_layout, random_layout
import itertools
import matplotlib.pyplot as plt
import time
import sys
import json
import os.path
import csv
from copy import deepcopy
import pprint as pp

# sys.path.append('./Solver/DifferentSolver')
# from Backtracking_Appointments import backtrackingSearch
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


    hours = ["08.00", "08.50", "09.00", "09.50",
             "14.00", "14.50", "15.00", "15.50"]

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
    
    hours = ["08.00", "08.50", "09.00", "09.50", "10.00", "10.50", "11.00", "11.50", #pausa pranzo dalle 12.30 alle 13.00
             "14.00", "14.50", "15.00", "15.50", "16.00", "16.50", "17.00", "17.50"]
    
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

    
def printSolution(solution, appointments):
    days = ["mon", "tue", "wed", "thu", "fri"]

    ordApp = [[], [], [], [], [],]
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
        else:
            notSched.append([x, solution[x]])
    # print(ordApp)
    for x in ordApp:
        x.sort(key=takeSecond)

    print(ordApp)
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
    return ordApp, len(notSched)



def computeObjFunc(ordApp):
    #print(ordApp)
    travelTime = 0
    for x in ordApp:
        for y in range(len(x)-1):
            if ((float(x[y][1][1]) > 12 and float(x[y+1][1][1]) > 12) or (float(x[y][1][1]) < 12 and float(x[y+1][1][1]) < 12)):
                travelTime += float(x[y+1][1][1]) - float(x[y][1][1])-1
                #print("TravelTime = ",travelTime)        
    print("TravelTime = ",travelTime)        
    return travelTime


def get_key(key):
    try:
        return int(key)
    except ValueError:
        return key


def readyForJSON(solution, appointments):
    jsonSolution = {}

    orderedKeys = []
    for x in sorted(solution[0].items(), key=lambda t: get_key(t[0])):
        orderedKeys.append(x[0])

    print(orderedKeys)

    for x in orderedKeys:
        if solution[0][x] == "notScheduled":
            jsonObject = {
                "Status": "not scheduled",
                "Name": appointments[x]["Name"],
                "Surname": appointments[x]["Surname"],
                "House": appointments[x]["House"],
                "Day": appointments[x]["Day"],
            }

            print("not scheduled -- skipping: " + x)
            # print(jsonObject)
            jsonSolution[x] = jsonObject
        else:
            hour, minutes = solution[0][x][1].split(".")

            hourEnd = int(hour)
            hourEnd = hourEnd+1
            if hourEnd < 10:
                hourEnd = "0" + str(hourEnd)
            else:
                hourEnd = str(hourEnd)
            
            if minutes == "50":
                minutes = "30"

            jsonObject = {
                "Name": appointments[x]["Name"],
                "Surname": appointments[x]["Surname"],
                "House": solution[0][x][2],
                "Day": solution[0][x][0],
                "HourStart": hour + ":" + minutes,
                "HourEnd": hourEnd + ":" + minutes
            }

            jsonSolution[x] = jsonObject
    return jsonSolution



def solver(appointments, domain, timeout):
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
            #print(appointments[x])
            #print(appointments[x]["Day"])
            
            for a in appointments[x]["Day"]:
                if "Morning" == a[1] and hour < 12 and y[0] in a[0] and y[2] in appointments[x]["House"]:
                    dom.append(y)

                if "Afternoon" == a[1] and hour > 12 and y[0] in a[0] and y[2] in appointments[x]["House"]:
                    dom.append(y)
            
        ConstraintGraph.add_node(x, domain = deepcopy(dom))
        dom.append("notScheduled")
        #Aggiungo la variabile corrente con il domain aggiustato
    #    print(dom)
        ConstraintGraphCost.add_node(x, domain = dom)
        variablesName.append(x)

    # Add edges to the constraint graph only if the two variables share at least one element of the domain, it is possible to make this part better
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
                        stop = True
                        break

                        
                    

    ConstraintGraph.add_edges_from(itertools.combinations(variablesName, 2))

    #ConstraintGraphCost.add_edges_from(itertools.combinations(variablesName, 2))


    '''
    nx.draw(ConstraintGraph)
    ax = plt.gca()
    ax.collections[0].set_edgecolor("#ffffff")
    plt.show()
    
    # Graph with Custom nodes:
    nx.draw(ConstraintGraphCost, pos = nx.spring_layout(ConstraintGraphCost, k = 1.5, iterations=50), with_labels=True, node_size=500, node_color="skyblue", node_shape="o", alpha=0.75, linewidths=1.5, font_size=10, font_weight="bold", width=1, edge_color="lightgrey")
    #nx.draw(ConstraintGraphCost, pos = nx.spring_layout(ConstraintGraphCost, k = 1.5, iterations=50), with_labels=True, node_size=2000, node_color="skyblue", node_shape="o", alpha=0.75, linewidths=3, font_size=20, font_weight="bold", width=3, edge_color="lightgrey")


    #nx.draw(ConstraintGraphCost, pos=nx.spring_layout(ConstraintGraphCost, k=0.5, iterations=35))
    #ax = plt.gca()
    #ax.collections[0].set_edgecolor("#ffffff")
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
    # sol = backtrackingSearchAllSolutions(ConstraintGraphCost, 1000*60*0 + 1000*0 + 500 )# minutes * seconds * 1000
    sol = backtrackingSearchAllSolutions(ConstraintGraphCost, timeout)  # minutes * seconds * 1000
    end = current_milli_time()
    print("\n\n###########Time spent to find all solution = ", end-start," ms.\n\n")
    # print(sol[0])
    # printSolution(sol[0], appointments)
    # print("With cost = ", sol[1])

    return sol


# appointments = loadAppointments(sys.argv[1])
# #print(appointments)
# domain = initDomain()
# # print(domain)
# solution = solver(appointments, domain)
# readyForJSON(solution, appointments)

def scheduler(requestsPath, timeout):

    domain = initDomain()
    appointments = loadAppointments(requestsPath)
    solution = solver(appointments, domain, timeout)
    jsonSolution = readyForJSON(solution, appointments)

    # write solutions on file
    scheduledAppointmentsFile = "data/scheduledAppointments.json"

    with open(scheduledAppointmentsFile, 'w') as json_file:
        json.dump(jsonSolution, json_file, indent=4)
    return(solution, appointments)

if __name__ == "__main__":
    (sol, appointments) = scheduler(sys.argv[1], int(sys.argv[2]))
    print(sol[0])
    (ordBest, notsched) = printSolution(sol[0], appointments)
    obj = computeObjFunc(ordBest)
    print("With cost = ", sol[1])

if os.path.exists(sys.argv[3]) == False:
    length = sys.argv[1][-7:-5]
    index = sys.argv[1][-8:-7]
    print(sys.argv[1])
    print(length, index)
    row1 = ["SoftConstraints "+  length , index,1,10,30,60,180,600]
    row2 = ["", "traveltime"]
    row3 = ["", "percentage"]
    row4 = ["", "notsched"]
     
    lines=[row1,row2,row3,row4]
    with open(sys.argv[3], 'w') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerows(lines)
    writeFile.close()

with open(sys.argv[3], 'r') as readFile:
    reader = csv.reader(readFile)
    lines = list(reader)
lines[1].append(obj)
lines[2].append(sol[3])
lines[3].append(notsched)

with open(sys.argv[3], 'w') as writeFile:
    writer = csv.writer(writeFile)
    writer.writerows(lines)
readFile.close()
writeFile.close()


