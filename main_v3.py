from abc import ABC, abstractmethod
from datetime import datetime
import textwrap

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
    def __init__(self, num, cliente):
        self._saldo = 0
        self._num = num
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, num):
        return cls(num, cliente)

    @property
    def saldo(self):
        return self._saldo

    @property
    def num(self):
        return self._num

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
            print("\nxxxx Saldo insuficiente para completar esta operação xxxx")
        elif valor > 0:
            self._saldo -= valor
            print("\n==== Saque realizado com sucesso ====")
            return True
        else:
            print("\nValor informado inválido")
        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("\n==== Depósito realizado com sucesso ====")
        else:
            print("\nxxxx Valor informado inválido xxxx")
            return False
        return True

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
        )
        excedeu_limite = valor > self._limite
        excedeu_saques = numero_saques >= self._limite_saques
        if excedeu_limite:
            print("\nxxxx Operação inválida, o valor informado é superior ao limite de saque xxxx")
        elif excedeu_saques:
            print("\nxxxx Você já atingiu o número máximo de saques por hoje, retorne amanhã para fazer mais xxxx")
        else:
            return super().sacar(valor)
        return False

    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.num}
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
                "data": datetime.now(),
            }
        )

class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @classmethod
    @abstractmethod
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

def menu():
    menu = """\n
    ===================== MENU =====================
                    [1]  NOVO CLIENTE
                    [2]  NOVA CONTA
                    [3]  LISTAR CONTAS
                    [4]  DEPOSITAR
                    [5]  SACAR
                    [6]  EXTRATO
                    [0]  SAIR
    =================================================
    -> """
    return input(textwrap.dedent(menu))

def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\nxxxx Cliente não possui conta xxxx")
        return

    # FIXME: não permite cliente escolher a conta
    return cliente.contas[0]

def depositar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("\nxxxx Cliente não encontrado xxxx")
        return
    valor = float(input("Informe o valor do depósito: "))
    transacao = Deposito(valor)
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    cliente.realizar_transacao(conta, transacao)

def sacar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("\nxxxx Cliente não encontrado xxxx")
        return
    valor = float(input("Informe o valor do saque: "))
    transacao = Saque(valor)
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    cliente.realizar_transacao(conta, transacao)

def exibir_extrato(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("\nxxxx Cliente não encontrado xxxx")
        return
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    print("\n================ EXTRATO ================")
    transacoes = conta.historico.transacoes
    extrato = ""
    if not transacoes:
        extrato = "xxxx Esta conta não recebeu nenhum tipo de movimentação até o momento xxxx"
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao["tipo"]}:\n\tR$ {transacao["valor"]:,.2f}"
    print(extrato)
    print(f"\nSaldo:\n\tR$ {conta.saldo:,.2f}")
    print("==========================================")

def criar_cliente(clientes):
    cpf = input("Informe o CPF (somente número): ")
    cliente = filtrar_cliente(cpf, clientes)
    if cliente:
        print("\nxxxx Já existe cliente com esse CPF xxxx")
        return
    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd/mm/aaaa): ")
    endereco = input("Informe o endereço (bairro, rua, número, cidade/sigla estado): ")
    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)
    clientes.append(cliente)
    print("\n==== Cliente criado com sucesso ====")

def criar_conta(num_conta, clientes, contas):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("\nxxxx Este CPF não está cadastrado no sistema, cadastre-o primeiros, depois tente efetuar esta operação novamente xxxx")
        return
    conta = ContaCorrente.nova_conta(cliente=cliente, num=num_conta)
    contas.append(conta)
    cliente.contas.append(conta)

    print("\n==== Conta criada com sucesso ====")

def listar_contas(contas):
    for conta in contas:
        print("=" * 50)
        print(textwrap.dedent(str(conta)))

def main():
    clientes = []
    contas = []

    while True:
        opcao = int(menu())
        match opcao:
            case 1:
                criar_cliente(clientes)
            case 2:
                numero_conta = len(contas) + 1
                criar_conta(numero_conta, clientes, contas)
            case 3:
                listar_contas(contas)
            case 4:
                depositar(clientes)
            case 5:
                sacar(clientes)
            case 6:
                exibir_extrato(clientes)
            case 0:
                print("==== Obrigado por utilizar nosso sistema ====")
                break
            case _:
                print("\nxxxx Operação informada inválida, tente novamentexxxx")

main()