from constraint import Problem, AllDifferentConstraint, FunctionConstraint
import time

## Problema
# 1 - Assign each patient (that will come to the hospital) into a bed for each night that the patient will stay in the hospital. 
# 2 - Each bed belongs to a room and each room belongs to a department, e.g., cardiology.
# 3 - The arrival and departure dates of the patients is fixed: only a bed needs to be assigned for each night.

## Constraints do Problema:
# [1] - 2 patients must not be assigned to the same bed in the same night
# [2] - Room gender limitation: only females, only males, the same gender in the same night, or no gender limitation
# [3] - A patient can require a room with specific equipment(s)

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
    def __init__(self, id_quarto, nome_quarto):
        self.id_quarto = id_quarto
        self.nome_quarto = nome_quarto

class Cama:
    def __init__(self, id_cama, nome_cama):
        self.id_cama = id_cama
        self.dados_cama = nome_cama



# Camas disponíveis no hospital
camas = [
    Cama(1, "1"),
    Cama(2, "2"),
    Cama(3, "3"),
    Cama(4, "4"),
    Cama(5, "5"),
    Cama(6, "6"),
    Cama(7, "7"),
    Cama(8, "8")
]

# Lista de pacientes
pacientes = [
    Paciente("Patient 1", 98, "M", 1, 1),
    Paciente("Patient 2", 82, "M", 1, 6),
    Paciente("Patient 3", 43, "M", 1, 2),
    Paciente("Patient 4", 88, "M", 1, 5),
    Paciente("Patient 5", 20, "F", 1, 4),
    Paciente("Patient 6", 65, "F", 1, 2),
    Paciente("Patient 7", 33, "F", 2,8),
    Paciente("Patient 8", 86, "M", 3, 4),
    Paciente("Patient 9", 22, "F", 3, 6),
    Paciente("Patient 10", 70, "F", 4, 11),
    Paciente("Patient 11", 42, "M", 5, 11),
    Paciente("Patient 12", 3," F", 6, 12),
    Paciente("Patient 13", 14, "F", 6, 13),
    Paciente("Patient 14", 78, "M", 8, 14),
    Paciente("Patient 15", 29, "F", 9, 10),
    Paciente("Patient 16", 61, "F", 10, 16),
    Paciente("Patient 17",56, "F", 11, 18),
    Paciente("Patient 18",106, "F", 11, 15),
    Paciente("Patient 19",4, "M", 12, 18),
    Paciente("Patient 20",52, "F", 13, 20),   
]

problem = Problem()

# Criar o domínio
for idx, paciente in enumerate(pacientes):
    problem.addVariable(f'P{idx + 1}.cama', camas)
    problem.addVariable(f'P{idx + 1}.entrada', [paciente.data_entrada])
    problem.addVariable(f'P{idx + 1}.saida', [paciente.data_saida])

# Adding constraints
for idx1, paciente1 in enumerate(pacientes):
    for idx2, paciente2 in enumerate(pacientes):
        if idx1 != idx2:
            cama1, cama2 = f'P{idx1 + 1}.cama', f'P{idx2 + 1}.cama'
            entrada1, entrada2 = f'P{idx1 + 1}.entrada', f'P{idx2 + 1}.entrada'
            saida1, saida2 = f'P{idx1 + 1}.saida', f'P{idx2 + 1}.saida'
            problem.addConstraint(FunctionConstraint(lambda c1, c2, e1, e2, s1, s2: 
                                                    e1 > s2 or s1 < e2 if c1 == c2 else True),
                                                    (cama1, cama2, entrada1, entrada2, saida1, saida2))

solutions = problem.getSolution()

for idx, paciente in enumerate(pacientes):
    idx_var = idx + 1
    cama_var = f'P{idx_var}.cama'
    entrada_var = f'P{idx_var}.entrada'
    saida_var = f'P{idx_var}.saida'

    print(f'Paciente {idx_var}: Cama: {solutions[cama_var].dados_cama} - Entrada: {solutions[entrada_var]}, Saída: {solutions[saida_var]}')
