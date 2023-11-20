import sys
import matplotlib.pyplot as plt

reference = sys.argv[1]
relevant_documents = {}
returned_documents = {}
revocation_precision = {}
average_revocation_precision = {}


def transform_into_multiples_of_10(valor):
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
    revocation_precision[documents] = {}
    for i in range(0, 101, 10):
        revocation_precision[documents][i] = 0
    for document in returned_documents[documents]:
        qtt_documents += 1
        if document in relevant_documents[documents]:
            qtt_relevant_documents += 1
            revocation = qtt_relevant_documents / len(relevant_documents[documents]) * 100
            revocation = transform_into_multiples_of_10(revocation)
            precision = qtt_relevant_documents / qtt_documents * 100
            revocation_precision[documents][revocation] = precision


# VARREDURA DE TRÁS PARA FRENTE
for value in revocation_precision:
    for i in range(100, -1, -10):
        if i != 0:
            actual_precision = revocation_precision[value][i]
            next_precision = revocation_precision[value][i-10]
            if actual_precision > next_precision:
                revocation_precision[value][i-10] = actual_precision

for i in range(0, 101, 10):
    average_revocation_precision[i] = 0

for dct in revocation_precision:
    for key in revocation_precision[dct]:
        average_revocation_precision[key] += revocation_precision[dct][key]

for key in average_revocation_precision:
    average_revocation_precision[key] /= qtt_queries


with open('media.txt', 'w') as arq:
    for i in average_revocation_precision:
        arq.write(f'{average_revocation_precision[i]/100:.2f} ')

x = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
for value in revocation_precision:
    y = []
    for key in revocation_precision[value]:
        y.append(revocation_precision[value][key])
    plt.plot(x, y)
    plt.title(f'Gráfico consulta {value}')
    plt.show()

y = []
for value in average_revocation_precision:
    y.append(average_revocation_precision[value])
plt.plot(x, y)
plt.title('Gráfico médias')
plt.show()
