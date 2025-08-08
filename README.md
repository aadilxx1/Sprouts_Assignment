# Sprouts_Assignment
Candidate Recommendation Engine powered by LLM
Candidate Recommendation Engine
📌 Overview
This Candidate Recommendation Engine ranks and summarizes resumes against a given job description using Natural Language Processing (NLP) and semantic similarity techniques.
It is designed to assist recruiters and hiring managers in quickly identifying top candidates from a pool of resumes.

The application:

Accepts a job description (text input).

Accepts multiple resumes (PDF, DOCX, or TXT files).

Extracts and cleans resume text.

Generates semantic embeddings using sentence-transformers.

Calculates cosine similarity between each resume and the job description.

Uses a lightweight LLM (MBZUAI/LaMini-Flan-T5-248M) for a short, human-readable explanation of why the candidate is a good fit.

Displays ranked results with:

Candidate Name (from resume or filename)

File Name

Similarity Score

Summary

🛠 Approach
1. Text Extraction
PDF resumes → parsed using PyPDF2

DOCX resumes → parsed using python-docx

TXT resumes → directly read as text

Minimal cleaning (remove extra spaces, special characters where needed)

2. Embedding Generation
Used all-MiniLM-L6-v2 from sentence-transformers for generating 384-dimensional embeddings.

Generated embeddings for:

Job description (once)

Each resume (individually)

3. Similarity Calculation
Computed cosine similarity between the job description embedding and each resume embedding.

Higher score = higher semantic similarity to the job description.

4. Candidate Name Extraction
Tried extracting candidate’s name from the first 3 lines of the resume (common format for names at the top).

If not found, fell back to filename without extension.

5. Summary Generation
Used MBZUAI/LaMini-Flan-T5-248M LLM for generating short summaries:

Prompt: "Why is this candidate a good fit for the given job description?"

This helps recruiters understand the matching context, not just the score.

📋 Assumptions
Resumes are in English.

Resume files are well-formatted (name near top, text extractable).

Similarity score is a proxy for relevance — not a hiring decision.

LLM summarization works best with cleaned, relevant resume sections.

Job descriptions are detailed enough for meaningful comparison.

⚠ Limitations
Cannot perfectly handle image-based (scanned) resumes without OCR.

Candidate name extraction may fail if resumes have unconventional formatting.

LLM summaries depend on model capability — may occasionally be generic.

Cosine similarity does not account for specific skill weights (all terms treated equally).

Large file uploads may impact performance on free hosting tiers.
