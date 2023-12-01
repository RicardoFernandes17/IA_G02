from constraint import Problem, AllDifferentConstraint, BacktrackingSolver
import time

start_time = time.time()

# Dados
patients = [
    {'ID': 1, 'name': 'Patient1', 'age': 98, 'gender': 'M', 'admission_day': 0, 'discharge_day': 3},
    {'ID': 2, 'name': 'Patient2', 'age': 82, 'gender': 'M', 'admission_day': 0, 'discharge_day': 5},
    {'ID': 3, 'name': 'Patient3', 'age': 43, 'gender': 'M', 'admission_day': 0, 'discharge_day': 1},
    {'ID': 4, 'name': 'Patient4', 'age': 88, 'gender': 'M', 'admission_day': 0, 'discharge_day': 4},
    {'ID': 5, 'name': 'Patient5', 'age': 20, 'gender': 'F', 'admission_day': 0, 'discharge_day': 3},
    {'ID': 6, 'name': 'Patient6', 'age': 65, 'gender': 'F', 'admission_day': 0, 'discharge_day': 1},
    {'ID': 7, 'name': 'Patient7', 'age': 33, 'gender': 'F', 'admission_day': 1, 'discharge_day': 7}
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

# adicionar variáveis: (paciente, noite) -> cama
variable_beds = {}
variable_domains = {}  # para guardar o dominio das variaveis

for patient in patients:
    for night in range(patient['admission_day'], patient['discharge_day']):
        variable_bed = (patient['ID'], night)
        domain_bed = [(bed['ID_room'], bed['ID_bed']) for bed in beds]
        problem.addVariable(variable_bed, domain_bed)
        variable_beds[(patient['ID'], night)] = variable_bed
        variable_domains[variable_bed] = domain_bed

# restriçao - nao deve haver pacientes com o mesmo par (quarto, cama) no mesmo dia
for night in range(max(patient['admission_day'] for patient in patients), min(patient['discharge_day'] for patient in patients) + 1):
    variables_for_night = [variable_beds[(patient['ID'], night)] for patient in patients if night in range(patient['admission_day'], patient['discharge_day'])]
    problem.addConstraint(AllDifferentConstraint(), variables_for_night)

# definir a estratégia de backtracking (talvez seja a default, mas força)
# estratégia que explora sistematicamente o espaço de busca para encontrar uma solução.
# tenta diferentes atribuições de valores às variáveis até encontrar uma solução ou determinar que não há solução possível
problem.setSolver(BacktrackingSolver())

# executar o solver para obter uma solução
solution = problem.getSolution()

# mostrar o domínio das variáveis
def mostrar_dominio():
    print("\nDominio:")
    for variable in problem._variables:
        domain = variable_domains.get(variable)
        print(f"{variable}: {domain}")

def mostrar_solucao_por_noite():
    # ordenar a solucao por noite
    sorted_solution = sorted(solution.items(), key=lambda x: x[0][1])

    # Mostrar a solução ordenada
    print("\nAtribuiçao de pacientes a quartos por noite:")
    current_night = None
    for (patient_id, night), (room_id, bed_id) in sorted_solution:
        if night != current_night:
            print(f"\nNoite {night}:")
            current_night = night
        patient = next(p for p in patients if p['ID'] == patient_id)
        room = next(r for r in rooms if r['ID'] == room_id)
        print(f"  {patient['name']} ({patient['ID']}) -> Room {room['name']}, Bed {bed_id}")

mostrar_dominio()
mostrar_solucao_por_noite()

print("--- %s seconds ---" % round(time.time() - start_time, 3))

