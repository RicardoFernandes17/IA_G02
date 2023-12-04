from constraint import MinConflictsSolver, Problem, AllDifferentConstraint, FunctionConstraint,BacktrackingSolver
import time

## Problema
# 1 - Assign each patient (that will come to the hospital) into a bed for each night that the patient will stay in the hospital. 
# 2 - Each bed belongs to a room and each room belongs to a department, e.g., cardiology.
# 3 - The arrival and departure dates of the patients is fixed: only a bed needs to be assigned for each night.

## Constraints do Problema:
# - 2 patients must not be assigned to the same bed in the same night
# - Room gender limitation: only females, only males, the same gender in the same night, or no gender limitation
# - A patient can require a room with specific equipment(s)

class Paciente:
    def __init__(self, nome, idade, genero, data_entrada, data_saida):
        self.nome = nome
        self.idade = idade
        self.genero = genero
        self.data_entrada = data_entrada
        self.data_saida = data_saida

class Departamento:
    def __init__(self, id_departamento, nome_departamento):
        self.id_departamento = id_departamento
        self.nome_departamento = nome_departamento

class Quarto:
    def __init__(self, id_quarto, nome_quarto, capacidade, departamento):
        self.id_quarto = id_quarto
        self.nome_quarto = nome_quarto
        self.capacidade = capacidade
        self.departamento = departamento

class Cama:
    def __init__(self, id_cama, nome_cama, id_quarto):
        self.id_cama = id_cama
        self.dados_cama = nome_cama
        self.id_quarto = id_quarto

        
start_time = time.time()


# Lista de pacientes
pacientes = [
    Paciente("Patient 1", 98, "M", 1, 2),
    Paciente("Patient 2", 82, "M", 1, 3),
    Paciente("Patient 3", 43, "M", 1, 4),
    Paciente("Patient 4", 88, "M", 1, 5),
    Paciente("Patient 5", 20, "F", 1, 1),
    Paciente("Patient 6", 65, "F", 1, 1),
    Paciente("Patient 7", 33, "F", 2, 8),
    Paciente("Patient 8", 86, "M", 3, 4),
    Paciente("Patient 9", 22, "F", 3, 6),
    Paciente("Patient 10", 70, "F", 4, 11),
    # Paciente("Patient 11", 42, "M", 5, 11),
    # Paciente("Patient 12", 3," F", 6, 12),
    # Paciente("Patient 13", 14, "F", 6, 13),
    # Paciente("Patient 14", 78, "M", 8, 14),
    # Paciente("Patient 15", 29, "F", 9, 10),
    # Paciente("Patient 16", 61, "F", 10, 16),
    # Paciente("Patient 17", 56, "F", 11, 18),
    # Paciente("Patient 18", 106, "F", 11, 15),
    # Paciente("Patient 19", 4, "M", 12, 18),
    # Paciente("Patient 20", 52, "F", 13, 20),   
]

departamentos = [
    Departamento(1, "Cardiologia"),
    Departamento(2, "Neurologia"),
]

rooms = [
    Quarto(1,'R1', 4, 1),
    Quarto(2,'R2', 4, 1),
]

# Camas disponíveis no hospital
camas = [
    Cama(1, "1", 1),
    Cama(2, "2", 1),
    Cama(3, "3", 1),
    Cama(4, "4", 1),
    Cama(5, "5", 2),
    Cama(6, "6", 2),
    Cama(7, "7", 2),
    Cama(8, "8", 2)
]


problem = Problem()

# Criar o domínio
for idx, paciente in enumerate(pacientes):
    problem.addVariable(f'P{idx + 1}.cama', camas)
    problem.addVariable(f'P{idx + 1}.entrada', [paciente.data_entrada])
    problem.addVariable(f'P{idx + 1}.saida', [paciente.data_saida])
    problem.addVariable(f'P{idx + 1}.genero', [paciente.genero])


# Constraints
def all_different_constraint(*args):
    return len(set(args)) == len(args)


# Function to add night assignment constraints between patients
def add_night_assignment_constraints(problem, patients):
    for idx1, paciente1 in enumerate(patients):
        for idx2, paciente2 in enumerate(patients):
            if idx1 != idx2:
                cama1, cama2 = f'P{idx1 + 1}.cama', f'P{idx2 + 1}.cama'
                entrada1, entrada2 = f'P{idx1 + 1}.entrada', f'P{idx2 + 1}.entrada'
                saida1, saida2 = f'P{idx1 + 1}.saida', f'P{idx2 + 1}.saida'
                
                
                problem.addConstraint(
                    FunctionConstraint(
                        lambda c1, c2, e1, e2, s1, s2: e1 > s2 or s1 < e2 if c1 == c2 else True
                    ),
                    (cama1, cama2, entrada1, entrada2, saida1, saida2)
                )

# Execução
add_night_assignment_constraints(problem, pacientes)

problem.setSolver(BacktrackingSolver())
solutions = problem.getSolution()

# Ordenando as soluções por entrada
sorted_solution = sorted(solutions.items(), key=lambda x: x[0])
lista_noites = range(1, max([paciente.data_saida for paciente in pacientes]) + 1)


# Listar a solução por noite
for noite in lista_noites:
    print(f'Noite {noite}:')
    for idx, paciente in enumerate(pacientes):
        if solutions[f'P{idx + 1}.entrada'] == noite:
            idx_var = idx + 1
            cama_var = f'P{idx_var}.cama'
            entrada_var = f'P{idx_var}.entrada'
            saida_var = f'P{idx_var}.saida'
            genero_var = f'P{idx_var}.genero'

            print(f'{idx_var}: {paciente.nome}, Sexo: {paciente.genero}, [Datas: {solutions[entrada_var]} a {solutions[saida_var]}], Quarto {solutions[cama_var].id_quarto}, Cama {solutions[cama_var].id_cama}')
        
    print('------------------')

print("--- %s seconds ---" % round(time.time() - start_time, 3))