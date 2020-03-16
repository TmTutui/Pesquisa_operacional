import pip

try:
  from pip import main as pipmain
except ImportError:
  from pip._internal import main as pipmain

def install(package):
  if hasattr(pip, 'main'):
    pip.main(['install', package])
  else:
    pipmain(['install', package])

try:
  from pulp import *
except:
  install("PuLP")
  from pulp import *


problem = LpProblem("Lucro_da_Gasolina", LpMaximize)

petrol = ["petrol1", "petrol2", "petrol3", "petrol4"]
cost_petrol = [19, 24, 20, 27]
petrol_production = {
    "petrol1": 3500,
    "petrol2": 2200,
    "petrol3": 4200,
    "petrol4": 1800
}
gasol = ["gasol1", "gasol2", "gasol3"]
price_gasol = [35, 28, 22]

"""Xij: quantidade de barris de petróleo do tipo i colocada na gasolina do tipo j"""
matrix = [["X11", "X12", "X13"], 
          ["X21", "X22", "X23"],
          ["X31", "X32", "X33"],
          ["X41", "X42", "X43"]]

petrol_var = [LpVariable (petrol[i], lowBound=0, upBound = petrol_production[petrol[i]], cat='Integer') for i in range(len(petrol)) ]
gasol_var = [LpVariable (gasol[i], lowBound=0, cat='Integer') for i in range(len(gasol)) ]
x_var = [[LpVariable(matrix[i][j], lowBound=0, cat="Integer") for j in range(len(matrix[i]))] for i in range(len(matrix))]

receita = lpSum([price_gasol[y]*x_var[x][y] for x in [0, 1, 2, 3] for y in [0, 1, 2] ]) # máx [(35 1Σ4 Xi1 + 28 1Σ4 Xi2 + 22 1Σ4 Xi3)

gasto = lpSum( [- cost_petrol[y]*x_var[y][x]  for x in[0, 1, 2]  for y in[0, 1, 2, 3] ] ) #  - (19 1Σ3 X1j + 24 1Σ3 X2j + 20 1Σ3 X3j + 27 1Σ3 X4j)]


problem += receita+gasto

print(problem)

# RESTRIÇÕES

""" 
1.Superazul
Não mais que 30% de 1
Não menos que 40% de 2
Não mais que 50% de 3


2.Azul
Não mais que 30% de 1
Não menos que 10% de 2

3.Amarela
Não mais que 70% de 1 

"""

petrol_production = {
    "petrol1": 3500,
    "petrol2": 2200,
    "petrol3": 4200,
    "petrol4": 1800
}
