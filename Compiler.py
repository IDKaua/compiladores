from Lexer import tokenize
from Parser import Parser

# Ambiente (tabela de símbolos) persistente entre chamadas
ENV = {}

# ==========================================
# COMPILADOR / INTERPRETADOR (EXECUÇÃO)
# ==========================================

def compiler(code):
    """
    Executa o pipeline completo:
    1. Análise Léxica  (Lexer)
    2. Análise Sintática e Avaliação (Parser)
    """
    try:
        # Passo 1: Análise Léxica
        tokens = tokenize(code)

        # Passo 2 e 3: Análise Sintática e Avaliação (compartilha ENV)
        parser = Parser(tokens, ENV)
        result = parser.parse()

        return result
    except Exception as e:
        return f"Erro: {e}"