from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader('a.pdf')

docs = loader.load()

print(len(docs))

print(docs[23].page_content)
print(docs[23].metadata)

