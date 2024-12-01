import textwrap
from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime


# Classes e Funções relacionadas a transações e contas
class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf


class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")

        elif valor > 0:
            self._saldo -= valor
            print("\n=== Saque realizado com sucesso! ===")
            return True

        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("\n=== Depósito realizado com sucesso! ===")
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
            return False

        return True


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
        )

        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saques >= self.limite_saques

        if excedeu_limite:
            print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")

        elif excedeu_saques:
            print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")

        else:
            return super().sacar(valor)

        return False

    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """


class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            }
        )


class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractclassmethod
    def registrar(self, conta):
        pass


class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


# Funções para interação com o usuário
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
    if any(usuario.cpf == cpf for usuario in usuarios):
        print("\n!!! Já existe um usuário com esse CPF! !!!")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    usuario = PessoaFisica(nome, data_nascimento, cpf, endereco)
    usuarios.append(usuario)
    print(" Usuário criado com sucesso! ")


def criar_conta(numero_conta, usuarios):
    cpf = input("Informe o CPF do usuário: ")
    usuario = next((user for user in usuarios if user.cpf == cpf), None)

    if usuario:
        conta = ContaCorrente(numero_conta, usuario)
        usuario.adicionar_conta(conta)
        print("\n Conta criada com sucesso! ")
        return conta

    print("\n!!! Usuário não encontrado, fluxo de criação de conta encerrado! !!!")
    return None


def listar_contas(contas):
    for conta in contas:
        print("=" * 100)
        print(conta)


# Inicialização de variáveis
usuarios = []
contas = []
numero_conta = 1

while True:
    operacao_selecionada = menu()

    if operacao_selecionada == "1":
        valor_depositado = float(input('Informe o valor a ser depositado: '))
        cpf = input("Informe o CPF do titular: ")
        usuario = next((user for user in usuarios if user.cpf == cpf), None)
        if usuario and usuario.contas:
            conta = usuario.contas[0]
            deposito = Deposito(valor_depositado)
            usuario.realizar_transacao(conta, deposito)
        else:
            print("Usuário ou conta não encontrados.")

    elif operacao_selecionada == "2":
        valor_saque = float(input("Informe o valor do saque: "))
        cpf = input("Informe o CPF do titular: ")
        usuario = next((user for user in usuarios if user.cpf == cpf), None)
        if usuario and usuario.contas:
            conta = usuario.contas[0]
            saque = Saque(valor_saque)
            usuario.realizar_transacao(conta, saque)
        else:
            print("Usuário ou conta não encontrados.")

    elif operacao_selecionada == "3":
        cpf = input("Informe o CPF do titular: ")
        usuario = next((user for user in usuarios if user.cpf == cpf), None)
        if usuario and usuario.contas:
            conta = usuario.contas[0]
            print("\nEXTRATO:")
            for transacao in conta.historico.transacoes:
                print(f"{transacao['tipo']}: R$ {transacao['valor']:.2f} em {transacao['data']}")
            print(f"\nSaldo atual: R$ {conta.saldo:.2f}")
        else:
            print("Usuário ou conta não encontrados.")

    elif operacao_selecionada == "4":
        criar_usuario(usuarios)

    elif operacao_selecionada == "5":
        conta = criar_conta(numero_conta, usuarios)
        if conta:
            contas.append(conta)
            numero_conta += 1

    elif operacao_selecionada == "6":
        listar_contas(contas)

    elif operacao_selecionada == "7":
        print("Saindo... Até logo!")
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")
