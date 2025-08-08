import json
from datetime import datetime

DATA_FILE = "data.json"

# -------------------------
# Funções de persistência
# -------------------------
def carregar_dados():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"vagas_totais": 5, "veiculos": []}

def salvar_dados(dados):
    with open(DATA_FILE, "w") as f:
        json.dump(dados, f, indent=4)

# -------------------------
# Funcionalidades do sistema
# -------------------------
def listar_vagas(dados):
    vagas_ocupadas = len(dados["veiculos"])
    vagas_livres = dados["vagas_totais"] - vagas_ocupadas
    print("\nStatus do Estacionamento:")
    print(f"Vagas Ocupadas: {vagas_ocupadas}")
    print(f"Vagas Livres: {vagas_livres}")
    print(f"Total de Vagas: {dados['vagas_totais']}")

def registrar_entrada(dados):
    if len(dados["veiculos"]) >= dados["vagas_totais"]:
        print("Estacionamento lotado.")
        return
    
    placa = input("Digite a placa do veículo: ").upper().strip()
    
    # Verifica se já está no estacionamento
    if any(v["placa"] == placa for v in dados["veiculos"]):
        print("Este veículo já está registrado no estacionamento.")
        return
    
    hora_entrada = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    dados["veiculos"].append({"placa": placa, "entrada": hora_entrada})
    salvar_dados(dados)
    print(f"Entrada registrada para {placa} às {hora_entrada}.")

def registrar_saida(dados):
    placa = input("Digite a placa do veículo: ").upper().strip()
    veiculo = next((v for v in dados["veiculos"] if v["placa"] == placa), None)
    
    if not veiculo:
        print("Veículo não encontrado.")
        return
    
    entrada = datetime.strptime(veiculo["entrada"], "%Y-%m-%d %H:%M:%S")
    saida = datetime.now()
    horas = (saida - entrada).total_seconds() / 3600
    valor = round(max(1, horas) * 5, 2)  # Cobrança mínima de 1 hora
    
    dados["veiculos"].remove(veiculo)
    salvar_dados(dados)
    print(f"Saída registrada para {placa}.")
    print(f"Tempo estacionado: {horas:.2f} horas.")
    print(f"Valor a pagar: R${valor:.2f}")

def listar_veiculos(dados):
    if not dados["veiculos"]:
        print("Nenhum veículo estacionado.")
        return
    
    print("\nVeículos estacionados:")
    for v in dados["veiculos"]:
        print(f"Placa: {v['placa']} | Entrada: {v['entrada']}")

# -------------------------
# Menu principal
# -------------------------
def main():
    dados = carregar_dados()
    
    print("Sistema de Estacionamento")
    
    while True:
        print("\n1 - Listar vagas")
        print("2 - Registrar entrada")
        print("3 - Registrar saída")
        print("4 - Listar veículos estacionados")
        print("0 - Sair")
        
        opcao = input("Escolha uma opção: ").strip()
        
        if opcao == "1":
            listar_vagas(dados)
        elif opcao == "2":
            registrar_entrada(dados)
        elif opcao == "3":
            registrar_saida(dados)
        elif opcao == "4":
            listar_veiculos(dados)
        elif opcao == "0":
            print("Sistema encerrado.")
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    main()