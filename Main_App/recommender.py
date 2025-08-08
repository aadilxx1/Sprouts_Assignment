from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

#Embedding Model
embedder = SentenceTransformer("all-mpnet-base-v2")

#Summarization Model
model_name = "MBZUAI/LaMini-Flan-T5-248M"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)


device = torch.device("cpu")
model.to(device)


def extract_key_sections(resume_text):
    sections = {"education": [], "experience": [], "skills": [], "projects": []}
    lines = resume_text.splitlines()
    current = None

    for line in lines:
        line = line.strip()
        if not line:
            continue

        l = line.lower()
        if "education" in l:
            current = "education"
        elif "experience" in l or "work history" in l:
            current = "experience"
        elif "skills" in l:
            current = "skills"
        elif "projects" in l or "certifications" in l:
            current = "projects"
        elif current:
            sections[current].append(line)

    return sections

def extract_applicant_name(resume_text, filename):
    
    # first 3 lines
    lines = resume_text.strip().split("\n")[:3]
    possible_name = None

    for line in lines:
        clean_line = line.strip()
        if clean_line and 2 <= len(clean_line.split()) <= 4:
            
            possible_name = clean_line
            break

    if possible_name:
        return possible_name
    return filename.rsplit(".", 1)[0]  #fallback to filename if name not found.


def rank_resumes(job_description, resume_texts):
    if not resume_texts:
        return []

    texts = [job_description] + [text for _, text in resume_texts]
    embeddings = embedder.encode(texts)
    job_embedding = embeddings[0].reshape(1, -1)
    resume_embeddings = embeddings[1:]

    similarities = cosine_similarity(job_embedding, resume_embeddings)[0]

    results = []
    for (filename, resume_text), sim in zip(resume_texts, similarities):
        applicant_name = extract_applicant_name(resume_text, filename)
        results.append({
            "filename": filename,                       
            "applicant_name": applicant_name,            
            "text": resume_text,
            "score": round(float(sim), 4)
        })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:4]


# ===== Summarization =====
def summarize_resume_flan(resume_text, job_description):
    prompt = f"""
    Summarize this resume in 3 bullet points, focusing on skills and experience relevant to the job description.

    Job Description:
    {job_description}

    Resume:
    {resume_text}
    """

    inputs = tokenizer(
        prompt, 
        return_tensors="pt", 
        truncation=True, 
        max_length=512
    ).to(device)

    outputs = model.generate(
        **inputs, 
        max_length=200, 
        num_beams=4, 
        early_stopping=True
    )

    return tokenizer.decode(outputs[0], skip_special_tokens=True)
