from datetime import datetime
import textwrap

def menu():
    menu = f"""
    =================== MENU ===================

                   [1] DEPOSITAR
                   [2] SACAR
                   [3] EXTRATO
                   [4] NOVO USUÁRIO
                   [5] NOVA CONTA
                   [6] LISTAR CONTAS
                   [0] SAIR
                   
    ============================================
    """

    return int(input(textwrap.dedent(menu)))

def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente["cpf"] == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

def depositar(saldo, valor, extrato, /):

    if valor > 0:
        saldo += valor
        extrato += f"Depósito:\tR$ {valor:,.2f}\t{datetime.strftime(datetime.now(), "%d/%m/%Y %H:%M:%S")}\n"
        print("\n===Depósito finalizado com sucesso===")
    else:
        print("---Ocorreu um erro, valor digitado inválido---")
    return saldo, extrato

def sacar(*, saldo, valor, extrato, limite, num_saque, limite_saque):
    excedeu_saldo =  valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = num_saque >= limite_saque

    if excedeu_saldo:
        print("===Saldo insuficiente para efetuar o saque===")
    elif excedeu_limite:
        print("===Valor de saque superior ao limite===")
    elif excedeu_saques:
        print("===Número de saques diários atingiu o limite, tente novamente amanhã=== ")
    elif valor > 0:
        saldo -= valor
        extrato += f"Saque:\tR$ {valor:,.2f}\t{datetime.strftime(datetime.now(), "%d/%m/%Y %H:%M:%S")}\n"
        num_saque += 1
        print("===Saque realizado com sucesso===")
    else:
        print("===Valor inválido===")
    return saldo, extrato

def exibir_extrato(saldo, /, *, extrato):
    print("================= EXTRATO =================")
    print("Não foram realizadas movimentações" if not extrato else extrato)
    print(f"\nSaldo:\tR$ {saldo:,.2f}")
    print("===========================================")

def criar_cliente(clientes):
    cpf = input("Informe o CPF (somente os números): ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("---Esse CPF já está cadastrado no sistema---")
        return
    
    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento(dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    clientes.append({"nome": nome, "data_nasciment": data_nascimento, "cpf": cpf, "endereco": endereco})

    print("===Usuário criado com sucesso===")

def criar_conta(agencia, num_conta, clientes):
    cpf = input("Informe o CPF do usuário: ")
    cliente = filtrar_cliente(cpf, clientes)
    
    if cliente:
        print("\n===Conta criada com sucesso===")
        return {"agencia": agencia, "num_conta": num_conta, "cliente": cliente}
    
    print("\n---Cliente não encontrado, operação encerrada---")

def listar_contas(contas):
    for conta in contas:
        linha = f"""
        Agência:\t{conta['agencia']}
        C/C:\t{conta['num_conta']}
        Titular:\t{conta['cliente']['nome']}
        """
        print("=" * 50)
        print(textwrap.dedent(linha))

def main():
    LIMITE_SAQUE = 3
    AGENCIA = "0001"
    
    limite = 500
    saldo = 0
    extrato = ""
    num_saque = 0
    clientes = []
    contas = []

    while True:
        opcao = menu()

        if opcao == 1:
            valor = float(input("Informe o valor a ser depositado: R$ "))
            saldo, extrato = depositar(saldo, valor, extrato)
        elif opcao == 2:
            valor = float(input("Informe o valor a ser sacado: R$ "))
            saldo, extrato = sacar(saldo=saldo,valor=valor,extrato=extrato,limite=limite,num_saque=num_saque,limite_saque=LIMITE_SAQUE)
        elif opcao == 3:
            exibir_extrato(saldo, extrato=extrato)
        elif opcao == 4:
            criar_cliente(clientes)
        elif opcao == 5:
            num_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, num_conta, clientes)
            if conta:
                contas.append(conta)
        elif opcao == 6:
            listar_contas(contas)
        elif opcao == 0:
            print("Sistema finalizado")
            break
        else:
            print("Operação Inválida")

main()