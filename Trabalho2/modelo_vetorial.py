import math

import nltk
import sys

extrator = nltk.stem.RSLPStemmer()
stopwords = nltk.corpus.stopwords.words('portuguese')
# stopwords.append("pra")
caracteres_especiais = [" ", ".", "...", ",", "!", "?", "\n", "\x97"]
caracteres_especiais_fora_do_modelo_vetorial = [" ", ".", "...", ",", "?", "|", "!", "\n", "\x97"]
operadores_de_separacao = ["&"]

base = sys.argv[1]
arquivo_consulta = sys.argv[2]

qtd_de_docs_que_o_termo_aparece = {}
pesos = {}
frequencias_consulta = {}
pesos_consulta = {}
caminhos = []
similaridades = {}


def calculo_idf(termo_calculado, total_docs):
    return math.log10(total_docs / qtd_de_docs_que_o_termo_aparece[termo_calculado])


def calculo_tf(frequencia_termo):
    if frequencia_termo == 0:
        return 0
    return 1 + math.log10(frequencia_termo)


def somatorio_numerador(lista_pesos_splitada, pesos_consulta):
    somatorio = 0
    for lista in lista_pesos_splitada:
        termo_presente = lista[0][0:-1]
        somatorio += float(lista[1]) * pesos_consulta[termo_presente]
    return somatorio


def somatorio_denominador(lista_pesos, lista_pesos_consulta):
    somatorio_documento = 0
    for peso in lista_pesos:
        somatorio_documento += float(peso) * float(peso)
    somatorio_documento = math.sqrt(somatorio_documento)

    somatorio_consulta = 0
    for peso in lista_pesos_consulta:
        somatorio_consulta += float(peso) * float(peso)
    somatorio_consulta = math.sqrt(somatorio_consulta)

    return somatorio_documento * somatorio_consulta


with open(f'{base}', 'r') as arq:
    linhas = arq.readlines()
    for linha in linhas:
        caminho = linha
        caminho = caminho.replace("\n", "")
        caminhos.append(caminho)

quantidade_documentos = len(caminhos)

with open(f'{arquivo_consulta}', 'r') as arqConsulta:
    busca = arqConsulta.read()
    busca = busca.lower()
    buscaTokens = busca.split(" ")
    buscaTokens = [p for p in buscaTokens if
                   p.lower() not in stopwords and p not in caracteres_especiais_fora_do_modelo_vetorial]

palavrasASeremBuscadas = [extrator.stem(p) for p in buscaTokens if p not in operadores_de_separacao]

for i in range(len(palavrasASeremBuscadas)):
    if palavrasASeremBuscadas[i] not in pesos_consulta:
        frequencias_consulta[palavrasASeremBuscadas[i]] = palavrasASeremBuscadas.count(palavrasASeremBuscadas[i])

palavrasASeremBuscadas = list(set(palavrasASeremBuscadas))

for cam in caminhos:
    with open(cam) as arquivo:
        text = arquivo.read()
        text = text.lower()
        tokens = nltk.wordpunct_tokenize(text)
        tokens = [extrator.stem(p) for p in tokens if p.lower() not in stopwords and p not in caracteres_especiais]
        for i in range(len(palavrasASeremBuscadas)):
            if palavrasASeremBuscadas[i] in tokens:
                if palavrasASeremBuscadas[i] not in qtd_de_docs_que_o_termo_aparece:
                    qtd_de_docs_que_o_termo_aparece[f'{palavrasASeremBuscadas[i]}'] = 1
                else:
                    qtd_de_docs_que_o_termo_aparece[f'{palavrasASeremBuscadas[i]}'] += 1

for cam in caminhos:
    with (open(cam) as arquivo):
        text = arquivo.read()
        text = text.lower()
        tokens = nltk.wordpunct_tokenize(text)
        tokens = [extrator.stem(p) for p in tokens if p.lower() not in stopwords and p not in caracteres_especiais]
        for i in range(len(palavrasASeremBuscadas)):
            calculo_tf_idf = calculo_tf(tokens.count(palavrasASeremBuscadas[i])) * calculo_idf(
                palavrasASeremBuscadas[i], quantidade_documentos)
            if calculo_tf_idf != 0:
                if cam not in pesos:
                    pesos[f'{cam}'] = []
                    pesos[f'{cam}'].append([f'{palavrasASeremBuscadas[i]}, {calculo_tf_idf}'])
                else:
                    pesos[f'{cam}'].append([f'{palavrasASeremBuscadas[i]}, {calculo_tf_idf}'])

for termo in frequencias_consulta:
    calculo_tf_idf = calculo_tf(frequencias_consulta[termo]) * calculo_idf(termo, quantidade_documentos)
    pesos_consulta[termo] = calculo_tf_idf

with open('pesos.txt', 'w') as arqPesos:
    for arquivo in pesos:
        arqPesos.write(f'{arquivo}: ')
        for peso in pesos[arquivo]:
            arqPesos.write(f'{peso[0]}  ')
        arqPesos.write(f'\n')

lista_pesos_consulta = []
for peso in pesos_consulta:
    lista_pesos_consulta.append(pesos_consulta[peso])

for doc in pesos:
    #print(pesos[doc], pesos_consulta)
    lista_pesos = []
    lista_splitada_doc = []
    for lista in pesos[doc]:
        lista_splitada = lista[0].split(" ")
        lista_splitada_doc.append(lista_splitada)
        lista_pesos.append(lista_splitada[1])
    numerador = somatorio_numerador(lista_splitada_doc, pesos_consulta)
    denominador = somatorio_denominador(lista_pesos, lista_pesos_consulta)
    similaridade = numerador / denominador
    if similaridade >= 0.001:
        similaridades[doc] = similaridade

with open('resposta.txt', 'w') as arqResposta:
    arqResposta.write(str(len(similaridades)))
    arqResposta.write('\n')
    for arquivo in similaridades:
        #print(arquivo)
        arqResposta.write(f'{arquivo} {similaridades[arquivo]:.4f}')
        arqResposta.write('\n')