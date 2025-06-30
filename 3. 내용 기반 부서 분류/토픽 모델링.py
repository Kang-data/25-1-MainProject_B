#import matplotlib.pyplot as plt
#from wordcloud import WordCloud

import pandas as pd
from konlpy.tag import Okt
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import networkx as nx

n="영천시뉴스제목.csv"
print(n)
df = pd.read_csv(n)
df = df.dropna(subset=['URL'])

okt = Okt()
def preprocess(text):
    tokens = okt.nouns(text)
    return " ".join([t for t in tokens if len(t) > 1])

df['cleaned'] = df['URL'].apply(preprocess)

vectorizer = CountVectorizer(max_df=0.9, min_df=5)
X = vectorizer.fit_transform(df['cleaned'])

n_topics = 10
lda_model = LatentDirichletAllocation(n_components=n_topics, random_state=42)
lda_model.fit(X)

topic_vectors = lda_model.components_ / lda_model.components_.sum(axis=1)[:, np.newaxis]
similarity_matrix = cosine_similarity(topic_vectors)

threshold = 0.8
G = nx.Graph()
G.add_nodes_from(range(n_topics))

for i in range(len(similarity_matrix)):
    for j in range(i + 1, len(similarity_matrix)):
        if similarity_matrix[i][j] > threshold:
            G.add_edge(i, j)

topic_groups = list(nx.connected_components(G))

words = vectorizer.get_feature_names_out()

print(f"\n병합된 토픽 그룹 수: {len(topic_groups)}개\n")
for group_id, group in enumerate(topic_groups):
    merged_vector = np.sum([lda_model.components_[i] for i in group], axis=0)
    top_words_idx = merged_vector.argsort()[:-11:-1]
    top_words = [words[i] for i in top_words_idx]
    print(f"병합 Topic {group_id+1} (원래 토픽: {sorted(list(group))})")
    print("주요 단어:", ", ".join(top_words))
    print()

# for i, topic in enumerate(lda_model.components_):
#     plt.figure(figsize=(6, 6))
#     font_path = "C:/Windows/Fonts/malgun.ttf"
#     wordcloud = WordCloud(
#     font_path=font_path,
#     background_color='white',
#     width=800,
#     height=600
# ).generate_from_frequencies({words[j]: topic[j] for j in topic.argsort()[:-30:-1]})
#     plt.imshow(wordcloud, interpolation='bilinear')
#     plt.axis("off")
#     plt.title(f"Topic {i+1}")
#     plt.show()
