from __future__ import annotations
import re


def extrair_numeros_cpf(cpf:str|int)->str:
    cpf_formatado = str(cpf).replace('.', '').replace('-', '')
    cpf_number_list = re.findall('\d', cpf_formatado)
    cpf_numeros = ''.join(cpf_number_list if cpf_number_list is not None else [])
    return cpf_numeros

class Usuario:
    def __init__(self, *, nome:str, data_nascimento:str, cpf:str, endereco:str):
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf
        self.endereco = endereco
        self.regex_pattern = '%d'
        self.contas = []
    
    def validar_dados(self):
        # Validar e mantêr apenas letras do CPF
        contem_erros = False
        self.cpf = extrair_numeros_cpf(self.cpf)
        if len(self.cpf) != 11:
            print('CPF do Usuário com número incorreto de dígitos')
            contem_erros = True
        # Validar endereço se contém separadores e se contém número correto de informações
        # Formato: logradouro - número - bairro - cidade/(sigla do estado)
        if not '-' in self.endereco:
            print('Endereço do Usuário não contém o separador "-"')
            contem_erros = True
        else:
            endereco_separado = self.endereco.split('-')
            if len(endereco_separado) != 4:
                print('Número incorreto de informações no endereço do usuário')
                contem_erros = True
            if '/' not in endereco_separado[-1].replace('\\', '/'):
                print('Sigla do Estado do Usuário não encontrada após a cidade')
                contem_erros = True
            else:
                if len(endereco_separado[-1].replace('\\', '/').split('/')[-1]) != 2:
                    print('Sigla do estado do Usuário contém mais de duas letras')
                    contem_erros = True
        return not contem_erros
    
    def adicionar_conta(self, conta:Conta):
        self.contas.append(conta)
        print('Conta adicionada ao usuário')
        
        
class Conta:
    def __init__(self, agencia:str|int, conta:str|int, usuario:Usuario):
        self.agencia = str(agencia).zfill(4)
        self.conta = str(conta).zfill(8)
        self.usuario = usuario
        print('Conta criada com sucesso')
        self.usuario.adicionar_conta(conta=conta)
    

def deposito(saldo:int, valor:int, extrato:str,/)->tuple[int, str]:
    if valor > 0:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"
    else:
        print("Operação falhou! O valor informado é inválido.")
    return saldo, extrato

def saque(*, saldo:int, valor:int, extrato:str, limite:int, numero_saques:int, limite_saques:int)->tuple[int, str, int]:
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("Operação falhou! Você não tem saldo suficiente.")
    elif excedeu_limite:
        print("Operação falhou! O valor do saque excede o limite.")
    elif excedeu_saques:
        print("Operação falhou! Número máximo de saques excedido.")
    elif valor > 0:
        saldo -= valor
        extrato += f"Saque: R$ {valor:.2f}\n"
        numero_saques += 1
        print('Saque realizado com sucesso!')
    else:
        print("Operação falhou! O valor informado é inválido.")
    return saldo, extrato, numero_saques

def print_extrato(saldo:int, /, *, extrato:str)->None:
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("==========================================")
    
def criar_usuario(*, lista_usuarios:dict, nome:str, data_nascimento:str, cpf:str, endereco:str)->dict:
    usuario = Usuario(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)
    dados_ok = usuario.validar_dados()
    if dados_ok:
        cpf_validado = usuario.cpf
        if lista_usuarios.get(cpf_validado):
            print('Usuário já cadastrado no sistema')
        else:
            lista_usuarios[cpf_validado] = usuario
            print('Usuário adicionado no sistema')
    else:
        print('Erro na validação de dados do usuário')
    return lista_usuarios

def criar_conta_padronizada(*, lista_contas:list, usuario:str)->list:
    # Cria conta seguindo a fórmula
    # Agência sempre igual '0001'
    # Conta = início em 1 e incrementado em 1 a cada conta criada
    if lista_contas:
        ultima_conta = lista_contas[-1]
        agencia = ultima_conta.agencia
        conta = int(ultima_conta.conta) + 1
    else:
        agencia = '0001'
        conta = 1
    lista_contas = criar_conta(lista_contas=lista_contas, agencia=agencia, conta=conta, usuario=usuario)

def criar_conta(*, lista_contas:list, agencia:str|int, conta:str|int, usuario:str)->list:
    # Cria conta e adiciona na lista de contas existente
    conta = Conta(agencia=agencia, conta=conta, usuario=usuario)
    lista_contas.append(conta)
    return lista_contas
    
if __name__ == '__main__':
    menu = """

[d] Depositar
[s] Sacar
[e] Extrato
[u] Usuário
[c] Conta
[q] Sair

=> """

    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    usuarios = {}
    contas = []
    LIMITE_SAQUES = 3

    while True:

        opcao = input(menu)

        # Opção Depósito
        if opcao == "d":
            valor = float(input("Informe o valor do depósito: "))
            saldo, extrato = deposito(saldo, valor, extrato)

        # Opção Saque
        elif opcao == "s":
            valor = float(input("Informe o valor do saque: "))
            saldo, extrato, numero_saques = saque(saldo=saldo, valor=valor, extrato=extrato, limite=limite, numero_saques=numero_saques, limite_saques=LIMITE_SAQUES)

        # Opção Extrato
        elif opcao == "e":
            print_extrato(saldo, extrato=extrato)

        # Opção criar Usuário
        elif opcao == "u":
            nome = input("Informe o nome do usuário: ")
            data_nascimento = input("Informe a data de nascimento do usuário no formato (dd/mm/yyyy): ")
            cpf = input("Informe o CPF do usuário no formato XXX.XXX.XXX-XX: ")
            endereco = input("Informe o endereço do usuário no formato logradouro - número - bairro - cidade/(sigla do estado): ")
            criar_usuario(lista_usuarios=usuarios, nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)
        
        # Opção criar Conta
        elif opcao == "c":
            cpf = input("Informe o CPF do usuário dono da conta no formato XXX.XXX.XXX-XX: ")
            cpf = extrair_numeros_cpf(cpf)
            usuario = usuarios.get(cpf)
            if not usuario:
                print('Não existe usuário cadastrado com esse CPF')
            else:
                criar_conta_padronizada(lista_contas=contas, usuario=usuario)
            
         # Opção Quit (encerrar)
        elif opcao == "q":
            break
        
        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")