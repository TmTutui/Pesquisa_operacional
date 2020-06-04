#!/usr/bin/env python3
from pulp import *

problem = LpProblem("Lucro_com_manteiga", LpMaximize)

insumos = ["insumo1", "insumo2", "insumo3", "insumo4", "insumo5" ]
cost_insumos = [10.4, 7.2, 3.2, 0.017, 0.074]
insumos_production = {
    "insumo1": 2500,
    "insumo2": 2550,
    "insumo3": 2900,
    "insumo4": 10000,
    "insumo5": 5000
}
manteigas = ["Comum", "Extra Fina", "1a qualidade"]
price_manteigas = [16*0.90 , 18*0.85 , 21*0.80 ]  # ja ajustado com o rendimento

# Xij: quantidade de kg de insumo do tipo i colocado na manteiga do tipo j
matrix = [["X11", "X12", "X13"], 
          ["X21", "X22", "X23"],
          ["X31", "X32", "X33"],
          ["X41", "X42", "X43"],
          ["X51", "X52", "X53"]]

############################################
#                                          #
# Resolvendo o problema para caso contínuo #
#                                          #
############################################

x_var = [[LpVariable(matrix[i][j], lowBound=1, cat="Continuous") for j in range(len(matrix[i]))] for i in range(len(matrix))]

receita = lpSum([price_manteigas[y]*x_var[x][y] for x in range(len(insumos)) for y in range(len(manteigas)) ])  # máx [(16 * 0,9 * 1Σ5 Xi1 + 18 * 0,85 * 1Σ5 Xi2 + 21 * 0,75 *  1Σ5 Xi3)

gasto = lpSum( [- cost_insumos[y]*x_var[y][x]  for x in range(len(manteigas))  for y in range(len(insumos)) ] )  # - (10,4 1Σ3 X1j + 7,2 1Σ3 X2j + 3,2 1Σ3 X3j + 0,017 1Σ3 X4j  + 0,0741Σ3 X5j)]


problem += receita + gasto


# RESTRIÇÕES de producao de insumos
for i in range (len(insumos)):
    problem += lpSum([x_var[i][j] for j in range(len(x_var[i]))]) <= insumos_production["insumo" + str(i+1)], "Max_insumos" + str(i)


# RESTRIÇÕES de composicao
"Gordura"
problem += lpSum([x_var[i][0] for i in range(len(x_var))])*0.8 >= 0.6*x_var[0][0] + 0.5*x_var[1][0], "0,6 X11 + 0,5 X21 >= 0,8 1Σ5 Xi1 "
problem += lpSum([x_var[i][1] for i in range(len(x_var))])*0.8 >= 0.6*x_var[0][1] + 0.5*x_var[1][1], "0,6 X12 + 0,5 X22 >= 0,8 1Σ5 Xi2 "
problem += lpSum([x_var[i][2] for i in range(len(x_var))])*0.83>= 0.6*x_var[0][2] + 0.5*x_var[1][2], "0,6 X13 + 0,5 X23 >= 0,83 1Σ5 Xi3 "

"Agua"
problem += lpSum([x_var[i][0] for i in range(len(x_var))])*0.16 >= 0.15*x_var[0][0] + 0.14*x_var[1][0] + 0.99*x_var[4][0], "0,4 X11 + 0,5 X21 <= 0,16 1Σ5 Xi1 "
problem += lpSum([x_var[i][1] for i in range(len(x_var))])*0.16 >= 0.15*x_var[0][1] + 0.14*x_var[1][1] + 0.99*x_var[4][1], "0,4 X12 + 0,5 X22 <= 0,16 1Σ5 Xi2 "
problem += lpSum([x_var[i][2] for i in range(len(x_var))])*0.16 >= 0.15*x_var[0][2] + 0.14*x_var[1][2] + 0.99*x_var[4][2], "0,4 X13 + 0,5 X23 <= 0,16 1Σ5 Xi3 "

"Sal"
problem += lpSum([x_var[i][0] for i in range(len(x_var))])*0.03 >= x_var[3][0], "X41 <= 0,03 1Σ5 Xi1 "
problem += lpSum([x_var[i][1] for i in range(len(x_var))])*0.02 >= x_var[3][1], "X42 <= 0,02 1Σ5 Xi2"
problem += lpSum([x_var[i][2] for i in range(len(x_var))])*0.025 >= x_var[3][2], "X43 <= 0,025 1Σ5 Xi3"

# RESTRIÇÕES de producao minima de cada tipo de manteiga
problem += lpSum([x_var[i][0] for i in range(len(x_var))]) >= 3000, " 1Σ5 Xi1 >= 3000 "
problem += lpSum([x_var[i][1] for i in range(len(x_var))]) >= 2000, " 1Σ5 Xi2 >= 2000 "
problem += lpSum([x_var[i][2] for i in range(len(x_var))]) >= 1000, " 1Σ5 Xi3 >= 1000 "

 
# RESTRIÇÕES de quantidade de corante 
max_corante = 0.005
problem += lpSum([x_var[i][0] for i in range(len(x_var))])*max_corante >= x_var[4][0], " X51 <= " + str(max_corante) + " 1Σ5 Xi1 "
problem += lpSum([x_var[i][1] for i in range(len(x_var))])*max_corante >= x_var[4][1], " X52 <= " + str(max_corante) + " 1Σ5 Xi2 "
problem += lpSum([x_var[i][2] for i in range(len(x_var))])*max_corante >= x_var[4][2], " X53 <= " + str(max_corante) + " 1Σ5 Xi3 "

min_corante = 0.0002
problem += lpSum([x_var[i][0] for i in range(len(x_var))])*min_corante <= x_var[4][0], " X51 >= " + str(min_corante) + " 1Σ5 Xi1 "
problem += lpSum([x_var[i][1] for i in range(len(x_var))])*min_corante <= x_var[4][1], " X52 >= " + str(min_corante) + " 1Σ5 Xi2 "
problem += lpSum([x_var[i][2] for i in range(len(x_var))])*min_corante <= x_var[4][2], " X53 >= " + str(min_corante) + " 1Σ5 Xi3 "


print(problem)

#SOLUTION
problem.solve()
print("Status:", LpStatus[problem.status])

for v in problem.variables():
  if v.varValue >= 0:
    print(v.name, "=", v.varValue)

print("\n")
print("Lucro ótimo para o caso contínuo: " + str(value(problem.objective))) 