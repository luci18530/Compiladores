from declarations import parse_variable_declarations, parse_variable_declaration, parse_subprogram_declarations


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
            self.debug_print(f"Declaração de subprograma reduzida: {tokens}")
            # Adicionar lógica para análise de subprogramas
            
        elif rule == 'compound_command':
            # Redução para comandos compostos
            self.debug_print(f"Comando composto reduzido: {tokens}")

        elif rule == 'simple_expression':
            self.debug_print(f"Expressão simples reduzida: {tokens}")

        elif rule == 'expression':
            self.debug_print(f"Expressão reduzida: {tokens}")
 
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
            self.shift()
            self.next_token()
            self.parse_commands_optional()
            if self.current_token['Token'] == 'end':
                self.shift()
                self.next_token()
                if self.current_token and self.current_token['Token'] == '.':
                    self.shift()  # Trata o ponto final corretamente.
                    if self.current_token is None:
                        # Verifica se realmente chegamos ao fim dos tokens
                        return
                    else:
                        raise SyntaxError("No additional tokens expected after program end.")
                else:
                    raise SyntaxError("Expected '.' at the end of the program")
            else:
                raise SyntaxError("Expected 'end'")
        else:
            raise SyntaxError("Expected 'begin'")



    def set_accept_state(self):
        self.is_accept_state = True

    def is_accept_state(self):
        return self.is_accept_state


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

            # Ignora comentários que podem aparecer entre comandos
            while self.current_token and self.current_token['Token'].startswith('{'):
                self.shift()  # Ignora o comentário
                self.next_token()

            if self.current_token and self.current_token['Token'] == ';':
                self.shift()  # Consome o ';'
                self.next_token()
                # Novamente, ignora comentários que podem aparecer após ';'
                while self.current_token and self.current_token['Token'].startswith('{'):
                    self.shift()  # Ignora o comentário
                    self.next_token()



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
            print("aa")
            # Olha à frente para verificar se os próximos tokens indicam uma instrução de atribuição.
            lookahead_token = self.tokens[self.index + 1] if self.index + 1 < len(self.tokens) else None
            print(lookahead_token)
            if lookahead_token['Token'] == ':':
                # Se o próximo token é ':', verifica se o subsequente é '=', indicando uma atribuição.
                self.parse_assignment_statement()
            elif lookahead_token['Token'] == ':=':
                # Se o próximo token é ':=', então a instrução de atribuição começa com o identificador atual.
                self.parse_assignment_statement()
            else:
                # Outros casos para identificadores que não são parte de uma atribuição (por exemplo, chamada de procedimento).
                self.parse_procedure_call()
        elif self.current_token['Token'] == 'if':
            self.parse_if_statement()
        elif self.current_token['Token'] == 'while':
            self.parse_while_statement()
        else:
            raise SyntaxError(f"Unexpected command: {self.current_token['Token']}")
        
    def parse_assignment_statement(self):
        # Verifica se o token atual é um identificador, o que é esperado no início de uma instrução de atribuição.
        if self.current_token['Classificação'] == 'Identificador':
            
            left_side_token = self.current_token  # Guarda o token do lado esquerdo da atribuição.
            self.shift()  # Shift para o identificador.
            self.next_token()
            # Verifica se os próximos dois tokens formam o operador de atribuição ':='.
            if self.current_token['Token'] == ':=':
                print('entroi')
                self.shift()  # Shift para ':='.
                self.next_token()
                # Analisa a expressão do lado direito da atribuição.
                self.parse_expression()
                # Após analisar a expressão, aplica a redução para a instrução de atribuição.
                self.reduce('assignment_statement', [left_side_token])
            else:
                raise SyntaxError("Invalid syntax in assignment statement. Expected ':='.")
        else:
            raise SyntaxError("Expected an identifier at the beginning of an assignment statement.")


        
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

    def parse_simple_expression(self):
        temp_tokens = []
        # Esta função analisa uma expressão simples, que pode conter operadores aditivos
        if self.current_token['Classificação'] in ['Número inteiro', 'Número real', 'Identificador']:
            temp_tokens.append(self.current_token)
            self.shift()  # Consumir o número ou identificador
            self.next_token()
        while self.current_token['Classificação'] in ['Operador aditivo', 'Operador multiplicativo']:
            temp_tokens.append(self.current_token)
            self.shift()  # Consumir o operador
            self.next_token()
            if self.current_token['Classificação'] in ['Número inteiro', 'Número real', 'Identificador']:
                temp_tokens.append(self.current_token)
                self.shift()  # Consumir o próximo número ou identificador
                self.next_token()
        self.reduce('simple_expression', temp_tokens)


    def parse_expression(self):
        temp_tokens = []
        # Esta função analisa uma expressão, que pode ser uma expressão simples ou uma expressão com um operador relacional
        self.parse_simple_expression()
        if self.current_token['Classificação'] == 'Operador relacional':
            temp_tokens.append(self.current_token)
            self.shift()  # Consumir o operador relacional
            self.next_token()
            self.parse_simple_expression()
        self.reduce('expression', temp_tokens)

    def parse_term(self):
        temp_tokens = []
        # Esta função analisa um termo, que pode ser um fator ou uma sequência de fatores multiplicados ou divididos
        self.parse_factor()
        while self.current_token['Classificação'] == 'Operador multiplicativo':
            temp_tokens.append(self.current_token)
            self.shift()  # Consumir o operador multiplicativo
            self.next_token()
            self.parse_factor()
        self.reduce('term', temp_tokens )


    def parse_factor(self):
        temp_tokens = []
        # Esta função analisa um fator, que pode ser um número, uma variável ou uma expressão entre parênteses
        if self.current_token['Classificação'] in ['Número inteiro', 'Número real', 'Identificador']:
            temp_tokens.append(self.current_token)
            self.shift()  # Consumir o número, real ou identificador
            
        elif self.current_token['Token'] == '(':
            temp_tokens.append(self.current_token)
            self.shift()  # Consumir '('
            self.next_token()
            self.parse_expression()
            if self.current_token['Token'] == ')':
                temp_tokens.append(self.current_token)
                self.shift()  # Consumir ')'
                self.next_token()
            else:
                raise SyntaxError("Esperado ')' após a expressão")
        else:
            raise SyntaxError("Fator inválido")
        self.reduce('factor', temp_tokens)


