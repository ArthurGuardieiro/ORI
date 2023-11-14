import sys

reference = sys.argv[1]
relevant_documents = {}
queries = {}

with open(reference, 'r') as arq:
    lines = arq.readlines()

qtt_queries = lines[0].replace('\n', '')
qtt_queries = int(qtt_queries)

for i in range(1, qtt_queries * 2 + 1):
    if i <= qtt_queries:
        relevant_documents[i] = lines[i].replace('\n', '')
    else:
        queries[i-qtt_queries] = lines[i].replace('\n', '')

print(relevant_documents)
print(queries)
