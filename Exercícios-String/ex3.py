texto = input("Entre com o texto: ")
texto = texto.replace(" ", "")

palindromo = texto[::-1]


if texto.lower() == palindromo.lower():
    print("Este texto é um palindromo")
else:
    print("Este texto não é um palindromo")


