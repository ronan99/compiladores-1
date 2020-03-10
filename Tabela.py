tabela_de_simbolos = {}
lista_de_tokens = []
tipo_esperado = ""

# reservadas = ('var', 'integer', 'real', 'if', 'then')
# terminais = (' ', '\t', '\n', ',', ':', ':=', '+', ',', ';', '=')
# delimitador = (',', ':', ';')
# operador = ('+', '-', ':=', '=')


def error_expected(token, expected):
    print("Erro de sintaxe: na linha {} o esperado era '{}' , mas a entrada foi '{}'"
          "".format(token.index, expected, token.value))
    exit(2)


def errorMessage(message):
    print("Erro: " + message)
    exit(66)


def searchTable(token):
    global tabela_de_simbolos
    aux = tabela_de_simbolos.get(token.value)
    return aux


def insertSimbol(token):
    global tabela_de_simbolos
    insertTs = {token.value: {"Index": token.index}}
    buscaTs = searchTable(token)
    if (buscaTs == None):
        tabela_de_simbolos.update(insertTs)
    else:
        errorMessage("Variavel declarada anteriormente:" + token.value)


def print_table():
    print('\nTabela de Simbolos:\n')
    for x in tabela_de_simbolos:
        print('Nome:', x)
        for y in tabela_de_simbolos[x]:
            print(y, ':', tabela_de_simbolos[x][y])
        print()


def check(tokens):
    if (not tokens):
        errorMessage("Cadeia incompleta")


def Z(tokens):
    I(tokens)
    S(tokens)
    print_table()


def I(tokens):
    check(tokens)
    token = tokens.pop(0)
    if(token.value != "var"):
        error_expected(token, "var")

    D(tokens)


def D(tokens):
    check(tokens)
    L(tokens)
    token = tokens.pop(0)
    if(token.value != ":"):
        error_expected(token, ":")

    K(tokens)

    O(tokens)


def S(tokens):
    global tipo_esperado
    if (not tokens):
        errorMessage("Cadeia incompleta, esperado: Identificador ou Condição")

    token = tokens.pop(0)

    if(token.type != "identificador" and token.value != "if"):
        error_expected(token, "Identificador ou condição")

    if(token.type == "identificador"):
        tsResponse = searchTable(token)

        if (tsResponse == None):
            errorMessage("Variavel '{}' nao declarada na linha {}".format(
                token.value, token.index))
        tipo_esperado = tsResponse.get("Tipo")
        tk = tokens.pop(0)

        if (tk.value != ':='):
            error_expected(tk, ':=')

        E(tokens)

    elif(token.value == 'if'):
        E(tokens)

        if (not tokens):
            errorMessage(
                "de sintaxe: linha {} | Esperado: then | Entrada: {}".format(tk.index, ''))
        tk = tokens.pop(0)

        if (tk.value != 'then'):
            error_expected(tk, 'Palavra reservada')

        tipo_esperado = ""
        S(tokens)


def L(tokens):
    check(tokens)
    token = tokens.pop(0)
    if(token.type != "identificador"):
        error_expected(token, "Identificador")
    insertSimbol(token)
    lista_de_tokens.append(token)
    X(tokens)


def X(tokens):
    check(tokens)
    tk = tokens[0]
    if(tk.value != ','):
        return
    tokens.pop(0)
    L(tokens)


def K(tokens):
    check(tokens)
    token = tokens.pop(0)
    if(token.value not in ("integer", "real")):
        error_expected(token, "Palavra Reservada")
    for aux in lista_de_tokens:
        busca = searchTable(aux)
        busca.update({"Tipo": token.value})

    lista_de_tokens.clear()


def O(tokens):
    check(tokens)

    if(not tokens):
        errorMessage("Cadeia incompleta")

    tk = tokens[0]

    if(tk.value != ";"):
        return
    tokens.pop(0)
    D(tokens)


def E(tokens):
    check(tokens)
    T(tokens)
    R(tokens)


def T(tokens):
    global tipo_esperado
    check(tokens)
    token = tokens.pop(0)
    if (token.type != 'identificador'):
        error_expected(token, 'idenficador')
    tsResponse = searchTable(token)

    if (tsResponse == None):
        errorMessage("Variavel nao declarada")

    if (tipo_esperado == ""):
        tipo_esperado = tsResponse.get("Tipo")
    else:
        tsType = tsResponse.get("Tipo")
        if (not tipo_esperado == tsType):
            errorMessage("Tipo incompativel: esperava-se tipo: %s, linha: %s, variavel: %s" %
                         (tipo_esperado, tsResponse.get("Index"), token.value))


def R(tokens):
    if (not tokens):
        return

    tk = tokens[0]

    if (tk.value == '+'):
        tk = tokens.pop(0)
        T(tokens)
        R(tokens)
