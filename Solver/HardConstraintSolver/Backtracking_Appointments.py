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

def varNonAssegnata(assegnamento, csp):
	minimumLength = 10000
	list = csp.nodes()
	for n in list:
		if n not in assegnamento and len(csp.nodes[n]['domain']) < minimumLength:
			chosenVar = n
			minimumLength = len(csp.nodes[n]['domain'])
	return chosenVar



# è possibile già qui identificare se c'è un successivo e azzerargli il dominio tranne quello da utilizzare?
# per evitare il problema di avere appuntamenti che avrebbero potuto essere nella stessa casa, e nello stesso periodo,
# ma non sono stati scelti tengo in nearest quelli che hanno la possibilità di confinare e poi vado a sceglierli 
def deleteValues(v, var, assegnamento, newCSP):
	#print("\nEliminio valori in conflitto con ", v)
	for n in newCSP.neighbors(var):
		if n not in assegnamento:
			#print("Variabile non in assegnamento ", n)	
			newDom = []
			for y in newCSP.nodes[n]['domain']:
				isSameDay = v[0] == y[0]
				bothMorning = float(v[1]) <= 11.5 and float(y[1]) <= 11.5
				bothAfternoon = float(v[1]) > 12.0 and float(y[1]) > 12.0
				isSamePeriod = bothMorning or bothAfternoon
				isSameHouse = v[2] == y[2]
				timeBwAppointments = abs(float(v[1])-float(y[1]))
				distanceBwHouses = (distance(v[2], y[2])*0.5 + 1)
				cantReachInTime = timeBwAppointments < distanceBwHouses
				if not (isSameDay and isSamePeriod and (cantReachInTime)):
					newDom.append(y)
			newCSP.nodes[n]['domain'] = newDom
			if len(newDom)==0:
				return False
	return True




def ordinaValoriCost(var, assegnamento, csp):
	'''
	Restituisco tutti i valori del dominio di var che non sono assegnati
	'''
	dom = deepcopy(csp.nodes[var]['domain'])
	#Bad idea!
	random.shuffle(dom)
	return dom


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
	endTime = current_milli_time() + maxTime
	return backtrackingAllSolutions([], {}, [], csp, csp, 0, analyzed, numTotalSolution, endTime)



def backtrackingAllSolutions(solutions, assegnamento, assegnate, csp, updatedCSP, recDepth, analyzed, numTotalSolution, endTime):
	
	#print("\n\n\nRecursion Depth = ", recDepth)
	recDepth += 1
	if(current_milli_time() > endTime):
		print("\n\n######TEMPO SCADUTO!!!#####\n\nIterazione numero = ", recDepth,"\nAnalyzed= ", analyzed, "\nPercentuale albero analizzata = ", (computeVisited(analyzed, assegnate, csp)/numTotalSolution*100), " \nAssegnamento corrente = ", assegnamento)
		return (solutions, "END")
	
	if assCompleto(assegnamento, updatedCSP):
		solutions.append(deepcopy(assegnamento))
		return (solutions, "found")

	var = varNonAssegnata(assegnamento, updatedCSP)
	analyzed[var] = 0
	
	#print("Variabile scelta ", var)
	orderedDomain = ordinaValoriCost(var, assegnamento, updatedCSP)
	ciclo = 0
	for v in orderedDomain:
		#print("##### Profondità ricorsione = ", recDepth-1, " Ciclo numero: ", ciclo, " Sto considerando la variabile ", var)
		ciclo+=1
		# duplico grafo dei vincoli in modo da modificare i domini delle variabili solo nel sotto albero 
		# incrementalmente
		newCSP = deepcopy(updatedCSP)
		# cancello i valori dei domini delle variabili che non soddisfano i vincoli hard (non posso avere 
		# sovrapposizione tra appuntamenti)
		# Inoltre calcolo contemporaneamente se c'è qualche appuntamento che potrebbe essere pianificato nello slot 
		# immediatamente successivo
		keepGoing = deleteValues(v, var, assegnamento, newCSP)
		#print(var," = ",v)
		# aggiorno l'assegnamento corrente e la lista di variabili attualmente assegnate
		#print("Assegno alla variabile " + str(var) + " il valore " + str(v))
		assegnamento[var] = v		
		#print("Aggiungo ad assegnate la variabile ", var)
		assegnate.append(var)
		# Calcolo della funzione di costo per il valore della variabile scelto nella iterazione corrente
		#print("Costo dell'attuale assegnamento parziale = ", iterationCost)
		# Controllo se è possibile tagliare il ramo corrente, se già il costo dell'assegnamento parziale
		# è più alto della soluzione precedentemente trovata non ha senso proseguire. 
		# Se è possibile trovare una soluzione migliore chiamo ricorsivamente la stessa
		# funzione che assegnerà una nuova variabile
		if keepGoing:
			(solutions, ris) = backtrackingAllSolutions(solutions, assegnamento, assegnate, csp, newCSP, recDepth, analyzed, numTotalSolution, endTime)
			
			#print("\n##### Riprendo, Profondità ricorsione = ", recDepth-1, " Ciclo numero: ", ciclo, " Sto considerando la variabile ", var)
			if ris=="END":
				return (solutions, "END")
			analyzed[var] += 1
			if ris=="found":
				print("Percentuale albero analizzata = ", (computeVisited(analyzed, assegnate, csp)/numTotalSolution*100))
				# se sono qui significa che ho finito di analizzare il sotto albero e devo sostituire la variabile che sto considerando.
				del(assegnamento[assegnate[-1]])
				del(assegnate[-1])
				# qui potrei anche uscire direttamente, tanto andando avanti troverei solo soluzioni peggiori...
			if ris == "finished":
				#print("Ho appena finito di controllare le soluzioni del sottoalbero", "\nAnalyzed= ", analyzed, "\nPercentuale albero analizzata = ", (computeVisited(analyzed, assegnate, csp)/numTotalSolution*100), " \nAssegnamento corrente = ", assegnamento)
				print("Percentuale albero analizzata = ", (computeVisited(analyzed, assegnate, csp)/numTotalSolution*100))
				if len(assegnate) > 0:
					del(assegnamento[assegnate[-1]])
					del(assegnate[-1])
		else:
			# qui potrei anche fare un break tanto i valori del dominio sono già organizzati in base alla funzione di costo: se non va il primo non vanno neanche quelli dopo...
			#print("Tutti i possibili valori successivi peggiorano la funzione di costo.")
			analyzed[var] = len(csp.nodes[var]['domain'])
			#print("Esco da albero", "\nAnalyzed= ", analyzed, "\nPercentuale albero analizzata = ", (computeVisited(analyzed, assegnate, csp)/numTotalSolution*100), " \nAssegnamento corrente = ", assegnamento, "\nAssegnate = ", assegnate)
			print("Percentuale albero analizzata = ", (computeVisited(analyzed, assegnate, csp)/numTotalSolution*100))
			if len(assegnate) > 0:
				del(assegnamento[assegnate[-1]])
				del(assegnate[-1])
			break

# esco da qui solo se tutti i cicli del for sono finiti e ho trovato almeno una soluzione nel frattempo
	analyzed[var] = 0
	return (solutions, "finished")



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
