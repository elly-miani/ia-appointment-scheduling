from copy import deepcopy
import pprint as pp
import time
import random


current_milli_time = lambda: int(round(time.time() * 1000))


def assCompleto(assegnamento,csp):
	'''
	Verifico se l'assegnamento è completo verificando se tutte le variabili del csp
	hanno un assegnamento
	'''
	return len(assegnamento)==len(csp.nodes())


def isSafe(v, var, assegnamento, csp):
	'''
	Verifico se l'assegnamento è consistente.
	'''
	#print("Verifico vincoli con i vicini alla variabile ", var, " con assegnato il valore ", v)
	for n in csp.neighbors(var):
		'''
		Per ogni vicino di var, verifico se ha già un assegnamento uguale a quello testato
		Qui è dove devo cercare di far rispettare i vincoli rispetto i vincoli con i vicini.
		valore che ho appena dato alla variabile var
		'''
		if n in assegnamento:
			y = assegnamento[n]

			#print("stampa assegnamento corrente ", y)

			isSameDay = v[0] == y[0]
			# va ancora aggiustato
			bothMorning = float(v[1]) <= 11.5 and float(y[1]) <= 11.5
			bothAfternoon = float(v[1]) > 12.0 and float(y[1]) > 12.0
			isSamePeriod = bothMorning or bothAfternoon
			isSameHouse = v[2] == y[2]

			timeBwAppointments = abs(float(v[1])-float(y[1]))
			distanceBwHouses = (distance(v[2], y[2])*0.5 + 1)
			cantReachInTime = (not isSameHouse and (timeBwAppointments < distanceBwHouses))
			avoidSameHouse = (isSameHouse and timeBwAppointments != 1)

			'''
			TODO: Check the new condition.
			'''
			
			if (isSameDay and isSamePeriod and (cantReachInTime or avoidSameHouse)):
				return (False, n)
	return (True, "-1")
	

def varNonAssegnata(assegnamento, csp, nearest):
	'''
	Restituisco la variabile del csp non assegnata che ha dominio più piccolo
	implementazione della euristica first fail.
	'''

	minimumLength = 10000
	chosenVar = "-1"
	if len(nearest)==0:
		list = csp.nodes()
	else:
		list = nearest

	for n in list:
		if n not in assegnamento and len(csp.nodes[n]['domain']) < minimumLength:
			chosenVar = n
			minimumLength = len(csp.nodes[n]['domain'])
	print("variabile scelta con dominio di dimensione = ", minimumLength)
	return chosenVar



def ordinaValori(var, assegnamento, csp):
	'''
	Restituisco tutti i valori del dominio di var che non sono assegnati
	'''
	list = deepcopy(csp.nodes[var]['domain'])
	# secondo me questo if non serve a nulla, non ci entro mai mi sembra
	if var in assegnamento:
		list.pop(list.index(assegnamento[var]))
	return list



"""
Funzione solver che viene chiamata dal programma principale
Per implementare il backjump è necessario tenere una lista delle variabili in
ordine che sono state assegnate
"""
def backtrackingSearch(csp):
	return backtracking({},[],csp,0)



def backtracking(assegnamento, assegnate, csp, iteration):
	'''
	Se l'assegnamento è completo mi fermo
	'''
	print("Iterazione numero = ", iteration, "\nAssegnamento corrente = ", assegnamento)
	iteration += 1

	if assCompleto(assegnamento, csp):
		return assegnamento

	var = varNonAssegnata(assegnamento, csp, [])
	conflictSet = []
	#print("Variabile scelta ", var)
	for v in ordinaValori(var, assegnamento, csp):
		(safe, conflict) = isSafe(v, var, assegnamento, csp)
		if safe:
			assegnamento[var] = v
			assegnate.append(var)
			assLength = len(assegnate)
			ris = backtracking(assegnamento, assegnate, csp, iteration)
			#Significa che è successo un backjump e sta tagliando il ramo attuale
			if assLength > len(assegnate)+1:
				return None
			if ris!=None:
				return ris
		else:
			conflictSet.append(conflict)
			# print("Conflict: " + conflict)
			# Se arrivo a questo punto sono sicuro di essere tornato alla radice
			# del sottoalbero che potevo analizzare e di non aver trovato una soluzione.

	backjump(assegnamento, assegnate, conflictSet, csp)
	return None

