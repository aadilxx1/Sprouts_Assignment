
# Candidate Recommendation Engine powered by LLM

## 📌 Overview

This Candidate Recommendation Engine ranks and summarizes resumes against a given job description using Natural Language Processing (NLP) and semantic similarity techniques. It is designed to assist recruiters and hiring managers in quickly identifying top candidates from a pool of resumes.

The application:

- Accepts a **job description** (text input).
- Accepts **multiple resumes** (PDF or TXT files).
- Extracts and cleans resume text.
- Generates semantic embeddings using **sentence-transformers**.
- Calculates **cosine similarity** between each resume and the job description.
- Uses a lightweight LLM (**MBZUAI/LaMini-Flan-T5-248M**) for a short, human-readable explanation of why the candidate is a good fit.
- Displays ranked results with:
  - **Candidate Name** (from resume or filename)
  - **File Name**
  - **Similarity Score**
  - **Summary**

---

## 🛠 Approach

##  AI Summarization

I chose **not to use GPT API or Gemini API** for the AI-powered candidate summary because 
I wanted to explore alternative options and deepen my understanding of
open-source large language models (LLMs).

After experimenting with several LLM models, I finalized on using the **MBZUAI/LaMini-Flan-T5-248M** 
model for generating candidate summaries. This model provides a good balance of performance 
and efficiency for summarization tasks, and working with it has helped me learn more about 
LLMs outside of the popular API-based services.

##  Embeddings
- For generating semantic embeddings to measure resume-job description similarity, 
I used **all-mpnet-base-v2** from the sentence-transformers library. This model 
provided better cosine similarity results compared to other embedding models I tested,
making the ranking of candidates more accurate and relevant.


- **Text Extraction**  
  - PDF resumes → parsed using PyPDF2  
  - DOCX resumes → parsed using python-docx  
  - TXT resumes → directly read as text  
  - Minimal cleaning (remove extra spaces, special characters where needed)

- **Embedding Generation**    
  - Generated embeddings for:  
    - Job description (once)  
    - Each resume (individually)

- **Similarity Calculation**  
  - Computed cosine similarity between the job description embedding and each resume embedding.  
  - Higher score = higher semantic similarity to the job description.

- **Candidate Name Extraction**  
  - Tried extracting candidate’s name from the first 3 lines of the resume (common format for names at the top).  
  - If not found, fell back to filename without extension.

- **Summary Generation**  
  - Used **MBZUAI/LaMini-Flan-T5-248M** LLM for generating short summaries.  
  - Prompt: *"Why is this candidate a good fit for the given job description?"*  
  - Helps recruiters understand the matching context, not just the score.

---

## 📋 Assumptions

- Resumes are in English.  
- Resume files are well-formatted (name near top, text extractable).  
- Similarity score is a proxy for relevance — not a hiring decision.  
- LLM summarization works best with cleaned, relevant resume sections.  
- Job descriptions are detailed enough for meaningful comparison.

---

## ⚠ Limitations
  
- Candidate name extraction may fail if resumes have unconventional formatting.  
- LLM summaries depend on model capability — may occasionally be generic.  
- Cosine similarity does not account for specific skill weights (all terms treated equally).  
- Large file uploads may impact performance on free hosting tiers.

## Potential Improvements

Here are some ideas to enhance the engine’s functionality and performance - 

### 1. Model and Embeddings
- Experiment with larger or more recent language models for improved summarization quality.  
- Fine-tune embedding models on domain-specific data for better candidate-job matching.  
- Cache embeddings to speed up repeated queries.

### 2. Ranking & Recommendation
- Incorporate additional ranking criteria like experience level, skills match weighting, or recency of resume updates.  
- Use a hybrid approach combining semantic similarity with keyword matching for more accurate recommendations.

### 3. Scalability and Deployment
- Containerize the app using Docker for easier deployment and scalability.  
- Integrate with cloud storage (e.g., AWS S3) for resume and job description management.  
- Use asynchronous processing or batch jobs to handle large volumes of resumes efficiently.


## Install dependencies:
pip install -r requirements.txt

## Running the Engine
python app.py

This will launch the engine locally, typically at http://127.0.0.1:5000/
---
