string = input("Entre com uma string: ")

qtdUpperChar = 0

for c in string:
    if c.isupper():
        qtdUpperChar += 1

print(f'Numero de caracteres alfabéticos maiúsculos: {qtdUpperChar}')
