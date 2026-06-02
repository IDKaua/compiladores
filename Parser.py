# ==========================================
# ANALISADOR SINTÁTICO (PARSER)
# ==========================================

class Parser:
    """
    Organiza os tokens em uma estrutura de árvore baseada
    na ordem de precedência e avalia a expressão.
    """

    def __init__(self, tokens, env=None):
        self.tokens = tokens
        self.pos = 0
        self.current_token = self.tokens[self.pos]
        self.env = env if env is not None else {}

    def error(self, message="Erro de sintaxe"):
        raise SyntaxError(message)

    def advance(self):
        """Avança para o próximo token."""
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]

    def eat(self, token_type):
        """Consome o token atual se ele for do tipo esperado."""
        if self.current_token[0] == token_type:
            self.advance()
        else:
            self.error(f"Esperado token {token_type}, mas encontrado {self.current_token[0]}")

    def factor(self):
        """Fator: Números ou expressões entre (), [], {}."""
        token = self.current_token

        if token[0] == 'NUMBER':
            self.eat('NUMBER')
            return token[1]

        elif token[0] == 'IDENT':
            # Variável: retorna o valor armazenado
            name = token[1]
            self.eat('IDENT')
            if name in self.env:
                return self.env[name]
            else:
                self.error(f"Variável não definida: {name}")

        elif token[0] == 'LPAREN':
            self.eat('LPAREN')
            result = self.expr()
            self.eat('RPAREN')
            return result

        elif token[0] == 'LBRACK':
            self.eat('LBRACK')
            result = self.expr()
            self.eat('RBRACK')
            return result

        elif token[0] == 'LBRACE':
            self.eat('LBRACE')
            result = self.expr()
            self.eat('RBRACE')
            return result

        self.error(f"Fator inválido: {token[1]}")

    def term(self):
        """Termo: Multiplicação e Divisão (maior precedência)."""
        node = self.power()
        while self.current_token[0] in ('MUL', 'DIV'):
            op = self.current_token[0]
            self.advance()
            if op == 'MUL':
                node = node * self.power()
            elif op == 'DIV':
                denominator = self.power()
                if denominator == 0:
                    raise ZeroDivisionError("Divisão por zero não é permitida.")
                node = node / denominator
        return node

    def power(self):
        """Potência: operador right-associative (**) ou ^."""
        node = None
        # Para associatividade à direita: parse base e se vir POW, compute base ** power()
        if self.current_token[0] in ('NUMBER', 'IDENT', 'LPAREN', 'LBRACK', 'LBRACE'):
            node = self.factor()
            if self.current_token[0] == 'POW':
                self.eat('POW')
                exponent = self.power()
                node = node ** exponent
            return node
        self.error(f"Fator inválido para potência: {self.current_token}")

    def expr(self):
        """Expressão: Soma e Subtração (menor precedência)."""
        node = self.term()
        while self.current_token[0] in ('PLUS', 'MINUS'):
            op = self.current_token[0]
            self.advance()
            if op == 'PLUS':
                node = node + self.term()
            elif op == 'MINUS':
                node = node - self.term()
        return node

    def parse(self):
        """Ponto de entrada do parser. Retorna o resultado da expressão."""
        # Suporta atribuição: IDENT = expr
        if self.current_token[0] == 'IDENT' and self.pos + 1 < len(self.tokens) and self.tokens[self.pos + 1][0] == 'ASSIGN':
            name = self.current_token[1]
            self.eat('IDENT')
            self.eat('ASSIGN')
            value = self.expr()
            self.env[name] = value
            if self.current_token[0] != 'EOF':
                self.error("Tokens extras encontrados no final da atribuição.")
            return value

        result = self.expr()
        if self.current_token[0] != 'EOF':
            self.error("Tokens extras encontrados no final da expressão.")
        return result