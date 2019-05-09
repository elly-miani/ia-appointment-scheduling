from ortools.linear_solver import pywraplp

solver = pywraplp.Solver("Soft Constraint Example", pywraplp.Solver.GLOP_LINEAR_PROGRAMMING)

product_a = solver.IntVar(0, 10000, "Pounds of Product A:")
product_b = solver.IntVar(0, 10000, "Pounds of Product B:")

product_a_surplus = solver.IntVar(0, 100, "Product A Surplus:")
product_a_deficit = solver.IntVar(0, 100, "Product A Deficit:")

product_b_surplus = solver.IntVar(0, 100, "Product B Surplus:")
product_b_deficit = solver.IntVar(0, 100, "Product B Deficit:")

cost_surplus = solver.IntVar(0, 10000, "Cost Surplus:")
cost_deficit = solver.IntVar(0, 10000, "Cost Deficit:")

product_a_goal = solver.Add(product_a - product_a_surplus + product_a_deficit == 500)
product_b_goal = solver.Add(product_b - product_b_surplus + product_b_deficit == 250)

cost_goal = solver.Add(product_a * 100 + product_b * 200 + cost_surplus - cost_deficit == 75000)

solver.Minimize(
    (1/100) * product_a_surplus
    + (1/100) * product_a_deficit
    + (1/200) * product_b_surplus
    + (1/200) * product_b_deficit
    + (1/75000) * cost_surplus
    + (1/75000) * cost_deficit
)

status = solver.Solve()

print(status == solver.OPTIMAL)

final_cost = product_a.solution_value() * 100 + product_b.solution_value() * 200

print("Final Cost:", final_cost)

var = [product_a, product_b, product_a_surplus, product_a_deficit,
       product_b_surplus, product_b_deficit,
       cost_surplus, cost_deficit]

for v in var:
    print(v.name(), v.solution_value())
