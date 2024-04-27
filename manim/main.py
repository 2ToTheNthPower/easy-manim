from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
import uvicorn
import re
import os

app = FastAPI()

class Text(BaseModel):
    text: str

@app.post("/generate_video/")
async def generate_video(text: Text):
    client = OpenAI()
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a programming assistant.  You speak only in python code and comments in your code."},
            {"role": "user", "content": text.text}
        ]
    )
    code_block = re.search(r'```(.*?)```', completion.choices[0].message, re.DOTALL)
    code = code_block.group(1)

    # Get scene name based on class name in code
    SceneName = re.search(r'class (.*?)[(:]', code).group(1)

    with open("code.py", "w") as f:
        f.write(code)

    try:
        os.system(f"manim -pql code.py {SceneName}")
        return {"video_path": f"{SceneName}.mp4"}
    except Exception as e:
        return {"error": str(e)}

