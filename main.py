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
gasol = ["Superazul", "Azul", "Amarela"]
price_gasol = [35, 28, 22]

# Xij: quantidade de barris de petróleo do tipo i colocada na gasolina do tipo j
matrix = [["X11", "X12", "X13"], 
          ["X21", "X22", "X23"],
          ["X31", "X32", "X33"],
          ["X41", "X42", "X43"]]

# petrol_var = [LpVariable(petrol[i], lowBound=0, upBound=petrol_production[petrol[i]], cat='Continuous') for i in range(len(petrol))]
# gasol_var = [LpVariable (gasol[i], lowBound=0, cat='Continuous') for i in range(len(gasol)) ]

x_var = [[LpVariable(matrix[i][j], lowBound=0, cat="Continuous") for j in range(len(matrix[i]))] for i in range(len(matrix))]

receita = lpSum([price_gasol[y]*x_var[x][y] for x in [0, 1, 2, 3] for y in [0, 1, 2] ]) # máx [(35 1Σ4 Xi1 + 28 1Σ4 Xi2 + 22 1Σ4 Xi3)

gasto = lpSum( [- cost_petrol[y]*x_var[y][x]  for x in[0, 1, 2]  for y in[0, 1, 2, 3] ] ) #  - (19 1Σ3 X1j + 24 1Σ3 X2j + 20 1Σ3 X3j + 27 1Σ3 X4j)]

problem += receita+gasto


# RESTRIÇÕES de producao de petroleo
problem += lpSum([x_var[0][j] for j in range(len(x_var[0]))]) <= 3500.0, "Max_petrol1"
problem += lpSum([x_var[1][j] for j in range(len(x_var[1]))]) <= 2200.0, "Max_petrol2"
problem += lpSum([x_var[2][j] for j in range(len(x_var[2]))]) <= 4200.0, "Max_petrol3"
problem += lpSum([x_var[3][j] for j in range(len(x_var[3]))]) <= 1800.0, "Max_petrol4"

# RESTRIÇÕES de gasolina 1, Superazul
problem += lpSum([x_var[i][0] for i in range(len(x_var))])*0.3 >= x_var[0][0], "Não mais que 0.3 de petrol1 na Superazul "
problem += lpSum([x_var[i][0] for i in range(len(x_var))])*0.4 <= x_var[1][0], "Não menos que 0.4 de petrol2 na Superazul "
problem += lpSum([x_var[i][0] for i in range(len(x_var))])*0.5 >= x_var[2][0], "Não menos que 0.5 de petrol3 na Superazul "

# RESTRIÇÕES de gasolina 2, Azul
problem += lpSum([x_var[i][1] for i in range(len(x_var))])*0.3 >= x_var[0][1], "Não mais que 0.3 de petrol1 na Azul "
problem += lpSum([x_var[i][1] for i in range(len(x_var))])*0.1 <= x_var[1][1], "Não menos que 0.1 de petrol2 na Azul "

# RESTRIÇÕES de gasolina 3, Amarela
problem += lpSum([x_var[i][2] for i in range(len(x_var))])*0.7 >= x_var[0][2], "Não mais que 0.7 de petrol1 na Amarela "



#SOLUTION
problem.solve()
print("Status:", LpStatus[problem.status])

for v in problem.variables():
  if v.varValue >= 0:
    print(v.name, "=", v.varValue)

print("\n")
print("Lucro otimo:" + str(value(problem.objective)))