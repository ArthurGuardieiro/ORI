gabarito = input("Entre com o gabarito: ")
respostasAluno = input("Entre com as respostas do aluno: ")

gabarito = gabarito.upper()
respostasAluno = respostasAluno.upper()

pontuacao=0

for i in range(0, len(gabarito)):
    if gabarito[i] == '!':
        pontuacao += 10
    elif gabarito[i] == respostasAluno[i]:
        pontuacao += 10

print(f"Pontuação do aluno: {pontuacao}")