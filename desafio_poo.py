from abc import ABC, abstractmethod, abstractproperty
from datetime import datetime
import textwrap


class Cliente:
    def __init__(self, endereco):
        """
        Inicializa um objeto Cliente com um endereço e uma lista vazia de contas.

        Args:
            endereco (str): O endereço do cliente.
        """
        self.endereco = endereco
        self.contas = []

        def realizar_transacao(self, conta, transacao):
            transacao.registrar(conta)

        def adicionar_conta(self, conta):
            self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):  
        """
        Inicializa um objeto PessoaFisica com os dados pessoais do cliente.

        Args:
            nome (str): Nome completo da pessoa física.
            data_nascimento (str): Data de nascimento da pessoa física no formato (dd-mm-aaaa).
            cpf (str): CPF da pessoa física (somente números).
            endereco (str): Endereço residencial da pessoa física.
        """
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

class Conta:
    def __init__(self, numero, cliente):
        """
        Inicializa uma instância da classe com número e cliente especificados.

        Args:
            numero (int): Número da conta.
            cliente (Cliente): Objeto representando o cliente associado à conta.
        """
        self._saldo = 0  # Saldo atual da conta
        self._numero = 0 # Número da conta
        self._agencia = "0001"  # Numero da agência
        self._cliente = ""  # String para armazenar o histórico de transações
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
            """Executa a operação de saque e atualiza o valor do saldo."""
            numero_saques = len(
                [transacao for transacao in self.historico.transacoes if transacao["tipo"] == "saque"]
            )

            excedeu_limite = valor > self.limite
            excedeu_saques = numero_saques >= self.limite_saques
            
            if excedeu_limite:
                print("\n[-] Operação falhou! Saldo insuficiente. [-]")

            elif excedeu_limite:
                self._saldo -= valor
                print("\n[-] Operação falhou! O valor do saque excede o limite. [-]")

            elif excedeu_saques:
                print("\n[-] Operação falhou! Número máximo de saques excedido. [-]")

            else:
                return super().sacar(valor)

            return False

        def __str__(self):
            return f"""\
                Agência:\t{self.agencia}
                C/C:\t\t{self.numero}
                Titular: {self.cliente.nome}
            """

        def depositar(self, valor):
            """Executa a operação de depósito e atualiza o valor do saldo."""
            if valor > 0:
                self._saldo += valor
                print("\n=== Depósito realizado com sucesso! ===")
                return True
            else:
                print("\n[-] Operação falhou! O valor informado é inválido. [-]")
                return False

            return True

