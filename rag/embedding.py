import sys

print(sys.path)
from sentence_transformers import SentenceTransformer, util
from database import USTCHBase



# model = SentenceTransformer('Sakil/sentence_similarity_semantic_search')
# sentences = ['A man is eating food. Why bother?',
#           'A man is eating a piece of bread.',
#           'The girl is carrying a baby.',
#           'A man is riding a horse.',
# ]
# embeddings = model.encode(sentences)
# print(embeddings.shape)
# util.cos_sim(embeddings, embeddings[:2])