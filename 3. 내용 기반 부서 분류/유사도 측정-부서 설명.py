from sentence_transformers import SentenceTransformer
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from collections import defaultdict
import pandas as pd

matplotlib.rcParams['font.family'] = 'Malgun Gothic'
matplotlib.rcParams['axes.unicode_minus'] = False

model = SentenceTransformer('snunlp/KR-SBERT-V40K-klueNLI-augSTS')

df = pd.read_csv("영천시_부서_담당_업무.csv")

trend_keywords = defaultdict(list)

for _, row in df.iterrows():
    dept = row["부서"]
    role = row["담당"]
    task = row["업무"]

    key = f"{dept}_{role}"
    formatted_task = f"[{role}] {task}"

    trend_keywords[key].append(formatted_task)


input_sentences = [
    "횡단보도 신호 간격이 너무 좁습니다."
]


all_embeddings = []
colors = []
labels = []
topic_names = []
topic_embeddings = []

for sentence in input_sentences:
    emb = model.encode(sentence)
    all_embeddings.append(emb)
    labels.append(sentence)
    colors.append('blue')

for trend_name, keywords in trend_keywords.items():
    keyword_embs = model.encode(keywords)
    centroid = np.mean(keyword_embs, axis=0)
    all_embeddings.append(centroid)
    labels.append(f"{trend_name}")
    colors.append('red')
    topic_names.append(trend_name)
    topic_embeddings.append(centroid)

for sentence in input_sentences:
    emb = model.encode(sentence).reshape(1, -1)
    sims = cosine_similarity(emb, np.array(topic_embeddings)).flatten()
    top3_idx = sims.argsort()[::-1][:3]
    print(f"\n입력 문장: \"{sentence}\"")
    print("가장 유사한 토픽 Top 3:")
    for i in top3_idx:
        print(f"{i+1}. {topic_names[i]} (유사도: {sims[i]:.4f})")

tsne = TSNE(n_components=3, perplexity=5, random_state=42)
reduced = tsne.fit_transform(np.array(all_embeddings))

fig = plt.figure(figsize=(12, 10))
ax = fig.add_subplot(111, projection='3d')

for i, label in enumerate(labels):
    x, y, z = reduced[i]
    ax.scatter(x, y, z, c=colors[i], s=100 if colors[i] == 'blue' else 150, marker='o' if colors[i] == 'blue' else 'X')
    ax.text(x + 1, y + 1, z + 1, label, fontsize=9)

ax.set_title("입력 문장 vs 토픽 트렌드 중심점")
plt.tight_layout()
plt.show()