class ContaCorrente(Conta):
    """
    Representa uma conta corrente bancária.

    Esta classe provê métodos para realizar operações bancárias básicas como saque, depósito,
    e exibição de extrato, considerando regras específicas como limite de saque e saldo mínimo.

    Atributos:
        numero (str): Número da conta corrente.
        cliente (Cliente): Objeto representando o titular da conta.
        limite (float): Valor do limite de crédito da conta.
        limite_saques (int): Número máximo de saques permitidos em um período.
    """
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor):
        excedeu_limite = valor > self.limite
        excedeu_saques = self.limite_saques <= 0
        excedeu_saldo = self.saldo < valor

        if excedeu_limite:
            print("\n[-] Operação falhou! O valor do saque excede o limite. [-]")

        elif excedeu_saques:
            print("\n[-] Operação falhou! Número máximo de saques excedido. [-]")

        elif excedeu_saldo:
            print("\n[-] Operação falhou! Saldo insuficiente. [-]")

        elif valor > 0:
            self._saldo -= valor
            self.limite_saques -= 1
            print("\n=== Saque realizado com sucesso! ===")
            return True

        else:
            print("\n[-] Operação falhou! O valor informado é inválido. [-]")

        return False
    
    def depositar(self, valor, /):
        """Lida com transações de depósito adicionando o valor especificado ao saldo da conta e registrando a transação.
        
        Args:
            valor (float): O valor do dinheiro a depositar.
        """
        if valor > 0:
            self.saldo += valor
            self.extrato += f"Depósito: R$ {valor:.2f}\n"
            print("\n=== Depósito realizado com sucesso! ===")
        else:
            print("Operação falhou! O valor informado é inválido.")

        return self.saldo, self.extrato

    def sacar(self, *, valor):
        """Lida com transações de saque subtraindo o valor especificado do saldo da conta, se possível, e registrando a transação.
        
        Args:
            valor (float): O valor do dinheiro a sacar.
        """
        # Verifica se o valor do saque excede o saldo disponível
        if valor > self.saldo:
            print("\nOperação falhou! Você não tem saldo suficiente.")
        # Verifica se o valor do saque excede o limite de saque
        elif valor > self.limite:
            print("\nOperação falhou! O valor do saque excede o limite de R$ 500,00.")
        # Verifica se o número de saques excede o máximo permitido
        elif self.numero_saques >= self.LIMITE_SAQUES:
            print("\nOperação falhou! Número máximo de saques excedido.")
        elif valor > 0:
            self.saldo -= valor
            self.extrato += f"Saque: R$ {valor:.2f}\n"
            self.numero_saques += 1
            print("\n=== Saque realizado com sucesso! ===")
        else:
            print("Operação falhou! O valor informado é inválido.")

        return self.saldo, self.extrato

    def exibir_extrato(self, saldo, /, *, extrato):
        """Imprime o histórico de transações e o saldo atual da conta."""
        print("\n================ EXTRATO ================")
        print("Não foram realizadas movimentações." if not self.extrato else self.extrato)
        print(f"\nSaldo: R$ {self.saldo:.2f}")
        print("==========================================")

    
    def criar_usuario(self, usuarios):
            """
            Cria um novo usuário e o adiciona à lista de usuários.

            Este método solicita ao usuário que informe o CPF, nome completo, data de nascimento e endereço.
            Após receber as informações, verifica se já existe um usuário com o CPF informado na lista de usuários.
            Se o usuário já existir, uma mensagem é exibida e a criação é cancelada.
            Caso contrário, o novo usuário é adicionado à lista com as informações fornecidas.

            Args:
                usuarios (list): Lista de dicionários contendo os usuários já cadastrados.

            Retorna:
                None
            """
            cpf = input("Informe o CPF (somente número): ")
            usuario = self.filtrar_usuario(cpf, usuarios)

            if usuario:
                print("\nJá existe usuário com esse CPF!")
                return

            nome = input("Informe o nome completo: ")
            data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
            endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

            usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})

            print("\n=== Usuário criado com sucesso! ===")

    def filtrar_usuario(self, cpf, usuarios):
        """
        Filtra usuários com base em um CPF fornecido e retorna o primeiro usuário correspondente ou None se nenhum usuário corresponder.
        
        :param cpf: O CPF pelo qual filtrar os usuários
        :param usuarios: Lista de dicionários representando os usuários
        :return: O primeiro dicionário de usuário que corresponde ao CPF fornecido ou None se não houver correspondência
        """
        usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
        return usuarios_filtrados[0] if usuarios_filtrados else None

    def criar_conta(self, agencia, numero_conta, usuarios):
        """
        Cria uma nova conta com a agência, número da conta e lista de usuários fornecidos.
        
        Parâmetros:
            agencia (str): A agência da conta.
            numero_conta (str): O número da conta.
            usuarios (list): Uma lista de usuários.
        
        Retorna:
            dict: Um dicionário contendo a agência, o número da conta e as informações do usuário, se o usuário for encontrado.
            None: Se o usuário não for encontrado.
        """
        cpf = input("Informe o CPF do usuário: ")
        usuario = self.filtrar_usuario(cpf, usuarios)

        if usuario:
            print("\n=== Conta criada com sucesso! ===")
            return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}

        print("\nUsuário não encontrado, fluxo de criação de conta encerrado!")

    def listar_contas(self, contas):
        """
        Gera uma string formatada para cada conta na lista e imprime-a.
        
        :param contas: lista de dicionários representando as contas
        :type contas: list
        :return: None
        """
        for conta in contas:
            linha = f"""\
                Agência:\t{conta['agencia']}
                C/C:\t\t{conta['numero_conta']}
                Titular:\t{conta['usuario']['nome']}
            """
            print("=" * 100)
            print(textwrap.dedent(linha))        

    def executar(self):
        """Executa a interface do ATM, permitindo que o usuário realize depósitos, saques e visualização do histórico de transações."""
        
        
        while True:
            try:
                opcao = self.menu()
                # Lida com a seleção do menu pelo usuário
                if opcao == "1":
                    valor = float(input("Informe o valor do depósito: ").strip())
                    self.depositar(valor)
                
                elif opcao == "2":
                    valor = float(input("Informe o valor do saque: ").strip())
                    self.sacar(valor=valor)
                
                elif opcao == "3":
                    self.exibir_extrato(self.saldo, extrato=self.extrato)
                
                elif opcao == "4":
                    self.criar_usuario(self.usuarios)
                
                elif opcao == "5":
                    numero_conta = len(self.contas) + 1
                    conta = self.criar_conta(self.AGENCIA, numero_conta, self.usuarios)
                    
                    if conta:
                        self.contas.append(conta)
                
                elif opcao == "6":
                    self.listar_contas(self.contas)
                
                elif opcao == "7":
                    break  # Sai do loop e termina o programa
                
                else:
                    print("Operação inválida, por favor selecione novamente a operação desejada.")
            except ValueError:
                print("Erro! Você digitou um valor inválido.")

class Historico:
    def __init__(self):
        self.transacoes = []

    @property
    def transacoes(self):
        return self.transacoes

    def adicionar_conta(self, transacao):
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
        sucesso_transacao = conta.sacar(self._valor)

        if sucesso_transacao:
            conta.historico.adicionar_conta(self)

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self._valor)

        if sucesso_transacao:
            conta.historico.adicionar_conta(self)
