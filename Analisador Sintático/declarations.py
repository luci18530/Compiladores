#métodos relacionados ao parsing de declarações

def parse_variable_declarations(self):
        temp_declaration_tokens = []
        if self.current_token['Token'] == 'var':
            self.shift()  # Shift para 'var'
            temp_declaration_tokens.append(self.current_token)
            self.next_token()
            while self.current_token and self.current_token['Classificação'] == 'Identificador':
                parse_variable_declaration(self)
                # Verifica se o próximo token é um ponto e vírgula que termina a declaração da variável
                if self.current_token['Token'] == ';':
                    self.shift()  # Shift para ';'
                    temp_declaration_tokens.append(self.current_token)
                    self.reduce('variable_declaration', temp_declaration_tokens)  # Chama reduce para a declaração de variável
                    self.next_token()
                else:
                    raise SyntaxError("Expected ';' after variable declaration")

def parse_variable_declaration(self):
    # Inicializa uma lista temporária para armazenar os tokens da declaração atual
    temp_declaration_tokens = []

    # Analisa identificadores e tipos
    while self.current_token['Classificação'] == 'Identificador' or self.current_token['Token'] == ',' or self.current_token['Token'] == ':':
        temp_declaration_tokens.append(self.current_token)
        self.shift()  # Shift para o identificador, vírgula ou dois pontos
        self.next_token()

        # Espera-se um tipo de dado após os dois pontos
    if self.current_token['Token'] in ['integer', 'real', 'boolean']:
        temp_declaration_tokens.append(self.current_token)
        self.shift()  # Shift para o tipo de dado
        self.next_token()
    else:
        raise SyntaxError("Expected a data type (integer, real, boolean) after ':'")
        

    # Aplica a redução imediatamente após analisar uma declaração de variável completa
    self.reduce('variable_declaration', temp_declaration_tokens)

def parse_subprogram_declarations(self):
    if self.current_token['Classificação'] == 'Palavra reservada' and self.current_token['Token'] == 'procedure':
        self.shift()  # Shift para 'procedure'
        self.next_token()
        if self.current_token['Classificação'] == 'Identificador':
            self.shift()  # Shift para o identificador do procedimento
            self.next_token()
            self.parse_arguments()  # Analisa os argumentos do procedimento
            if self.current_token['Token'] == ';':
                self.shift()  # Shift para ';'
                self.next_token()
                self.parse_variable_declarations()  # Repete a análise para declarações de variáveis dentro do subprograma
                self.parse_subprogram_declarations()  # Repete a análise para possíveis subprogramas aninhados
                self.parse_compound_command()  # Analisa o comando composto que define o corpo do subprograma
                self.reduce('subprogram_declaration')  # Aplica a regra de redução para declaração de subprograma
            else:
                raise SyntaxError("Expected ';' after procedure declaration")
        else:
            raise SyntaxError("Expected procedure name identifier after 'procedure'")
        
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