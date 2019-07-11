from copy import deepcopy
import pprint as pp
import time
import random

current_milli_time = lambda: int(round(time.time() * 1000))

def assCompleto(assegnamento,csp):
	return len(assegnamento)==len(csp.nodes())

def varNonAssegnata(assegnamento, csp, nearest):
	minimumLength = 10000
	chosenVar = "-1"
	list = csp.nodes()
	for n in list:
		if n not in assegnamento and len(csp.nodes[n]['domain']) < minimumLength:
			chosenVar = n
			minimumLength = len(csp.nodes[n]['domain'])
	return chosenVar

def ordinaValoriCost(var, assegnamento, csp):
	'''
	Restituisco tutti i valori del dominio di var che non sono assegnati
	'''
	ordDomain = []
	dom = deepcopy(csp.nodes[var]['domain'])
	while(len(dom) > 0):
		bestValue = []
		bestValueCost = 10000
		for v in dom:
			if v != "notScheduled":
				conflict = False
				usable = True
				previousAppointment = ['', '0', '']
				for n in csp.neighbors(var):
					# skip the following iterations because the value is in conflict with at least one assigned variable
					if(conflict==False):
						'''
						Devo trovare l'appuntamento precedente a quello che sto provando ad assegnare.
						'''
						if n in assegnamento and assegnamento[n] != "notScheduled":
							y = assegnamento[n]
							isSameDay = v[0] == y[0]
							bothMorning = float(v[1]) <= 11.5 and float(y[1]) <= 11.5
							bothAfternoon = float(v[1]) > 12.0 and float(y[1]) > 12.0
							isSamePeriod = bothMorning or bothAfternoon
							isSameHouse = v[2] == y[2]
							timeBwAppointments = abs(float(v[1])-float(y[1]))
							distanceBwHouses = (distance(v[2], y[2])*0.5 + 1)
							cantReachInTime = timeBwAppointments < distanceBwHouses
							# Case in which there is an overlapping with an appointment already scheduled
							if (isSameDay and isSamePeriod and (cantReachInTime)):
								if bestValueCost == 10000:
									bestValue = v
								usable = False
								break
							if(isSameDay and isSamePeriod and float(v[1])-float(y[1]) < float(v[1])-float(previousAppointment[1])):
								previousAppointment = y
				if usable:
					if previousAppointment[1] == '0' and (v[1] == "08.00" or v[1] == "14.00")  and bestValueCost > 0.5:
						bestValueCost = 0.5
						bestValue = v
					else:
						if previousAppointment[1] == '0' and bestValueCost > 15:
							bestValueCost = 15
							bestValue = v
						else:
							if(bestValueCost > ((float(v[1])-float(previousAppointment[1])-1)/0.5)*((float(v[1])-float(previousAppointment[1])-1)/0.5)):
								bestValueCost = ((float(v[1])-float(previousAppointment[1])-1)/0.5)*((float(v[1])-float(previousAppointment[1])-1)/0.5)
								bestValue = v
					#print("Attuale best = ", bestValue, " Con costo " , bestValueCost)
			else:
				if (bestValueCost > 10):
					bestValue = "notScheduled"
					bestValueCost = 10
		#print(bestValue)
		dom.remove(bestValue)
		ordDomain.append((bestValue, bestValueCost))
	print("ordDomain = ", ordDomain)
	return ordDomain


"""
Funzione solver che viene chiamata dal programma principale
Per implementare il backjump è necessario tenere una lista delle variabili in
ordine che sono state assegnate
"""
def backtrackingSearchAllSolutions(csp, maxTime):
	numTotalSolution = 1
	analyzed = {}
	for n in csp.nodes():
		print("variabile ", n, " Dominio lungo ", len(csp.nodes[n]['domain']))
		numTotalSolution *= len(csp.nodes[n]['domain'])
		analyzed[n] = 0

	print("Total number of possible solution = ", numTotalSolution)
	"""
	IDEA: forse posso passare a btas un vettore [a,b,c,d] dove vedo a che ciclo e a che profondità sto
	"""
	endTime = current_milli_time() + maxTime
	return backtrackingAllSolutions({}, 1000000000, 100, {}, 0, [], csp, [], 0, analyzed, numTotalSolution, endTime)


