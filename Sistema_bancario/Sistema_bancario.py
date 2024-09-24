opcoes = """
=-=-=-=-=-=-=-=-=-=-=-=-
Bem vindo ao seu novo caixa virtual! 
Selecione o que deseja
[1] Depósito
[2] Saque
[3] Extrato
[4] Sair
=>"""
saldo = 0
extrato = ""
limite = 500
numero_saques = 0
LIMITE_SAQUES = 3


while True:
    operação_selecionada = input(opcoes)

    if operação_selecionada == "1":
        valor_depositado = float(input('Informe o valor a ser depositado: '))
        print(f'você depositou {valor_depositado}')

        if valor_depositado > 0:
            saldo += valor_depositado
            extrato += f"Depósito: R$ {valor_depositado:.2f}\n"

        else:
            print("Operação inválida, valor fornecido é inválido.")

    elif operação_selecionada == "2":
            valor_depositado = float(input("Informe o valor do saque: "))

            excedeu_saldo = valor_depositado > saldo
            excedeu_limite = valor_depositado > limite
            excedeu_saques = numero_saques >= LIMITE_SAQUES

        
            if excedeu_saldo:
                print("Você não possui saldo suficiente.")

            elif excedeu_limite:
                print("valor do seu saque excede o limite que você possui.")

            elif excedeu_saques:
                print("Número máximo de saques diários excedido. Volte amanhã!")

            elif valor_depositado > 0:
                saldo -= valor_depositado
                extrato += f"Saque: R$ {valor_depositado:.2f}\n"
                numero_saques += 1

            else:
                print("Falha! O valor informado é inválido.")

    elif operação_selecionada == "3":
            print("\n==================================")
            print("\n              EXTRATO             ")
            print("Não foram feitas movimentações na sua conta." if not extrato else extrato)
            print(f"\nSaldo: R$ {saldo:.2f}")
            print("==========================================")

    elif operação_selecionada == "4":
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")
