from Xclient import MetaLMEmbeddings

xlembed = MetaLMEmbeddings(model="bge-m3-v",base_url="http://10.88.36.58:8200")

text = ['asdasda','asdwrfa']

res= xlembed.embed_query('asdasda')
print(res)
res= xlembed.embed_documents(text)
print(res)

res= xlembed.embed_documents_sparse(text)
print(res)


res= xlembed.embed_query_sparse('asdasda')
print(res)