def backtrackingAllSolutions(solution, bestSolCost, unsched, assegnamento, currCost, currUnsched, assegnate, csp, nearest, recDepth, analyzed, numTotalSolution, endTime):
	'''
	Se l'assegnamento è completo mi fermo
	'''
	#print("\n\n\nRecursion Depth = ", recDepth)
	recDepth += 1
	if(current_milli_time() > endTime):
		percentage = (computeVisited(analyzed, assegnate, csp)/numTotalSolution*100)
		print("\n\n######TEMPO SCADUTO!!!#####\n\nIterazione numero = ", recDepth,"\nAnalyzed= ", analyzed, "\nPercentuale albero analizzata = ", (computeVisited(analyzed, assegnate, csp)/numTotalSolution*100), " \nAssegnamento corrente = ", assegnamento)
		return (solution, bestSolCost, "END", percentage)

	if assCompleto(assegnamento, csp):
		#Devo anche fare in modo di visitare la vicina soluzione probabilmente
		#basta cancellare il valore dell'ultima variabile dall'assegnamento
		if currUnsched<unsched or (currUnsched == unsched and currCost <= bestSolCost):
			solution = (deepcopy(assegnamento))
			bestSolCost = currCost
			unsched = currUnsched
			print("\n\n######################### Cambio soluzione #########################\n\n")
			print(solution)
			print("Che ha costo = ", currCost)
			# anche in questo caso devo eliminare le variabili assegnate, devo riprendere nel ciclo e devo risettare la stessa variabile!
		return (solution, bestSolCost, "found",0)

	var = varNonAssegnata(assegnamento, csp, nearest)
	# voglio spostarlo dopo, all'uscita
	analyzed[var] = 0

	#print("Variabile scelta ", var)
	orderedDomain = ordinaValoriCost(var, assegnamento, csp)
	ciclo = 0
	for v in orderedDomain:
		ciclo+=1
		assegnamento[var] = v[0]
		assegnate.append(var)
		iterationCost = currCost + v[1]
		iterationUnsched = currUnsched + v[2]
		if iterationCost < bestSolCost:
			(solution, bestSolCost, ris, per) = backtrackingAllSolutions(solution, bestSolCost, assegnamento, iterationCost, assegnate, csp, nearest, recDepth, analyzed, numTotalSolution, endTime)

			#print("\n##### Riprendo, Profondità ricorsione = ", recDepth-1, " Ciclo numero: ", ciclo, " Sto considerando la variabile ", var)
			if ris=="END":
				return (solution, bestSolCost, "END", per)
			analyzed[var] += 1
			if ris=="found":
				#print("Ho appena trovato una soluzione")
				#print("Analyzed= ", analyzed, "\nPercentuale albero analizzata = ", (computeVisited(analyzed, assegnate, csp)/numTotalSolution*100), " \nAssegnamento corrente = ", assegnamento)
				#print("Percentuale albero analizzata = ", (computeVisited(analyzed, assegnate, csp)/numTotalSolution*100))
				# se sono qui significa che ho finito di analizzare il sotto albero e devo sostituire la variabile che sto considerando.
				del(assegnamento[assegnate[-1]])
				del(assegnate[-1])
				# qui potrei anche uscire direttamente, tanto andando avanti troverei solo soluzioni peggiori...
			if ris == "finished":
				#print("Ho appena finito di controllare le soluzioni del sottoalbero", "\nAnalyzed= ", analyzed, "\nPercentuale albero analizzata = ", (computeVisited(analyzed, assegnate, csp)/numTotalSolution*100), " \nAssegnamento corrente = ", assegnamento)
				#print("Percentuale albero analizzata = ", (computeVisited(analyzed, assegnate, csp)/numTotalSolution*100))
				if len(assegnate) > 0:
					del(assegnamento[assegnate[-1]])
					del(assegnate[-1])
		else:
			print(assegnamento)
			printSolution(assegnamento)
			print("With iteration cost = ", iterationCost)
			# qui potrei anche fare un break tanto i valori del dominio sono già organizzati in base alla funzione di costo: se non va il primo non vanno neanche quelli dopo...
			#print("Tutti i possibili valori successivi peggiorano la funzione di costo.")
			analyzed[var] = len(csp.nodes[var]['domain'])
			#print("Esco da albero", "\nAnalyzed= ", analyzed, "\nPercentuale albero analizzata = ", (computeVisited(analyzed, assegnate, csp)/numTotalSolution*100), " \nAssegnamento corrente = ", assegnamento, "\nAssegnate = ", assegnate)
			#print("Percentuale albero analizzata = ", (computeVisited(analyzed, assegnate, csp)/numTotalSolution*100))
			if len(assegnate) > 0:
				del(assegnamento[assegnate[-1]])
				del(assegnate[-1])
			break

# esco da qui solo se tutti i cicli del for sono finiti e ho trovato almeno una soluzione nel frattempo
	analyzed[var] = 0
	return (solution, bestSolCost, "finished", 100)



def computeVisited(analyzed, assegnate, csp):
	total = 0
	passed = []
	#print("\n\n###computeVisited", "\nAssegnate = ", assegnate)
	#print("analyzed = ", analyzed)
	for i in assegnate:
		partial = analyzed[i]
		passed.append(i)
		for k in csp.nodes():
			if k not in passed:
				partial *= len(csp.nodes[k]['domain'])

		#print("variabile ", i, "Contributo = ", partial)
		total += partial
		'''
		if i in assegnate:
			print("moltiplico per ", analyzed[i])
			total *= analyzed[i]
		else:
			print("moltiplico per ", len(csp.nodes[i]['domain']))
			total *= len(csp.nodes[i]['domain'])
		'''
	#print("Total visited = ", total)
	return total



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
        if len(x)!=0:
            print("\n\nGiorno: ", days[index])
            print("\nMattina:")
            cond = True
            for y in x:
                if (cond and float(y[1][1]) > 12):
                    print("\nPomeriggio:")
                    cond = False
                print("Ore: ", y[1][1], "Casa: ", y[1][2], " Appuntamento numero: ", y[0])
        index += 1
    print(notSched)


def takeSecond(elem):
    return elem[1]
