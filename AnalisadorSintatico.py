from Tabela import *
import nltk


path = input("Digite o nome do arquivo a ser verificado:\n")
print("\n")


# Palavras reservadas, delimitadores, operadores e terminais
reservadas = ('var', 'integer', 'real', 'if', 'then')
terminais = (' ', '\t', '\n', ',', ':', ':=', '+', ',', ';', '=')
delimitador = (',', ':', ';')
operador = ('+', '-', ':=', '=')


# Classe de token
class Token:
    def __init__(self, _value, _type, _index):
        self.type = _type
        self.value = _value
        self.index = _index

    def __str__(self):
        return "'{}' {} linha {}".format(self.value, self.type, self.index)

    __repr__ = __str__


# Função para caractere inválido
def invalid_char(aux):
    print("Caractere invalido: '" + aux + "'")
    exit(66)  # execute order 66


# Main começa aqui
if __name__ == '__main__':
    with open(path, 'r') as input_file:
        tokens = []

        for i, l in enumerate(input_file):
            tokenizador = nltk.WordPunctTokenizer()
            lista_de_termos = tokenizador.tokenize(l)
            for j in lista_de_termos:
                if j in reservadas:
                    tokens.append(Token(j, "reservada", i))
                elif j in delimitador:
                    tokens.append(Token(j, "delimitador", i))
                elif j in operador:
                    tokens.append(Token(j, "operador", i))
                elif j.isalpha():
                    tokens.append(Token(j, "identificador", i))
                elif j:
                    invalid_char(j)

        for i in tokens:
            print('[', i, ']')

        Z(tokens)

        if(tokens):
            print("Era esperado o final da cadeia mas foi lido: ")
            for i in tokens:
                print(i)
        else:
            print('\nCadeia aceita')
