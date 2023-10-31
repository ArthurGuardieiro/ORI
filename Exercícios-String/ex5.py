message = input("Entre com a mensagem: ")

encodedMessage = ''

for c in message:
    #print(chr( ord(c) + 1))
    if c.isalpha():
        if c == 'Z':
            encodedMessage = encodedMessage + 'A'
        else:
            encodedMessage = encodedMessage + chr( ord(c) + 1 )
    else:
        encodedMessage = encodedMessage + c

print(encodedMessage)
