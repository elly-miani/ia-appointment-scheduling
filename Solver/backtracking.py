
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
	for n in csp.neighbors(var):
		'''
		Per ogni vicino di var, verifico se ha già un assegnamento uguale a quello testato
		'''
		if n in assegnamento and assegnamento[n]==v:
			return False
	return True

def varNonAsssegnata(assegnamento, csp):
	'''
	Restituisco la prima variabile del csp che non compare nell'assegnamento
	'''
	for n in csp.nodes():
		if n not in assegnamento:
			return n

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

	var=varNonAsssegnata(assegnamento, csp)

	for v in ordinaValori(var,assegnamento,csp):
		if isSafe(v, var, assegnamento, csp):
			assegnamento[var]=v

			ris=backtracking(assegnamento,csp)
			if ris!=None:
				return ris

			del(assegnamento[var])

	return None