def backjump(assegnamento, assegnate, conflictSet, csp):
	assIndex = len(assegnate)-1
	print("\n\n####BACKJUMP####\n")
	print("AssIndex = ", assIndex, "\nAssegnamento = ", assegnamento, "\nAssegnate = ", assegnate, "\nConflictSet = ", conflictSet)
	#l'unica cosa che posso fare è una stima di quante ne salto... dovrei passare a che punto dello scorrere del dominio sono arrivato
	while( not(assegnate[assIndex] in conflictSet)):
		del(assegnamento[assegnate[assIndex]])
		del(assegnate[assIndex])
		assIndex -= 1
		#print("AssIndex = ", assIndex, "\nAssegnamento = ", assegnamento, "\nAssegnate = ", assegnate, "\nConflictSet = ", conflictSet)
	
	del(assegnamento[assegnate[assIndex]])
	del(assegnate[assIndex])
	#print("AssIndex = ", assIndex, "\nAssegnamento = ", assegnamento, "\nAssegnate = ", assegnate, "\nConflictSet = ", conflictSet)
	#print("\n####BACKJUMP_FINE####\n")
	

# è possibile già qui identificare se c'è un successivo e azzerargli il dominio tranne quello da utilizzare?
# per evitare il problema di avere appuntamenti che avrebbero potuto essere nella stessa casa, e nello stesso periodo,
# ma non sono stati scelti tengo in nearest quelli che hanno la possibilità di confinare e poi vado a sceglierli 
def deleteValues(v, var, assegnamento, newCSP):
	nearest = []
	print("Eliminio valori in conflitto con ", v)
	if v != "notScheduled":
		for n in newCSP.neighbors(var):
			if n not in assegnamento:
				print("Variabile non in assegnamento ", n)	
				newDom = []
				for y in newCSP.nodes[n]['domain']:
					if y != "notScheduled":
						isSameDay = v[0] == y[0]
						bothMorning = float(v[1]) <= 11.5 and float(y[1]) <= 11.5
						bothAfternoon = float(v[1]) > 12.0 and float(y[1]) > 12.0
						isSamePeriod = bothMorning or bothAfternoon
						isSameHouse = v[2] == y[2]
						timeBwAppointments = abs(float(v[1])-float(y[1]))
						distanceBwHouses = (distance(v[2], y[2])*0.5 + 1)
						cantReachInTime = timeBwAppointments < distanceBwHouses
						if not (isSameDay and isSamePeriod and (cantReachInTime)):
							if(timeBwAppointments == 1 and isSameHouse and isSameDay ):
								print("appuntamento precedente ", y, " rispetto a ", v)
								nearest.append(n)
							newDom.append(y)
						else:	
							print("rimuovo ", y, " dal dominio di", n)
				newDom.append("notScheduled")
				print("dominio rimanente = ", newDom,"\n")
				newCSP.nodes[n]['domain'] = newDom
	print("nearest ", nearest)
	return nearest


#devo considerare entrambi i casi, successivo e precedente

def ordinaValoriCost(var, assegnamento, csp):
	'''
	Restituisco tutti i valori del dominio di var che non sono assegnati
	'''
	#print("\n\n###########ordina valori################\n")
	ordDomain = []
	dom = deepcopy(csp.nodes[var]['domain'])
	#Bad idea!
	random.shuffle(dom)
	#print("Assegnamento ", assegnamento)
	#print("dom senza conflitti = ", dom)
	while(len(dom) > 0):
		bestValue = []
		bestValueCost = 1000
		for v in dom:
			#print("Considero attuale ", v)
			if v != "notScheduled":
				conflict = False
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
							if(isSameDay and isSamePeriod and float(v[1])-float(y[1]) < float(v[1])-float(previousAppointment[1])):
								previousAppointment = y
				#print("v ", v)
				#print("prev ",previousAppointment)
				#print("With distance = ", float(v[1])-float(previousAppointment[1]))
				#print("previous appointment per attuale = ",previousAppointment)
				# It does make sense to penalize the choice of a casual starting point if the current slot is free.
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
		dom.remove(bestValue)
	
		
		ordDomain.append((bestValue, bestValueCost))
		#print("dom = ", dom)
		#print("ordDomain = ", ordDomain)
		#print("\n\n###Fine analisi per massimo locale\nOrdDom = ", ordDomain)
		
	print("\n\n###Fine ordinamento per  = ",var, " ", ordDomain)
	
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
		numTotalSolution *= len(csp.nodes[n]['domain'])
		analyzed[n] = 0

	print("Total number of possible solution = ", numTotalSolution)
	"""
	IDEA: forse posso passare a btas un vettore [a,b,c,d] dove vedo a che ciclo e a che profondità sto
	"""
	endTime = current_milli_time() + maxTime
	return backtrackingAllSolutions({}, 1000000000, {}, 0, [], csp, [], 0, analyzed, numTotalSolution, endTime)


