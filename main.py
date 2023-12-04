from collections import defaultdict
from constraint import Problem, FunctionConstraint,BacktrackingSolver
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
    def __init__(self,id, nome, idade, genero, data_entrada, data_saida):
        self.id = id
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
    def __init__(self, id_quarto, nome_quarto, capacidade, departamento, genero_quarto):
        self.id_quarto = id_quarto
        self.nome_quarto = nome_quarto
        self.capacidade = capacidade
        self.departamento = departamento
        self.genero_quarto = genero_quarto

class Cama:
    def __init__(self, id_cama, nome_cama, id_quarto):
        self.id_cama = id_cama
        self.dados_cama = nome_cama
        self.id_quarto = id_quarto

        
start_time = time.time()


# Lista de pacientes
pacientes = [
    Paciente(1,"Paciente 1", 98, "M", 1, 2),
    Paciente(2,"Paciente 2", 82, "M", 1, 3),
    Paciente(3,"Paciente 3", 43, "F", 1, 4),
    Paciente(4,"Paciente 4", 88, "M", 1, 5),
    Paciente(5,"Paciente 5", 20, "F", 1, 1),
    Paciente(6,"Paciente 6", 65, "F", 1, 1),
    Paciente(7,"Paciente 7", 88, "M", 1, 5),
    Paciente(8,"Paciente 8", 88, "M", 1, 5),
    Paciente(9,"Paciente 9", 86, "M", 3, 4),
    Paciente(10,"Paciente 10", 22, "F", 3, 6),
    Paciente(11,"Paciente 11", 70, "F", 4, 6),
    Paciente(12,"Paciente 12", 70, "F", 4, 6),
]

departamentos = [
    Departamento(1, "Cardiologia"),
    Departamento(2, "Neurologia"),
]

rooms = [
    Quarto(1,'R1', 4, 1, "M"),
    Quarto(2,'R2', 4, 1, "F"),
    Quarto(3,'R3', 4, 1, "M"),
    Quarto(4,'R4', 4, 1, "F"),
]

# Camas disponíveis no hospital com base nos quartos
camas = []
for room in rooms:
    for i in range(1, room.capacidade + 1):
        camas.append(Cama(i, "Cama {i}" , room.id_quarto))

problem = Problem()

# Criar o domínio
for idx, paciente in enumerate(pacientes):
    problem.addVariable(f'P{idx + 1}.genero', [paciente.genero])
    problem.addVariable(f'P{idx + 1}.entrada', [paciente.data_entrada])
    problem.addVariable(f'P{idx + 1}.saida', [paciente.data_saida])
    problem.addVariable(f'P{idx + 1}.cama', camas)
    problem.addVariable(f'P{idx + 1}.quarto', rooms)



def getQuartoByCama(cama):
    for quarto in rooms:
        if quarto.id_quarto == cama.id_quarto:
            return quarto

# Function to add night assignment constraints between patients
def add_night_assignment_constraints(problem, patients):
    for idx1, paciente1 in enumerate(patients):
        for idx2, paciente2 in enumerate(patients):
            if idx1 != idx2:
                cama1, cama2 = f'P{idx1 + 1}.cama', f'P{idx2 + 1}.cama'
                entrada1, entrada2 = f'P{idx1 + 1}.entrada', f'P{idx2 + 1}.entrada'
                saida1, saida2 = f'P{idx1 + 1}.saida', f'P{idx2 + 1}.saida'
                genero1,genero2 = f'P{idx1 + 1}.genero', f'P{idx2 + 1}.genero'
 
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

print(sorted_solution)


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
            quarto_var = f'P{idx_var}.quarto'
            room_gender = solutions[quarto_var].genero_quarto


            print(f'{idx_var}: {paciente.nome}, Sexo: {paciente.genero}, [Datas: {solutions[entrada_var]} a {solutions[saida_var]}], Quarto {solutions[cama_var].id_quarto}, Cama {solutions[cama_var].id_cama} [{room_gender}]')
    print('------------------')



print("--- %s seconds ---" % round(time.time() - start_time, 3))