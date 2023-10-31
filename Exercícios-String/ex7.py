qtdTimes = int(input("Entre com o numero de times: "))

maiorPontuacao = 0
campeao = 0

print()

for i in range(0, qtdTimes):
    pontuacao = 0
    resultados = input(f"Entre com a string de resultados do time {i+1}: ")
    for c in resultados:
        if c == "V":
            pontuacao += 3
        elif c == "E":
            pontuacao +=1
    if pontuacao > maiorPontuacao:
        maiorPontuacao = pontuacao
        campeao = i+1

print(f"\nMaior pontuação: {maiorPontuacao}")
print(f"Campeão: time {campeao}")