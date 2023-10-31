texto = input("Entre com o texto: ")

newText = ''

for c in texto:
    if c.isupper():
       newText = newText + c.lower()
    else:
        newText = newText + c.upper()

print(newText)