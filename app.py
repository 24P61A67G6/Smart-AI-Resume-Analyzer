from flask import Flask, render_template, request
import PyPDF2
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)

    text = ""

    for page in reader.pages:
        text += page.extract_text() or ""

    return text


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():

    resume = request.files["resume"]
    job_description = request.form["job_description"]

    if resume.filename == "":
        return "Please upload a resume"

    resume_text = extract_text_from_pdf(resume)

    skills = [
        "python",
        "java",
        "sql",
        "html",
        "css",
        "javascript",
        "git",
        "github",
        "docker",
        "jenkins",
        "aws",
        "machine learning"
    ]

    resume_lower = resume_text.lower()
    job_lower = job_description.lower()

    matched_skills = []
    missing_skills = []

    for skill in skills:

        if skill in job_lower:

            if skill in resume_lower:
                matched_skills.append(skill)

            else:
                missing_skills.append(skill)

    total_required = len(matched_skills) + len(missing_skills)

    if total_required > 0:
        score = int((len(matched_skills) / total_required) * 100)
    else:
        score = 0

    return render_template(
        "index.html",
        score=score,
        matched_skills=matched_skills,
        missing_skills=missing_skills
    )


if __name__ == "__main__":
    app.run(debug=True)
