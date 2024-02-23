from declarations import parse_variable_declarations, parse_variable_declaration, parse_subprogram_declarations
from expressions import parse_expression, parse_simple_expression, parse_term, parse_factor

class PascalParser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.stack = []
        self.current_token = None
        self.index = 0

    def debug_print(self, message):
        print(f"[Debug] {message}")

    def parse(self):
        self.current_token = self.tokens[self.index] if self.tokens else None
        self.debug_print(f"Token atual: {self.current_token}")
        if not self.current_token:
            raise ValueError("No tokens to parse.")
        if self.current_token['Token'] == 'program':
            self.shift()  # Shift para 'program'
            self.next_token()
            if self.current_token['Classificação'] == 'Identificador':
                self.shift()  # Shift para o identificador do programa
                self.next_token()
                if self.current_token['Token'] == ';':
                    self.shift()  # Shift para ';'
                    self.next_token()
                    # Analisa declarações de variáveis e subprogramas, se houver
                    parse_variable_declarations(self)
                    parse_subprogram_declarations(self)
                    # Após declarações, analisa o comando composto principal
                    self.parse_compound_command()
                else:
                    raise SyntaxError("Expected ';' after program name")
            else:
                raise SyntaxError("Expected program name")
        else:
            raise SyntaxError("Expected 'program' at the beginning of the file")


    def shift(self):
        self.debug_print(f"Shift: {self.current_token}")
        self.stack.append(self.current_token)

    def reduce(self, rule, tokens):
        self.debug_print(f"Reduce aplicado para a regra: {rule}")
        if rule == 'variable_declaration':
            # Aqui tokens é a lista de tokens específicos para a declaração de variável
            self.debug_print(f"Declaração de variável reduzida: {tokens}")
            # Não precisa remover tokens da pilha, pois a redução é feita especificamente para os tokens passados
            
        elif rule == 'subprogram_declaration':
            # Processo similar para declarações de subprogramas
            subprogram_declaration = []
            while self.stack and self.stack[-1]['Token'] not in ['procedure']:
                subprogram_declaration.insert(0, self.stack.pop())
            self.debug_print(f"Declaração de subprograma reduzida: {subprogram_declaration}")
            # Adicionar lógica para análise de subprogramas
            
        elif rule == 'compound_command':
            # Redução para comandos compostos
            compound_command = []
            while self.stack and self.stack[-1]['Token'] not in ['begin']:
                compound_command.insert(0, self.stack.pop())
            self.debug_print(f"Comando composto reduzido: {compound_command}")
            # Análise de comandos compostos
 
    def parse_procedure_activation(self):
        self.shift()  # Shift para o identificador do procedimento
        self.next_token()
        if self.current_token['Token'] == '(':
            self.shift()  # Shift para '('
            self.next_token()
            self.parse_expression_list()  # Analisa a lista de expressões
            if self.current_token['Token'] == ')':
                self.shift()  # Shift para ')'
                self.next_token()
            else:
                raise SyntaxError("Expected ')' after expressions in procedure activation")
        self.reduce('procedure_activation')

    def parse_compound_command(self):
        if self.current_token['Token'] == 'begin':
            self.shift()  # Shift para 'begin'
            self.next_token()
            self.parse_commands_optional()  # Analisa os comandos dentro do bloco
            if self.current_token['Token'] == 'end':
                self.shift()  # Shift para 'end'
                self.next_token()
                if self.current_token['Token'] == '.':
                    self.shift()  # Final do programa
                    # Aqui, você pode verificar se a pilha está vazia ou fazer outras verificações finais
                else:
                    pass
                    # Continua a análise se 'end' não for o fim do programa
            else:
                raise SyntaxError("Expected 'end' to close 'begin' block")
        else:
            raise SyntaxError("Expected 'begin' at the start of compound command")

    def next_token(self):
        self.index += 1
        if self.index < len(self.tokens):
            self.current_token = self.tokens[self.index]
            #print(f"Token atual: {self.current_token}")
        else:
            self.current_token = None

    def is_accept_state(self):
        pass  # Implementar conforme necessário

    
    def parse_commands_optional(self):
        while self.current_token and self.current_token['Token'] != 'end':
            self.parse_command()
            
            # Após parsear um comando, verifica se o próximo token é um ';' ou 'end'
            if self.current_token and self.current_token['Token'] == ';':
                self.shift()  # Consome o ';'
                self.next_token()
            elif self.current_token and self.current_token['Token'] != 'end' and self.current_token['Token'] != '.' :
                # Se o token atual não for ';' e o próximo token não for 'end', lança um erro
                raise SyntaxError("Expected ';' or 'end' after command.")



    def parse_compound_command(self):
        if self.current_token['Classificação'] == 'Palavra reservada' and self.current_token['Token'] == 'begin':
            self.shift()  # Shift para 'begin'
            self.next_token()
            self.parse_commands_optional()  # Analisa comandos opcionais dentro do bloco
            if self.current_token['Classificação'] == 'Palavra reservada' and self.current_token['Token'] == 'end':
                self.shift()  # Shift para 'end'
                self.reduce('compound_command')  # Aplica regra de redução para comando composto
            else:
                raise SyntaxError("Expected 'end' at the end of compound command")
        else:
            raise SyntaxError("Expected 'begin' at the start of compound command")

    def parse_arguments(self):
        if self.current_token['Token'] == '(':
            self.shift()  # Shift para '('
            self.next_token()
            self.parse_parameter_list()
            if self.current_token['Token'] == ')':
                self.shift()  # Shift para ')'
                self.next_token()
            else:
                raise SyntaxError("Expected ')' after arguments")
        # Implementar lógica para ε (cadeia vazia)

    def parse_parameter_list(self):
        # Implementação semelhante à de parse_variable_declarations, mas para parâmetros
        pass

    def parse_command(self):
        if self.current_token['Classificação'] == 'Identificador':
            # Verifica o próximo token sem consumi-lo.
            lookahead_token = self.tokens[self.index + 1] if self.index + 1 < len(self.tokens) else None

            if lookahead_token and lookahead_token['Token'] == ':=':
                self.parse_assignment_statement()
            else:
                self.parse_procedure_call()
        elif self.current_token['Token'] == 'if':
            self.parse_if_statement()
        elif self.current_token['Token'] == 'while':
            self.parse_while_statement()
        else:
            raise SyntaxError(f"Unexpected command: {self.current_token['Token']}")

                
    def parse_assignment_statement(self):
        self.shift()  # Shift para o identificador
        self.next_token()
        if self.current_token['Token'] == ':=':
            self.shift()  # Shift para ':='
            self.next_token()
            self.parse_expression()  # Analisa a expressão à direita do ':='
            self.reduce('assignment_statement')  # Aplica redução para a instrução de atribuição
        else:
            raise SyntaxError("Expected ':=' in assignment statement")

        
    def parse_parameter_list(self):
        # Assume que o token atual é o início da lista de parâmetros
        while True:
            self.parse_list_of_identifiers()
            if self.current_token['Token'] == ':':
                self.shift()  # Shift para ':'
                self.next_token()
                self.parse_type()
                if self.current_token['Token'] == ';':
                    self.shift()  # Shift para ';'
                    self.next_token()
                elif self.current_token['Token'] == ')':  # Fim da lista de parâmetros
                    break
                else:
                    raise SyntaxError("Expected ';' or ')' after parameter type")
            else:
                raise SyntaxError("Expected ':' after parameter list")
            
    def parse_procedure_call(self):
        self.shift()  # Shift para o identificador do procedimento
        self.next_token()
        if self.current_token['Token'] == '(':
            self.shift()  # Shift para '('
            self.next_token()
            self.parse_expression_list()  # Analisa a lista de expressões
            if self.current_token['Token'] == ')':
                self.shift()  # Shift para ')'
                self.next_token()
            else:
                raise SyntaxError("Expected ')' after expressions in procedure activation")
        self.reduce('procedure_activation', [self.current_token])


    def parse_if_statement(self):
        self.shift()  # Shift para 'if'
        self.next_token()
        self.parse_expression()  # Analisa a condição do if
        if self.current_token['Token'] == 'then':
            self.shift()  # Shift para 'then'
            self.next_token()
            self.parse_command()  # Analisa o comando a ser executado se a condição for verdadeira
            if self.current_token['Token'] == 'else':
                self.shift()  # Shift para 'else'
                self.next_token()
                self.parse_command()  # Analisa o comando a ser executado se a condição for falsa
        else:
            raise SyntaxError("Expected 'then' after if condition")
        self.reduce('if_statement')

    def parse_while_statement(self):
        self.shift()  # Shift para 'while'
        self.next_token()
        self.parse_expression()  # Analisa a condição do while
        if self.current_token['Token'] == 'do':
            self.shift()  # Shift para 'do'
            self.next_token()
            self.parse_command()  # Analisa o comando a ser repetido enquanto a condição for verdadeira
        else:
            raise SyntaxError("Expected 'do' after while condition")
        self.reduce('while_statement')

