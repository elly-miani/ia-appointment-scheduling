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


def varNonAssegnata(assegnamento, csp, nearest):
	'''
	Restituisco la variabile del csp non assegnata che ha dominio più piccolo
	implementazione della euristica first fail o quella che potrebbe essere assegnata più vicina.
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
	#print("variabile scelta con dominio di dimensione = ", minimumLength)
	return chosenVar

"""
Implementation of forward checking
"""
def deleteValues(v, var, assegnamento, newCSP):
	nearest = []
	#print("\nEliminio valori in conflitto con ", v)
	if v != "notScheduled":
		for n in newCSP.neighbors(var):
			if n not in assegnamento:
				#print("Variabile non in assegnamento ", n)	
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
								#print("appuntamento precedente ", y, " rispetto a ", v)
								nearest.append(n)
							newDom.append(y)
						#else:	
							#print("rimuovo ", y, " dal dominio di", n)
				newDom.append("notScheduled")
				#print("dominio rimanente = ", newDom,"\n")
				newCSP.nodes[n]['domain'] = newDom
	#print("nearest ", nearest)
	return nearest


def ordinaValoriCost(var, assegnamento, csp):
	'''
	Restituisco tutti i valori del dominio di var che non sono assegnati ordinandoli in base all'assegnamento corrente
	'''
	#print("\n\n###########ordina valori################\n")
	ordDomain = []
	dom = deepcopy(csp.nodes[var]['domain'])
	#Bad idea!
	#random.shuffle(dom)
	#print("Assegnamento ", assegnamento)
	#print("dom senza conflitti = ", dom)
	while(len(dom) > 0):
		bestValue = []
		bestValueCost = 10000
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
		
	#print("\n\n###Fine ordinamento per  = ",var, " ", ordDomain)
	
	return ordDomain


"""
Branch and bound
"""
def branchAndBoundSearch(csp, maxTime):
	numTotalSolution = 1
	analyzed = {}
	for n in csp.nodes():
		print("variabile ", n, " Dominio lungo ", len(csp.nodes[n]['domain']))
		numTotalSolution *= len(csp.nodes[n]['domain'])
		analyzed[n] = 0

	print("Total number of possible solution = ", numTotalSolution)
	endTime = current_milli_time() + maxTime
	return branchAndBound({}, 1000000000, {}, 0, [], csp, csp, [], 0, analyzed, numTotalSolution, endTime)


def branchAndBound(solution, bestSolCost , assegnamento, currCost, assegnate, csp, updatedCSP, nearest, recDepth, analyzed, numTotalSolution, endTime):
	'''
	Se l'assegnamento è completo mi fermo
	'''
	#print("\n\n\nRecursion Depth = ", recDepth)
	recDepth += 1
	if(current_milli_time() > endTime):
		print("\n\n######TEMPO SCADUTO!!!#####\n\nIterazione numero = ", recDepth,"\nAnalyzed= ", analyzed, "\nPercentuale albero analizzata = ", (computeVisited(analyzed, assegnate, csp)/numTotalSolution*100), " \nAssegnamento corrente = ", assegnamento)
		return (solution, bestSolCost, "END")
	
	if assCompleto(assegnamento, updatedCSP):
		#Devo anche fare in modo di visitare la vicina soluzione probabilmente
		#basta cancellare il valore dell'ultima variabile dall'assegnamento
		if currCost <= bestSolCost:
			solution = (deepcopy(assegnamento))
			bestSolCost = currCost
			print("\n\n######################### Cambio soluzione #########################\n\n")
			print(solution)
			print("Che ha costo = ", currCost)
		return (solution, bestSolCost, "found")

	var = varNonAssegnata(assegnamento, updatedCSP, nearest)
	analyzed[var] = 0
	
	orderedDomain = ordinaValoriCost(var, assegnamento, updatedCSP)
	ciclo = 0
	for v in orderedDomain:
		#print("##### Profondità ricorsione = ", recDepth-1, " Ciclo numero: ", ciclo, " Sto considerando la variabile ", var)
		ciclo+=1
		newCSP = deepcopy(updatedCSP)
		nearest = deleteValues(v[0], var, assegnamento, newCSP)
		assegnamento[var] = v[0]		
		assegnate.append(var)
		iterationCost = currCost + v[1]
		if iterationCost < bestSolCost:
			(solution, bestSolCost, ris) = branchAndBound(solution, bestSolCost, assegnamento, iterationCost, assegnate, csp, newCSP, nearest, recDepth, analyzed, numTotalSolution, endTime)
			#print("\n##### Riprendo, Profondità ricorsione = ", recDepth-1, " Ciclo numero: ", ciclo, " Sto considerando la variabile ", var)
			if ris=="END":
				return (solution, bestSolCost, "END")
			analyzed[var] += 1
			if ris=="found":
				#print("Percentuale albero analizzata = ", (computeVisited(analyzed, assegnate, csp)/numTotalSolution*100))
				del(assegnamento[assegnate[-1]])
				del(assegnate[-1])
			if ris == "finished":
				#print("Percentuale albero analizzata = ", (computeVisited(analyzed, assegnate, csp)/numTotalSolution*100))
				if len(assegnate) > 0:
					del(assegnamento[assegnate[-1]])
					del(assegnate[-1])
		else:
			analyzed[var] = len(csp.nodes[var]['domain'])
			#print("Percentuale albero analizzata = ", (computeVisited(analyzed, assegnate, csp)/numTotalSolution*100))
			if len(assegnate) > 0:
				del(assegnamento[assegnate[-1]])
				del(assegnate[-1])
			break

	analyzed[var] = 0
	return (solution, bestSolCost, "finished")


"""
Function that returns the number of assignment that are already been analyzed
"""
def computeVisited(analyzed, assegnate, csp):
	total = 0
	passed = []
	for i in assegnate:
		partial = analyzed[i]
		passed.append(i)
		for k in csp.nodes():
			if k not in passed:
				partial *= len(csp.nodes[k]['domain'])
		
		total += partial
	return total


"""
Function that returns the distance between two locations
"""
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