def backtrackingAllSolutions(solution, bestSolCost , assegnamento, currCost, assegnate, csp, nearest, iteration, analyzed, numTotalSolution, endTime):
	'''
	Se l'assegnamento è completo mi fermo
	'''
	print("\n\n\nIteration = ", iteration)
	iteration += 1
	if(current_milli_time() > endTime):
		print("\n\n######TEMPO SCADUTO!!!#####\n\nIterazione numero = ", iteration,"\nAnalyzed= ", analyzed, "\nPercentuale albero analizzata = ", (computeVisited(analyzed, assegnate, csp)/numTotalSolution*100), " \nAssegnamento corrente = ", assegnamento)
		return (solution, bestSolCost, "END")

	
	if assCompleto(assegnamento, csp):
		#Devo anche fare in modo di visitare la vicina soluzione probabilmente
		#basta cancellare il valore dell'ultima variabile dall'assegnamento
		if currCost <= bestSolCost:
			solution = (deepcopy(assegnamento))
			bestSolCost = currCost
			print("\n\n######################### Cambio soluzione #########################\n\n")
			print(solution)
			print("Che ha costo = ", currCost)
		return (solution, bestSolCost, "found")

	var = varNonAssegnata(assegnamento, csp, nearest)
	analyzed[var] = 0
	
	print("Variabile scelta ", var)
	orderedDomain = ordinaValoriCost(var, assegnamento, csp)
	for v in orderedDomain:
		newCSP = deepcopy(csp)
		nearest = deleteValues(v[0], var, assegnamento, newCSP)
		print(var," = ",v)
		iterationCost = currCost + v[1]
		print("currentCost = ", iterationCost)
		if iterationCost < bestSolCost:
			print("Assegno alla variabile " + str(var) + " il valore " + str(v))
			assegnamento[var] = v[0]
			print("\n\n#####Settimana attualmente schedulata#####")
			printSolution(assegnamento)
			assegnate.append(var)
			(solution, bestSolCost, ris) = backtrackingAllSolutions(solution, bestSolCost, assegnamento, iterationCost, assegnate, newCSP, nearest, iteration, analyzed, numTotalSolution, endTime)
			print("\nRiprendo all'iterazione ", iteration-1, " Sto considerando la variabile ", var)
			if ris=="END":
				return (solution, bestSolCost, "END")
			analyzed[var] += 1
			if ris=="found":
				print("Ho appena trovato una soluzione")
				print("Analyzed= ", analyzed, "\nPercentuale albero analizzata = ", (computeVisited(analyzed, assegnate, csp)/numTotalSolution*100), " \nAssegnamento corrente = ", assegnamento)
				del(assegnamento[assegnate[-1]])
				del(assegnate[-1])
			if ris == "finished":
				print("Ho appena finito di controllare le soluzioni del sottoalbero", "\nAnalyzed= ", analyzed, "\nPercentuale albero analizzata = ", (computeVisited(analyzed, assegnate, csp)/numTotalSolution*100), " \nAssegnamento corrente = ", assegnamento)
				# non si può fare sempre?
				if len(assegnate) > 0:
					del(assegnamento[assegnate[-1]])
					del(assegnate[-1])
		else:
			#qui potrei anche fare un break tanto i valori del dominio sono già organizzati in base alla funzione di costo: se non va il primo non vanno neanche quelli dopo...
			analyzed[var] += 1
			break
# esco da qui solo se tutti i cicli del for sono finiti e ho trovato almeno una soluzione nel frattempo
	print("Esco da albero", "\nAnalyzed= ", analyzed, "\nPercentuale albero analizzata = ", (computeVisited(analyzed, assegnate, csp)/numTotalSolution*100), " \nAssegnamento corrente = ", assegnamento)
	analyzed[var] = 0
	return (solution, bestSolCost, "finished")





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
	print("Total = ", total)
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
