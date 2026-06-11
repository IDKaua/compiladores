# Compilador de Expressões Matemáticas
ALUNO: Flávio Miguel Guilherme dos Santos - 01647888
ALUNO: Pabllo Wyllams Tavares Barbosa - 01633453
ALUNO: Eduardo Leandro Santos - 01670259
ALUNO: Cícero Barros da Silva - 01638161
ALUNO: Edillan Kauã da Silva Oliveira - 01611518
Este projeto é um compilador/interpretador híbrido desenvolvido em **Python** para análise,
validação e execução de expressões matemáticas complexas e atribuição de variáveis em
tempo real. Ele utiliza um pipeline de compilação clássico composto por um Analisador
Léxico (Lexer) baseado em Expressões Regulares e um Analisador Sintático (Parser)
Descendente Recursivo.
## Como o Compilador Funciona:
O funcionamento do interpretador é dividido em 3 etapas sequenciais que transformam o
texto bruto digitado pelo usuário em um resultado numérico final:
### 1. Análise Léxica (Lexer / Tokenizer)
Quando você insere uma expressão (ex: `x = 2 * (3 + 5)`), o texto bruto é enviado para a
função `tokenize()`.
* O **Lexer** varre a string caractere por caractere utilizando Expressões Regulares (`re`).
* Ele agrupa os caracteres em unidades lógicas chamadas **Tokens** (uma estrutura
contendo o tipo do elemento e o seu valor).
* Espaços em branco são ignorados automaticamente (`SKIP`).
* Se um caractere inválido for digitado (como `@` ou `$`), o padrão `MISMATCH` é acionado
e o programa interrompe a execução acusando um erro de sintaxe.
* Ao final do texto, um token especial `EOF` (End of File) é adicionado para marcar o
término da leitura.
### 2. Análise Sintática (Parser)
Com a lista de tokens gerada, a classe `Parser` assume o controle através do método
`parse()`. Este componente utiliza a técnica de **Análise Descendente Recursiva**
(*Recursive Descent Parsing*).
* O Parser valida se a ordem dos tokens respeita as regras gramaticais estabelecidas.
* Cada nível de precedência matemática possui uma função dedicada, processada de cima
para baixo:
1. `expr()`: Gerência operações de menor precedência (**Soma** `+` e **Subtração** `-`).
2. `term()`: Gerência operações intermediárias (**Multiplicação** `*` e **Divisão** `/`).
3. `power()`: Gerencia a **Exponenciação** (`**` ou `^`).
4. `factor()`: Gerencia a base (**Números**, **Variáveis** ou expressões aninhadas dentro
de agrupadores).
### 3. Análise Semântica e Avaliação DiretaDiferente de compiladores tradicionais que geram uma Árvore Sintática Abstrata (AST)
explícita para depois convertê-la em código de máquina, este projeto executa uma
**avaliação em tempo de execução**. À medida que o Parser valida a estrutura do código,
ele calcula imediatamente os valores aritméticos associados.
---
## Recursos Especiais Implementados
### Associatividade à Direita na Potência
Matematicamente, potências sequenciais devem ser resolvidas da direita para a esquerda
($2^{3^2} = 2^9 = 512$). O compilador implementa isso nativamente na função `power()`
através de recursão à direita:
```python
# Se encontrar o operador POW, chama recursivamente a si mesmo para resolver o
expoente primeiro
exponent = self.power()
node = node ** exponent
```
### Múltiplos Agrupadores Equivalentes

O fator aceita de forma equivalente o isolamento de expressões por Parênteses (),
Colchetes [] e Chaves {}, permitindo expressões altamente legíveis como:

```
x = {2 * [3 + (5 ** 2)]}
=> Resultado: 56.0
```

### Tratamento Robustecido de Erros

O sistema está protegido contra falhas críticas comuns em tempo de execução:

● Divisão por Zero: A sub-rotina de divisão verifica se o denominador resulta em 0 e
lança uma exceção limpa (ZeroDivisionError) em vez de quebrar a aplicação.

● Variáveis Não Definidas: Tentar chamar uma variável que não existe no dicionário
ENV gera uma mensagem de erro controlada avisando que a variável não foi
definida.

● Tokens Extras: Garante que expressões mal formadas ao final (como 2 + 3 5 +)
acionem um erro de sintaxe por não consumirem o token EOF.
Tecnologias Utilizadas

● Python 3.x (Sem dependências externas, utiliza apenas a biblioteca nativa re).
