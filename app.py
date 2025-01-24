# Import necessary libraries
import re
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import streamlit as st

# Preprocessing function for text
def preprocess_text(text):
    text = re.sub(r'\W', ' ', text)
    text = re.sub(r'\d', '', text)
    text = text.lower()
    return text

# Function to extract name from CV content
def extract_name(cv_text):
    # Extract name from the first few lines (adjust logic as needed)
    lines = cv_text.splitlines()
    for line in lines[:3]:  # Only check the first 3 lines
        if len(line.split()) >= 2:  # Assume names have at least 2 words
            return line.strip()
    return "Unknown Name"

# Function to read the uploaded file
def read_file(file):
    try:
        # Try reading as utf-8
        return file.read().decode('utf-8')
    except UnicodeDecodeError:
        try:
            # If utf-8 fails, try latin-1
            return file.read().decode('latin-1')
        except UnicodeDecodeError:
            # If both fail, try windows-1252
            return file.read().decode('windows-1252')

# Load pre-trained model from sentence-transformers
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

# Function to get embeddings for text
def get_embeddings(text_list):
    return model.encode(text_list)

# Cosine similarity function to rank candidates
def rank_candidates(cv_embeddings, job_embedding):
    similarities = cosine_similarity(cv_embeddings, job_embedding)
    ranked_indices = np.argsort(similarities[:, 0])[::-1]  # Sort in descending order
    return ranked_indices[:10]  # Return top 10 candidates

# Streamlit app function
def main():
    st.title("HR Candidate Ranking App")

    # File uploader for multiple CVs
    uploaded_files = st.file_uploader("Upload CV files", accept_multiple_files=True)

    if uploaded_files:
        # Preprocess and read all uploaded CVs
        cvs = [preprocess_text(read_file(file)) for file in uploaded_files]
        names = [extract_name(read_file(file)) for file in uploaded_files]  # Extract candidate names

        # Text area to input job description
        job_description = st.text_area("Enter Job Description")

        if st.button("Rank Candidates"):
            # Get embeddings for CVs and job description
            cv_embeddings = get_embeddings(cvs)
            job_embedding = get_embeddings([job_description])

            # Rank candidates based on similarity
            ranked_indices = rank_candidates(cv_embeddings, job_embedding)

            # Display ranked candidates
            st.write("Top 10 Candidates:")
            for rank, idx in enumerate(ranked_indices, 1):
                st.write(f"Candidate {rank}: {names[idx]}")  # Correctly map index to name

# Entry point
if __name__ == "__main__":
    main()
