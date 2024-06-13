import numpy as np
from .get_embedding import get_embedding

def cosine_similarity(vec1, vec2):
    """コサイン類似度を計算する関数"""
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

def word_similarity(llm, query1, query2):
    """クエリの類似度を計算する関数"""
    embedding1 = get_embedding(llm, query1)
    embedding2 = get_embedding(llm, query2)
    return cosine_similarity(embedding1, embedding2)