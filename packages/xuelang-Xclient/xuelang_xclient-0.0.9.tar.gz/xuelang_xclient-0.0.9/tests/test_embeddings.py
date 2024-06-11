from Xclient import MetaLMEmbeddings

xlembed = MetaLMEmbeddings(model="bge-m3-v",base_url="http://10.88.36.58:8200")

text = ['asdasda','asdwrfa']

res= xlembed.embed_documents_sparse(text)
print(res[1])


res= xlembed.embed_query_sparse('asdasda')
print(res[1])