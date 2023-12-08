from constraint import  FunctionConstraint, Problem, BacktrackingSolver
import time

class Paciente:
    def __init__(self,id, nome, idade, genero, data_entrada, data_saida,telemetry,oxygen):
        self.id = id
        self.nome = nome
        self.idade = idade
        self.genero = genero
        self.data_entrada = data_entrada
        self.data_saida = data_saida
        self.telemetry = telemetry
        self.oxygen = oxygen

class Departamento:
    def __init__(self, id_departamento, nome_departamento):
        self.id_departamento = id_departamento
        self.nome_departamento = nome_departamento

class Quarto:
    def __init__(self, id_quarto, nome_quarto, capacidade, departamento, genero_quarto,telemetry, oxygen):
        self.id_quarto = id_quarto
        self.nome_quarto = nome_quarto
        self.capacidade = capacidade
        self.departamento = departamento
        self.genero_quarto = genero_quarto
        self.telemetry = telemetry
        self.oxygen = oxygen

class Cama:
    def __init__(self, id_cama, nome_cama, id_quarto):
        self.id_cama = id_cama
        self.nome_cama = nome_cama
        self.id_quarto = id_quarto
        
start_time = time.time()


# Lista de pacientes
pacientes = [
    Paciente(1, "Patient 1", 98, "M", 1, 2, 0, 0),
    Paciente(2, "Patient 2", 82, "M", 14, 15, 1, 1),
    Paciente(3, "Patient 3", 43, "M", 1, 2, 0, 0),
    Paciente(4, "Patient 4", 88, "F", 16, 18, 0, 0),
    Paciente(5, "Patient 5", 20, "M", 1, 3, 0, 1),
    Paciente(6, "Patient 6", 65, "F", 14, 18, 0, 0),
    Paciente(7, "Patient 7", 33, "F", 1, 7, 1, 0),
    Paciente(8, "Patient 8", 86, "F", 2, 3, 0, 0),
    Paciente(9, "Patient 9", 22, "M", 2, 5, 0, 1),
    Paciente(10, "Patient 10", 70, "F", 3, 10, 1, 0),
    Paciente(11, "Patient 11", 42, "M", 4, 10, 1, 1),
    Paciente(12, "Patient 12", 3, "F", 5, 11, 0, 0),
    Paciente(13, "Patient 13", 14, "F", 5, 12, 0, 1),
    Paciente(14, "Patient 14", 78, "M", 7, 13, 0, 0),
    Paciente(15, "Patient 15", 29, "F", 8, 9, 1, 0),
    Paciente(16, "Patient 16", 61, "M", 9, 15, 0, 0),
    Paciente(17, "Patient 17", 56, "M", 10, 17, 0, 1),
    Paciente(18, "Patient 18", 106, "F", 10, 14, 1, 0),
    Paciente(19, "Patient 19", 4, "F", 11, 17, 1, 0),
    Paciente(20, "Patient 20", 52, "F", 12, 19, 1, 1),
]

# Lista de Departamentos
departamentos = [
    Departamento(1, "Cardiologia"),
    Departamento(2, "Neurologia"),
]

# Lista de Quartos
rooms = [
    Quarto(1,'R1', 2, 1, "F", 1, 0),
    Quarto(2,'R2', 2, 1, "F", 1, 1),
    Quarto(3,'R3', 2, 2, "M", 1, 0),
    Quarto(4,'R4', 2, 2, "M", 1, 1),
]

# Camas disponíveis no hospital com base nos quartos
camas = [
    Cama(1, "Cama 1", 1), # MULHER
    Cama(2, "Cama 2", 1), # MULHER
    Cama(3, "Cama 3", 2), # MULHER
    Cama(4, "Cama 4", 2), # MULHER

    Cama(5, "Cama 5", 3), # HOMEM
    Cama(6, "Cama 6", 3), # HOMEM
    Cama(7, "Cama 7", 4), # HOMEM
    Cama(8, "Cama 8", 4), # HOMEM
]

problem = Problem()


# Sets
camasM = set()
camasF = set()

telemetry = set()
oxygen = set()

dominio = {}

for room in rooms:
    
    if room.genero_quarto == "M":
        camasM.update([cama.id_cama for cama in camas if cama.id_quarto == room.id_quarto])
    elif room.genero_quarto == "F":
        camasF.update([cama.id_cama for cama in camas if cama.id_quarto == room.id_quarto])

    


# Domínio
for i in range(1, len(pacientes) + 1):
    dominio[f"P{i}"] = camasM if pacientes[i-1].genero == "M" else camasF    
    problem.addVariable(f'P{i}', list(dominio[f'P{i}']))



# Pacientes não podem ficar no mesmo <CAMA> no mesmo período
def check_cama_por_noite(a,b):
    return a != b
    

# Pacientes têm de ter o mesmo género que o quarto (no dominio)
def check_genero_quarto(genero,cama_id):
    print(genero,cama_id)

    camaEspecifica = list((cama.id_quarto for cama in camas if cama.id_cama == cama_id))
    quarto = list((quarto.genero_quarto for quarto in rooms if quarto.id_quarto == camaEspecifica[0]))
    return genero == quarto[0]


for i, paciente1 in enumerate(pacientes):
    for j, paciente2 in enumerate(pacientes):
        entradap1 = paciente1.data_entrada
        saidap1 = paciente1.data_saida
        entradap2 = paciente2.data_entrada
        saidap2 = paciente2.data_saida

        if i != j and not(entradap1 > saidap2 or saidap1 < entradap2):
           
            problem.addConstraint(
                FunctionConstraint(check_cama_por_noite),(f"P{i+1}",f"P{j+1}")
            )

# Default é o backtracking
solution = problem.getSolution()


# Lista de Noites    
lista_noites = range(0, max([paciente.data_entrada for paciente in pacientes]) + 1)

for noite in lista_noites:
    print(f"Noite {noite}:")
    res = False
    for i, paciente in enumerate(pacientes):    
        if paciente.data_entrada == noite:

            camaEspecifica = list((cama.id_quarto for cama in camas if cama.id_cama == solution[f'P{i+1}']))
            departamento = list((departamento.nome_departamento for departamento in departamentos if departamento.id_departamento == rooms[camaEspecifica[0]-1].departamento))

            print(f"[{paciente.nome} Gen:{paciente.genero}] - [Dept: {departamento[0]} Quarto: {camaEspecifica[0]} - Cama:{solution[f'P{i+1}']}]  [Entrada: {paciente.data_entrada} - Saída:{paciente.data_saida}]")
            res = True    
    if not res:
        print("Esta noite foi calminha...")
    
    print("---------")

print("--- %s seconds ---" % (time.time() - start_time))