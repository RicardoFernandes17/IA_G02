from constraint import Problem, AllDifferentConstraint

#dados
patients = [
    {'ID': 1, 'name': 'Patient1', 'age': 98, 'gender': 'M', 'admission_day': 0, 'discharge_day': 0},
    {'ID': 2, 'name': 'Patient2', 'age': 82, 'gender': 'M', 'admission_day': 0, 'discharge_day': 5},
    #{'ID': 3, 'name': 'Patient3', 'age': 43, 'gender': 'M', 'admission_day': 0, 'discharge_day': 1},
    #{'ID': 4, 'name': 'Patient4', 'age': 88, 'gender': 'M', 'admission_day': 0, 'discharge_day': 4},
    #{'ID': 5, 'name': 'Patient5', 'age': 20, 'gender': 'F', 'admission_day': 0, 'discharge_day': 3},
    #{'ID': 6, 'name': 'Patient6', 'age': 65, 'gender': 'F', 'admission_day': 0, 'discharge_day': 1},
    #{'ID': 7, 'name': 'Patient7', 'age': 33, 'gender': 'F', 'admission_day': 1, 'discharge_day': 7}
]

departments = [
    {'ID': 1, 'Name': 'Dept01'},
    {'ID': 2, 'Name': 'Dept02'}
]

rooms = [
    {'ID': 11, 'name': 'R11', 'capac': 2, 'dept': 1},
    {'ID': 12, 'name': 'R12', 'capac': 2, 'dept': 1},
    {'ID': 21, 'name': 'R22', 'capac': 2, 'dept': 2},
    {'ID': 22, 'name': 'R23', 'capac': 2, 'dept': 2}
]

beds = [
    {'ID_bed': 1, 'ID_room': 11},
    {'ID_bed': 2, 'ID_room': 11},
    {'ID_bed': 3, 'ID_room': 12},
    {'ID_bed': 4, 'ID_room': 12},
    {'ID_bed': 5, 'ID_room': 21},
    {'ID_bed': 6, 'ID_room': 21},
    {'ID_bed': 7, 'ID_room': 22},
    {'ID_bed': 8, 'ID_room': 22}
]

# criar o problema CSP
problem = Problem()

# guardar o dominio das variáveis
variable_domains = {}

# variaveis: paciente -> quarto
for patient in patients:
    variable = patient['ID']
    domain = [bed['ID_bed'] for bed in beds]
    variable_domains[variable] = domain
    problem.addVariable(variable, domain)

# mostrar o domínio
print("Domínio das variáveis:")
for variable, domain in variable_domains.items():
    print(f"Paciente {variable}: {domain}")

# restriçao - cada paciente só pode ser alocado a um quarto e cama diferentes
def all_different_constraint(*args):
    return len(set(args)) == len(args)

# Aplicar a restrição a cada par de variáveis (paciente, cama)
for i in range(len(patients)):
    for j in range(i + 1, len(patients)):
        problem.addConstraint(all_different_constraint, [patients[i]['ID'], patients[j]['ID']])

# restrição - cada paciente deve ter uma cama para cada noite no hospital
# def nightly_allocation_constraint(*args):
#    return len(set(args)) == 1

# Aplicar a nova restrição a cada combinação de variáveis (paciente, noite)
# for patient in patients:
#    for night in range(patient['admission_day'], patient['discharge_day'] + 1):
#        problem.addConstraint(nightly_allocation_constraint, [patient['ID'], night])
        
# executar o solver
solutions = problem.getSolutions()

# mostrar a soluçao
for solution in solutions:
    print("Alocação de pacientes a quartos:")
    for patient_id, bed_id in solution.items():
        patient = next(p for p in patients if p['ID'] == patient_id)
        bed = next(b for b in beds if b['ID_bed'] == bed_id)
        print(f"{patient['name']} ({patient['ID']}) -> Room {bed['ID_room']}, Bed {bed['ID_bed']}")
    print("\n")
