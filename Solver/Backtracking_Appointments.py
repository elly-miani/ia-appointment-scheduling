from copy import deepcopy
import pprint as pp


def assCompleto(assegnamento,csp):
	'''
	Verifico se l'assegnamento è completo verificando se tutte le variabili del csp
	hanno un assegnamento
	'''
	return len(assegnamento)==len(csp.nodes())


def isSafeAllSolutions(v, var, assegnamento, csp, analyzed):
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
			# notEnoughTime = (timeBwAppointments < distanceBwHouses)

			if (isSameDay and isSamePeriod and (cantReachInTime or avoidSameHouse)):
				
				numCutSolutions = 1
				print(csp.nodes())
				for k in csp.nodes():
					if k not in assegnamento and k != var:
						numCutSolutions *= len(csp.nodes[k]['domain'])
				analyzed += numCutSolutions
				print("####Pruning#### analizzate altre soluzioni : ", numCutSolutions )
				
				return (False, n, analyzed)
	return (True, "-1", analyzed)


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



def varNonAssegnata(assegnamento, csp):
	'''
	Restituisco la variabile del csp non assegnata che ha dominio più piccolo
	implementazione della euristica first fail.
	'''

	minimumLength = 10000
	chosenVar = "-1"
	for n in csp.nodes():
		if n not in assegnamento and len(csp.nodes[n]['domain']) < minimumLength:
			chosenVar = n

	'''
	Restituisco la prima variabile del csp che non compare nell'assegnamento
	for n in csp.nodes():
	'''
	# if n not in assegnamento:
	# 	print(type(n))
	# 	return n
	return chosenVar



def ordinaValori(var, assegnamento, csp):
	'''
	Restituisco tutti i valori del dominio di var che non sono assegnati
	'''
	list = deepcopy(csp.nodes[var]['domain'])
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

	var = varNonAssegnata(assegnamento, csp)
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

	backjump(assegnamento, assegnate, conflictSet)
	return None



"""
Funzione solver che viene chiamata dal programma principale
Per implementare il backjump è necessario tenere una lista delle variabili in
ordine che sono state assegnate
"""
def backtrackingSearchAllSolutions(csp):
	numTotalSolution = 1
	for n in csp.nodes():
		numTotalSolution *= len(csp.nodes[n]['domain'])
	print("Total number of possible solution = ", numTotalSolution)
	"""
	IDEA: forse posso passare a btas un vettore [a,b,c,d] dove vedo a che ciclo e a che profondità sto
	"""
	return backtrackingAllSolutions([],{},[],csp,0, 0, numTotalSolution)[0]


def backtrackingAllSolutions(solutions, assegnamento, assegnate, csp, iteration, analyzed, numTotalSolution):
	'''
	Se l'assegnamento è completo mi fermo
	'''
	print("Iterazione numero = ", iteration, "Percentuale albero analizzata = ", (analyzed/numTotalSolution*100), " \nAssegnamento corrente = ", assegnamento)
	iteration += 1

	if assCompleto(assegnamento, csp):
		#Devo anche fare in modo di visitare la vicina soluzione probabilmente
		#basta cancellare il valore dell'ultima variabile dall'assegnamento
		solutions.append(deepcopy(assegnamento))
		analyzed+=1
		#print("Assegnamento prima del ")
		#pp.pprint(assegnamento)
		del(assegnamento[assegnate[-1]])
		del(assegnate[-1])
		#print("Assegnamento dopo del ")
		#pp.pprint(assegnamento)
		print("\n\n######################### SOLUZIONE NUMERO ", len(solutions), " #########################\n\n")
		print(solutions[-1])
		print("assegnate = ", assegnate,"\n\n")

		return (solutions, None, analyzed)

	var = varNonAssegnata(assegnamento, csp)
	conflictSet = []
	#print("Variabile scelta ", var)
	for v in ordinaValori(var, assegnamento, csp):
		(safe, conflict, analyzed) = isSafeAllSolutions(v, var, assegnamento, csp, analyzed)
		if safe:
			assegnamento[var] = v
			assegnate.append(var)
			assLength = len(assegnate)
			(sol, ris, analyzed) = backtrackingAllSolutions(solutions, assegnamento, assegnate, csp, iteration, analyzed, numTotalSolution)
			#Significa che è successo un backjump e sta tagliando il ramo attuale
			if assLength > len(assegnate) + 1:
				print("Exit here")
				return (sol, None, analyzed)
			'''if ris!=None:
				return (sol, ris)
			'''
		else:
			conflictSet.append(conflict)
			# print("Conflict: " + conflict)
			# Se arrivo a questo punto sono sicuro di essere tornato alla radice
			# del sottoalbero che potevo analizzare e di non aver trovato una soluzione.

	if len(conflictSet) != 0:
		analyzed = backjump(assegnamento, assegnate, conflictSet, analyzed, csp)
	else:
		if len(assegnate) > 0:
			del(assegnate[-1])

	print("Iterazione numero = ", iteration, "Percentuale albero analizzata = ", (analyzed/numTotalSolution*100), " \nAssegnamento corrente = ", assegnamento)
	return (solutions, None, analyzed)


def backjump(assegnamento, assegnate, conflictSet, analyzed, csp):
	assIndex = len(assegnate)-1
	print("\n\n####BACKJUMP####\n")
	print("AssIndex = ", assIndex, "\nAssegnamento = ", assegnamento, "\nAssegnate = ", assegnate, "\nConflictSet = ", conflictSet)
	#l'unica cosa che posso fare è una stima di quante ne salto... dovrei passare a che punto dello scorrere del dominio sono arrivato
	skipped = 1
	while( not(assegnate[assIndex] in conflictSet)):
		controlled = 0
		for x in csp.nodes[assegnate[assIndex]]['domain']:
			controlled += 0
		skipped *= (len(csp.nodes[assegnate[assIndex]]['domain'])-controlled) 
		del(assegnamento[assegnate[assIndex]])
		del(assegnate[assIndex])
		assIndex -= 1
		#print("AssIndex = ", assIndex, "\nAssegnamento = ", assegnamento, "\nAssegnate = ", assegnate, "\nConflictSet = ", conflictSet)
	
	analyzed+=skipped
	print("Soluzioni skippate= ", skipped)
	# Per questo non devo considerare rami tagliati perché riparto proprio da lì
	del(assegnamento[assegnate[assIndex]])
	del(assegnate[assIndex])
	#print("AssIndex = ", assIndex, "\nAssegnamento = ", assegnamento, "\nAssegnate = ", assegnate, "\nConflictSet = ", conflictSet)
	#print("\n####BACKJUMP_FINE####\n")
	return analyzed







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
