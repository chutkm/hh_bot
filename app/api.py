from fastapi import FastAPI
from .models import Resume, SkillsResponse
import spacy
from spacy.matcher import PhraseMatcher
from app.skills_keywords import SKILLS_KEYWORDS
nlp = spacy.load("ru_core_news_sm")

app = FastAPI()

# Инициализация matcher один раз
matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
patterns = [nlp.make_doc(skill) for skill in SKILLS_KEYWORDS]
matcher.add("SKILLS", patterns)

def extract_skills(text: str) -> list:
    """
    Извлекает навыки из текста на основе списка SKILLS_KEYWORDS.
    Возвращает уникальные навыки в нижнем регистре.
    """
    doc = nlp(text)
    matches = matcher(doc)
    skills_found = {doc[start:end].text.lower() for _, start, end in matches}
    return list(skills_found)

# def extract_skills(text: str):
#     skills = []
#     keywords = ["Python", "SQL", "Machine Learning", "Data Analysis", "Java", "C++"]
#     for kw in keywords:
#         if kw.lower() in text.lower():
#             skills.append(kw)
#     return skills

@app.post("/extract_skills/", response_model=SkillsResponse)
async def get_skills(resume: Resume):
    skills = extract_skills(resume.text)
    return {"skills": skills}
