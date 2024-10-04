import textwrap

def menu():
    opcoes = """
    =-=-=-=-=-=-=-=-=-=-=-=-
    Bem-vindo ao seu novo caixa virtual! 
    Selecione o que deseja:
    [1] Depósito
    [2] Saque
    [3] Extrato
    [4] Novo Usuário
    [5] Nova Conta
    [6] Listar Contas
    [7] Sair
    => """
    return input(opcoes)

def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente números): ")
    if any(usuario['cpf'] == cpf for usuario in usuarios):
        print("\n!!! Já existe um usuário com esse CPF! !!!")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})
    print(" Usuário criado com sucesso! ")

def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF do usuário: ")
    usuario = next((user for user in usuarios if user["cpf"] == cpf), None)

    if usuario:
        print("\n Conta criada com sucesso! ")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}
    print("\n!!! Usuário não encontrado, fluxo de criação de conta encerrado! !!!")

def listar_contas(contas):
    for conta in contas:
        linha = f"""\
            Agência:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
        """
        print("=" * 100)
        print(textwrap.dedent(linha))

# Inicialização de variáveis
saldo = 0
extrato = ""
limite = 500
numero_saques = 0
LIMITE_SAQUES = 3
usuarios = []
contas = []
AGENCIA = "0001"

while True:
    operacao_selecionada = menu()

    if operacao_selecionada == "1":
        valor_depositado = float(input('Informe o valor a ser depositado: '))
        
        if valor_depositado > 0:
            saldo += valor_depositado
            extrato += f"Depósito: R$ {valor_depositado:.2f}\n"
            print(f'Você depositou R$ {valor_depositado:.2f}')
        else:
            print("Operação inválida, valor fornecido é inválido.")

    elif operacao_selecionada == "2":
        valor_saque = float(input("Informe o valor do saque: "))

        excedeu_saldo = valor_saque > saldo
        excedeu_limite = valor_saque > limite
        excedeu_saques = numero_saques >= LIMITE_SAQUES

        if excedeu_saldo:
            print("Você não possui saldo suficiente.")
        elif excedeu_limite:
            print("O valor do seu saque excede o limite que você possui.")
        elif excedeu_saques:
            print("Número máximo de saques diários excedido. Volte amanhã!")
        elif valor_saque > 0:
            saldo -= valor_saque
            extrato += f"Saque: R$ {valor_saque:.2f}\n"
            numero_saques += 1
            print(f'Saque de R$ {valor_saque:.2f} realizado com sucesso!')
        else:
            print("Falha! O valor informado é inválido.")

    elif operacao_selecionada == "3":
        print("\n==================================")
        print("\n              EXTRATO             ")
        print("Não foram feitas movimentações na sua conta." if not extrato else extrato)
        print(f"\nSaldo: R$ {saldo:.2f}")
        print("==========================================")

    elif operacao_selecionada == "4":
        criar_usuario(usuarios)

    elif operacao_selecionada == "5":
        numero_conta = len(contas) + 1
        conta = criar_conta(AGENCIA, numero_conta, usuarios)
        if conta:
            contas.append(conta)

    elif operacao_selecionada == "6":
        listar_contas(contas)

    elif operacao_selecionada == "7":
        print("Saindo... Até logo!")
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")
