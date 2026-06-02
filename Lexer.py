import re

# ==========================================
# ANALISADOR LÉXICO (LEXER)
# ==========================================

TOKEN_SPECIFICATION = [
    ('NUMBER',   r'\d+(\.\d+)?'),  # Números inteiros ou decimais
    ('IDENT',    r'[A-Za-z_][A-Za-z0-9_]*'), # Identificadores/variáveis
    ('POW',      r'\*\*|\^'),    # Potência (**) ou ^
    ('PLUS',     r'\+'),           # Soma
    ('MINUS',    r'-'),            # Subtração
    ('MUL',      r'\*'),           # Multiplicação
    ('DIV',      r'/'),            # Divisão
    ('ASSIGN',   r'='),            # Atribuição
    ('LPAREN',   r'\('),           # (
    ('RPAREN',   r'\)'),           # )
    ('LBRACK',   r'\['),           # [
    ('RBRACK',   r'\]'),           # ]
    ('LBRACE',   r'\{'),           # {
    ('RBRACE',   r'\}'),           # }
    ('SKIP',     r'[ \t\n]+'),     # Pular espaços e quebras de linha
    ('MISMATCH', r'.'),            # Qualquer outro caractere inválido
]


def tokenize(code):
    """Transforma o texto bruto em uma lista de tokens."""
    tok_regex = '|'.join(f'(?P<{name}>{regex})' for name, regex in TOKEN_SPECIFICATION)
    tokens = []
    for mo in re.finditer(tok_regex, code):
        kind = mo.lastgroup
        value = mo.group()
        if kind == 'NUMBER':
            tokens.append(('NUMBER', float(value)))
        elif kind == 'IDENT':
            tokens.append(('IDENT', value))
        elif kind == 'SKIP':
            continue
        elif kind == 'MISMATCH':
            raise SyntaxError(f'Caractere inesperado: {value}')
        else:
            tokens.append((kind, value))
    tokens.append(('EOF', None))  # Fim do arquivo/texto
    return tokens