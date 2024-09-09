import datetime as dt

LIMITE_SAQUE = 3
saldo = 0
num_saque = 0
num_deposito = 0
opcao = -1
extrato = []

while opcao != 0:
    opcao = int(input(f"""
===============================MENU===============================
                        [1] - DEPOSITAR
                        [2] - SACAR
                        [3] - EXTRATO
                        [0] - SAIR

                Número de saques feitos hoje: {num_saque}
==================================================================
"""))
    if opcao == 1:
        deposito = float(input("Informe o valor a ser depositado: R$"))
        if deposito < 0:
            print("Valoar digitado inválido, tente novamente")
        else:
            saldo += deposito
            print(f"Depósto efetuado com sucesso, seu saldo é de: R${saldo:,.2f}")
            num_deposito += 1
            extrato.append(f"{num_deposito}º Depósito: R${saldo:,.2f}")
    elif opcao == 2:
        if num_saque == LIMITE_SAQUE:
            print("O limite diário de saques foi excedido, tente novamente amanhã.")
        else:
            saque = float(input("Informe o valor a ser sacado: R$"))
            if saque < 500:
                if saque <= 0 or saque >= saldo:
                    print("O saldo é inferior ao saque ou é menor que 0, tente novamente.")
                else:
                    saldo -= saque
                    num_saque += 1
                    extrato.append(f"{num_saque}º Saque: R${saque:,.2f}")
            else:
                print("Valor digitado superior ao limite de R$500,00, digite uma valor inferior ao limite para efetuar o saque.")
        print(f"Seu saldo é de: R${saldo:,.2f}")
    elif opcao == 3:
        print(f"Seu saldo atual é de: R${saldo:,.2f}\n{extrato}")
    elif opcao > 3 or opcao < -1:
        print("Operação informada inválida, tente novamente.")
    else:
        print("Obrigado por utilizar nosso sistema, até mais.")
        break
