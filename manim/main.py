from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
import uvicorn
import re
import os
import subprocess

app = FastAPI()

class Text(BaseModel):
    text: str
    model_name: str
    high_quality: bool


client = OpenAI()

@app.post("/generate_video/")
async def generate_video(text: Text):
    messages = [
            {"role": "system", "content": """You are a programming assistant.  
             You create working animations as described in the user message using manim and python.  
             You only speak using code and comments in code.
             If given an error message, you rewrite the entire code block to fix the message."""},
        ]
    
    messages.append({"role": "user", "content": text.text})

    def get_response(messages: list, model_name: str = text.model_name):
        completion = client.chat.completions.create(
            model=model_name,
            messages=messages
        )

        code_block = re.search(r'```python\n(.*?)```', completion.choices[0].message.content, re.DOTALL)
        code = code_block.group(1)

        # Get scene name based on class name in code
        SceneName = re.search(r'class (.*?)[(:]', code).group(1)

        with open(f"/videos/{SceneName}.py", "w") as f:
            f.write(code)

        try:
            if text.high_quality:
                subprocess.run(["manim", "-pqh", f"/videos/{SceneName}.py", SceneName], check=True)
                subprocess.run(["cp", f"/app/media/videos/{SceneName}/1080p60/{SceneName}.mp4", "/videos/1080p60/"], check=True)
                return {"video_path": f"/videos/1080p60/{SceneName}.mp4"}
            else:
                subprocess.run(["manim", "-pql", f"/videos/{SceneName}.py", SceneName], check=True)
                subprocess.run(["cp", f"/app/media/videos/{SceneName}/480p15/{SceneName}.mp4", "/videos/480p15/"], check=True)
                return {"video_path": f"/videos/480p15/{SceneName}.mp4"}
        except subprocess.CalledProcessError as e:
            messages.append({"role": "user", "content": f"{str(e)}"})
            return messages
        
    messages = get_response(messages)

    for i in range(5):
        if isinstance(messages, list):
            # if this just returns the list of messages, then we need to keep going
            messages = get_response(messages)
        else:
            return messages

        

