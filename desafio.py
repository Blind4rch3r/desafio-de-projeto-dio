class ATM:
    def __init__(self):
        """Inicializa um objeto ATM com valores padrão para saldo, limite de saque e histórico de transações."""
        self.saldo = 0  # Saldo atual da conta
        self.limite = 500  # Limite máximo de saque por transação
        self.extrato = ""  # String para armazenar o histórico de transações
        self.numero_saques = 0  # Contador para o número de saques
        self.LIMITE_SAQUES = 3  # Número máximo de saques permitidos

    def depositar(self, valor):
        """Lida com transações de depósito adicionando o valor especificado ao saldo da conta e registrando a transação.
        
        Args:
            valor (float): O valor do dinheiro a depositar.
        """
        if valor > 0:
            self.saldo += valor
            self.extrato += f"Depósito: R$ {valor:.2f}\n"
        else:
            print("Operação falhou! O valor informado é inválido.")

    def sacar(self, valor):
        """Lida com transações de saque subtraindo o valor especificado do saldo da conta, se possível, e registrando a transação.
        
        Args:
            valor (float): O valor do dinheiro a sacar.
        """
        # Verifica se o valor do saque excede o saldo disponível
        if valor > self.saldo:
            print("Operação falhou! Você não tem saldo suficiente.")
        # Verifica se o valor do saque excede o limite de saque
        elif valor > self.limite:
            print("Operação falhou! O valor do saque excede o limite de R$ 500,00.")
        # Verifica se o número de saques excede o máximo permitido
        elif self.numero_saques >= self.LIMITE_SAQUES:
            print("Operação falhou! Número máximo de saques excedido.")
        elif valor > 0:
            self.saldo -= valor
            self.extrato += f"Saque: R$ {valor:.2f}\n"
            self.numero_saques += 1
        else:
            print("Operação falhou! O valor informado é inválido.")

    def exibir_extrato(self):
        """Imprime o histórico de transações e o saldo atual da conta."""
        print("\n================ EXTRATO ================")
        print("Não foram realizadas movimentações." if not self.extrato else self.extrato)
        print(f"\nSaldo: R$ {self.saldo:.2f}")
        print("==========================================")

    def executar(self):
        """Executa a interface do ATM, permitindo que o usuário realize depósitos, saques e visualização do histórico de transações."""
        
        menu ="\n[1] Depositar\n"
        menu += "[2] Sacar\n"
        menu += "[3] Extrato\n"
        menu += "[4] Sair\n"
        menu += "\n=> "
        
        while True:
            try:
                opcao = input(menu).strip()
                # Lida com a seleção do menu pelo usuário
                if opcao == "1":
                    valor = float(input("Informe o valor do depósito: ").strip())
                    self.depositar(valor)
                elif opcao == "2":
                    valor = float(input("Informe o valor do saque: ").strip())
                    self.sacar(valor)
                elif opcao == "3":
                    self.exibir_extrato()
                elif opcao == "4":
                    break  # Sai do loop e termina o programa
                else:
                    print("Operação inválida, por favor selecione novamente a operação desejada.")
            except ValueError:
                print("Erro! Você digitou um valor inválido.")

if __name__ == "__main__":
    atm = ATM()
    atm.executar()



