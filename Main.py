import requests
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from transformers import pipeline

file_urls = [
   "https://raw.githubusercontent.com/acmjec/CompetitiveCoding_Hacktoberfest2024/main/JP%20Morgan/problem11.md",
    "https://raw.githubusercontent.com/acmjec/CompetitiveCoding_Hacktoberfest2024/main/JP%20Morgan/problem9.md",
    "https://raw.githubusercontent.com/acmjec/CompetitiveCoding_Hacktoberfest2024/main/JP%20Morgan/problem8.md",
    "https://raw.githubusercontent.com/acmjec/CompetitiveCoding_Hacktoberfest2024/main/JP%20Morgan/problem7.md",
    "https://raw.githubusercontent.com/acmjec/CompetitiveCoding_Hacktoberfest2024/main/JP%20Morgan/problem10.md"
]

problems = []
for url in file_urls:
    response = requests.get(url)
    if response.status_code == 200:
        problems.append(response.text.strip())
    else:
        problems.append("Error loading problem.")

# text embeddings
model = SentenceTransformer("all-MiniLM-L6-v2")  
problem_embeddings = model.encode(problems)

# faiss index
embedding_dimension = problem_embeddings.shape[1]
index = faiss.IndexFlatL2(embedding_dimension)
index.add(np.array(problem_embeddings))

# hugging fce interface
print("Loading generation model (google/flan-t5-base)...")
generator = pipeline("text2text-generation", model="google/flan-t5-base")


# Command Line
print("Welcome to CodeSage CLI.\n(Type 'quit' to quit.)")

MAX_CHARS = 1500

while True:
    user_query = input("\n Ask your coding question:")

    if user_query.lower() == "quit":
        print("Thanks for using CodeSage.")
        break

    # embedding user query
    query_embedding = model.encode([user_query])

    # searching
    distances, indices = index.search(np.array(query_embedding), k=1)
    match_index = indices[0][0]

    # returning
    print("\n The Problem is: ")
    matched_problem = problems[match_index]

    # truncate the query
    trimmed_problem = matched_problem[:MAX_CHARS]

    # generate answer: hugging face
    prompt = f"Based on the following coding problem, answer the question.\n\nProblem:\n{trimmed_problem}\n\nQuestion:\n{user_query}"
    output = generator(prompt, max_new_tokens=150)

    # printing answer
    print("\n💡 Most Relevant Problem:")
    print(trimmed_problem[:300] + "...")  # Show first 300 chars for context

    print("\n🤖 Answer:")
    print(output[0]['generated_text'].strip())