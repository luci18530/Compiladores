def parse_simple_expression(self):
    if self.current_token['Classificação'] in ['Sinal', 'Identificador', 'Número inteiro', 'Número real']:
        self.shift()  # Shift para o sinal, identificador ou número
        self.next_token()
        while self.current_token['Classificação'] in ['Operador aditivo', 'Operador multiplicativo']:
            self.shift()  # Shift para o operador
            self.next_token()
            self.shift()  # Shift para o próximo termo/fator
            self.next_token()
    self.reduce('simple_expression')

def parse_expression(self):
    self.parse_simple_expression()
    if self.current_token['Classificação'] == 'Operador relacional':
        self.shift()  # Shift para o operador relacional
        self.next_token()
        self.parse_simple_expression()
    self.reduce('expression')

def parse_term(self):
    self.parse_factor()
    while self.current_token['Classificação'] == 'Operador multiplicativo':
        self.shift()  # Shift para o operador multiplicativo
        self.next_token()
        self.parse_factor()
    self.reduce('term')

def parse_factor(self):
    if self.current_token['Classificação'] in ['Identificador', 'Número inteiro', 'Número real']:
        self.shift()  # Shift para o identificador ou número
    elif self.current_token['Token'] == '(':
        self.shift()  # Shift para '('
        self.next_token()
        self.parse_expression()
        if self.current_token['Token'] != ')':
            raise SyntaxError("Expected ')' after expression")
        self.shift()  # Shift para ')'
    elif self.current_token['Token'] == 'not':
        self.shift()  # Shift para 'not'
        self.next_token()
        self.parse_factor()
    else:
        raise SyntaxError("Invalid factor")
    self.next_token()
    self.reduce('factor')

