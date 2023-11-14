import sys

reference = sys.argv[1]
relevant_documents = {}
returned_documents = {}
revocation_precision = {}

def transformar_em_multiplos_de_10(valor):
    if 0 <= valor <= 100:
        return int((valor // 10) * 10)
    else:
        return valor

with open(reference, 'r') as arq:
    lines = arq.readlines()

qtt_queries = lines[0].replace('\n', '')
qtt_queries = int(qtt_queries)

for i in range(1, qtt_queries * 2 + 1):
    if i <= qtt_queries:
        line = lines[i].replace('\n', '')
        relevant_documents[i] = [int(value) for value in line.split()]
    else:
        line = lines[i].replace('\n', '')
        returned_documents[i-qtt_queries] = [int(value) for value in line.split()]

for documents in returned_documents:
    qtt_relevant_documents = 0
    qtt_documents = 0
    revocation_precision[documents] = []
    for document in returned_documents[documents]:
        qtt_documents += 1
        if document in relevant_documents[documents]:
            qtt_relevant_documents += 1
            revocation = qtt_relevant_documents / len(relevant_documents[documents]) * 100
            revocation = transformar_em_multiplos_de_10(revocation)
            precision = qtt_relevant_documents / qtt_documents * 100
            revocation_precision[documents].append([revocation, precision])

print(revocation_precision)