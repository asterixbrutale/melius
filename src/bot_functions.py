from config import pip_number

def calculator(budget, risk):
    #rischio basso
    if risk==0:
        new_budget = (0.01/400)*budget
    #rischio medio
    if risk==1:
        new_budget = (0.01/250)*budget
    #rischio alto
    if risk==2:
        new_budget = (0.01/150)*budget

    new_budget *=100
    #circa 0.09
    pip_value = 0.09*new_budget*pip_number
    return pip_value