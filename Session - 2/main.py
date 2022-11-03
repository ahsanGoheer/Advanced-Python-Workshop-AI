from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import spacy

app = FastAPI()

model = spacy.load('en_core_web_sm')

class Article(BaseModel):
    content: str
    comments: List[str] = []
    
@app.get('/')
def get_something():
    return {"message": "Hello World !"}

@app.post("/input/")
def analyze_input(articles: List[Article]):
    
    
    """
    Comments can be **Shown** and *Styled*
    
    * This will show in docs as well
    * with bullet points
    """

    ents = []
    comments = []
    for article in articles:

        for comment in article.comments:
            comments.append(comment.upper())

        doc = model(article.content)
        for ent in doc.ents:
            ents.append({"text":ent.text, "label":ent.label_})
    return {
        "entities":ents,
        "comments":comments
    } 
                            
## Run using:
### uvicorn main:app 