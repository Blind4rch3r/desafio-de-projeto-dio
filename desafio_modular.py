import textwrap


class ATM:
    def __init__(self):
        """Inicializa um objeto ATM com valores padrão para saldo, limite de saque e histórico de transações."""
        self.saldo = 0  # Saldo atual da conta
        self.limite = 500  # Limite máximo de saque por transação
        self.extrato = ""  # String para armazenar o histórico de transações
        self.numero_saques = 0  # Contador para o número de saques
        self.LIMITE_SAQUES = 3  # Número máximo de saques permitidos
        self.AGENCIA = "0001"
        self.usuarios = []
        self.contas = []


    def menu(self):
        menu = """\n
        ================ MENU ================
        [1] Depositar
        [2] Sacar
        [3] Extrato
        [4] Cadastrar Usuário
        [5] Cadastrar Conta
        [6] Listar Contas
        [7] Sair
        => """
        return input(textwrap.dedent(menu))
    
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

if __name__ == "__main__":
    atm = ATM()
    atm.executar()