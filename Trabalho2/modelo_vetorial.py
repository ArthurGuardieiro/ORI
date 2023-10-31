import math

import nltk
import sys

extrator = nltk.stem.RSLPStemmer()
stopwords = nltk.corpus.stopwords.words('portuguese')
# stopwords.append("pra")
caracteresEspecias = [" ", ".", "...", ",", "!", "?", "\n", "\x97"]
caracteresEspeciasForaDoModeloVetorial = [" ", ".", "...", ",", "?", "|", "!", "\n", "\x97"]
operadoresDeSeparacao = ["&"]

base = sys.argv[1]
arquivoConsulta = sys.argv[2]

qtdDeDocsQueOTermoAparece = {}
pesos = {}
pesosConsulta = []
caminhos = []


def calculo_idf(termo, total_docs):
    return math.log10(total_docs / qtdDeDocsQueOTermoAparece[termo])


def calculo_tf(frequencia_termo):
    if frequencia_termo == 0:
        return 0
    return 1 + math.log10(frequencia_termo)


with open(f'{base}', 'r') as arq:
    linhas = arq.readlines()
    for linha in linhas:
        caminho = linha
        caminho = caminho.replace("\n", "")
        caminhos.append(caminho)

quantidadeDocumentos = len(caminhos)

with open(f'{arquivoConsulta}', 'r') as arqConsulta:
    busca = arqConsulta.read()
    busca = busca.lower()
    buscaTokens = busca.split(" ")
    buscaTokens = [p for p in buscaTokens if
                   p.lower() not in stopwords and p not in caracteresEspeciasForaDoModeloVetorial]

palavrasASeremBuscadas = [extrator.stem(p) for p in buscaTokens if p not in operadoresDeSeparacao]

for i in range(len(palavrasASeremBuscadas)):
    print(palavrasASeremBuscadas[i])
    print(pesosConsulta)
    if palavrasASeremBuscadas[i] not in pesosConsulta:
        pesosConsulta.append([palavrasASeremBuscadas[i], palavrasASeremBuscadas.count(palavrasASeremBuscadas[i])])

print('asdada',pesosConsulta)


palavrasASeremBuscadas = list(set(palavrasASeremBuscadas))
print(palavrasASeremBuscadas)

for cam in caminhos:
    with open(cam) as arquivo:
        text = arquivo.read()
        text = text.lower()
        tokens = nltk.wordpunct_tokenize(text)
        tokens = [extrator.stem(p) for p in tokens if p.lower() not in stopwords and p not in caracteresEspecias]
        for i in range(len(palavrasASeremBuscadas)):
            if palavrasASeremBuscadas[i] in tokens:
                if palavrasASeremBuscadas[i] not in qtdDeDocsQueOTermoAparece:
                    qtdDeDocsQueOTermoAparece[f'{palavrasASeremBuscadas[i]}'] = 1
                else:
                    qtdDeDocsQueOTermoAparece[f'{palavrasASeremBuscadas[i]}'] += 1

for cam in caminhos:
    with (open(cam) as arquivo):
        text = arquivo.read()
        text = text.lower()
        tokens = nltk.wordpunct_tokenize(text)
        tokens = [extrator.stem(p) for p in tokens if p.lower() not in stopwords and p not in caracteresEspecias]
        for i in range(len(palavrasASeremBuscadas)):
            calculo_tf_idf = calculo_tf(tokens.count(palavrasASeremBuscadas[i])) * calculo_idf(
                palavrasASeremBuscadas[i], quantidadeDocumentos)
            if calculo_tf_idf != 0:
                if cam not in pesos:
                    pesos[f'{cam}'] = []
                    pesos[f'{cam}'].append([f'{palavrasASeremBuscadas[i]}, {calculo_tf_idf}'])
                else:
                    pesos[f'{cam}'].append([f'{palavrasASeremBuscadas[i]}, {calculo_tf_idf}'])

print(pesos)

with open('pesos.txt', 'w') as arqPesos:
    for arquivo in pesos:
        arqPesos.write(f'{arquivo}: ')
        for peso in pesos[arquivo]:
            arqPesos.write(f'{peso[0]}  ')
        arqPesos.write(f'\n')
