str1 = input("Entre com a primeira string: ")
str2 = input("Entre com a segunda string: ")

allCaracteresAre = True

for c in str1:
    if c not in str2:
        allCaracteresAre = False

if allCaracteresAre:
    print("Todos os caracteres da primeira string aparecem na segunda")
else:
    print("Nem todos os caracteres da primeira string aparecem na segunda")