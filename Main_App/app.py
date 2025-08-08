from flask import Flask, render_template, request
from recommender import rank_resumes, summarize_resume_flan
import os
import pdfplumber
from recommender import extract_applicant_name


app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    job_description = ""
    results = []
    message = None

    if request.method == "POST":
        job_description = request.form["job_description"]
        uploaded_files = request.files.getlist("resumes")

        
        for file in uploaded_files:
            if file and (file.filename.endswith(".txt") or file.filename.endswith(".pdf")):
                filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
                file.save(filepath)

        
        resume_texts = []
        for filename in os.listdir(app.config["UPLOAD_FOLDER"]):
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            if filename.endswith(".txt"):
                with open(filepath, "r", encoding="utf-8") as f:
                    text = f.read()
            elif filename.endswith(".pdf"):
                
                with pdfplumber.open(filepath) as pdf:
                    pages = [page.extract_text() for page in pdf.pages]
                    text = "\n".join(pages)
            else:
                continue  

            resume_texts.append((filename, text))

       
        results = rank_resumes(job_description, resume_texts)
        if not results:
            message = "No resumes found in uploads folder. Please upload some."
        else:
            
            for candidate in results:
                candidate["summary"] = summarize_resume_flan(candidate["text"], job_description)


    return render_template("index.html", results=results, job_description=job_description, message=message)

if __name__ == "__main__":
    app.run(debug=True)
