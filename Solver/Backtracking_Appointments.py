
from copy import deepcopy

def assCompleto(assegnamento,csp):
	'''
	Verifico se l'assegnamento è completo verificando se tutte le variabili del csp
	hannoo un assegnamento
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
			if (v[0] == y[0] and ((v[2] != y[2] and abs(float(v[1])-float(y[1])) < distance(v[2], y[2])*0.5 + 1) or (v[2] == y[2] and abs(float(v[1])-float(y[1])) != 1))):
				return False
	return True


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
	return chosenVar

	'''
	Restituisco la prima variabile del csp che non compare nell'assegnamento
	'''
	''''
	for n in csp.nodes():
		if n not in assegnamento:
			print(type(n))
			return n
	'''

def ordinaValori(var,assegnamento,csp):
	'''
	Restituisco tutti i valori del dominio di var che non sono assegnati
	'''
	list=deepcopy(csp.nodes[var]['domain'])
	if var in assegnamento:
		list.pop(list.index(assegnamento[var]))
	return list

def backtrackingSearch(csp):
	return backtracking({},csp)

def backtracking(assegnamento, csp):
	'''
	Se l'assegnamentp è completo mi fermo
	'''
	if assCompleto(assegnamento, csp):
		return assegnamento

	var=varNonAssegnata(assegnamento, csp)

	for v in ordinaValori(var,assegnamento,csp):
		if isSafe(v, var, assegnamento, csp):
			assegnamento[var]=v

			ris=backtracking(assegnamento,csp)
			if ris!=None:
				return ris

			del(assegnamento[var])

	return None


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
