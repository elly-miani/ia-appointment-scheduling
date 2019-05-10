## To make request from terminal

`$pip3 install httpie`

`http http://127.0.0.1:8000`



La data di inizio del job 3 >= 5 gg + inizio job 1

# Questions

## `Solver.py`

- Why are some hours at 50 minutes?

- Why does this `constraintFunction()` not have parameters?

```
def constraintFunction():
    # for each 
    def innerFunction (x, y): 
        # if 
        if x[0] != y[0]:
            return True
        # se sono qui sono sicuro che sto considerando due appuntamenti che avvengono nello stesso giorno.
        #print("x = ", x, "   y = ", y)
        if (x[2] != y[2] and abs(float(x[1])-float(y[1])) < distance(x[2], y[2])*0.5 + 1):
            return False
        if (x[2] == y[2] and abs(float(x[1])-float(y[1])) != 1):
            return False
        else:
            return True
    return innerFunction
```


- Why is `x` (as in "`appointment`") this:
```
{'Day': "[['thu', 'sat', 'wed']]",
 'House': 'D',
 'Name': 'Logan',
 'Pref': "['Afternoon']",
 'Surname': 'Davies'}
 ```
 And when used in `constraintFunction()` it becomes this:
 ```
 ['sat', '11.00', 'D']
```
Are they different things?