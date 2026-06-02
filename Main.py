from Compiler import compiler

# ==========================================
# PONTO DE ENTRADA / MODO INTERATIVO
# ==========================================

if __name__ == "__main__":
    print("=== COMPILADOR DE EXPRESSÕES MATEMÁTICAS ===")
    print("Operadores suportados: + - * /")
    print("Agrupadores suportados: () [] {}")
    print("Variáveis: ident = expressão (ex: x = 5)")
    print("Potência: ** ou ^ (ex: 2 ** 3 ou 2 ^ 3)")
    print("Digite 'sair' para encerrar.\n")

    while True:
        try:
            expressao = input(">> ")
            if expressao.strip().lower() == "sair":
                print("Encerrando...")
                break
            if expressao.strip() == "":
                continue
            resultado = compiler(expressao)
            print(f"=> Resultado: {resultado}\n")
        except KeyboardInterrupt:
            print("\nEncerrando...")
            break