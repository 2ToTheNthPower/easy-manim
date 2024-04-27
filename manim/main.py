from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
import uvicorn
import re
import os

app = FastAPI()

class Text(BaseModel):
    text: str
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

    def get_response(messages: list):
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )

        print(completion.choices[0].message)

        code_block = re.search(r'```python\n(.*?)```', completion.choices[0].message.content, re.DOTALL)
        code = code_block.group(1)

        print(code)

        # Get scene name based on class name in code
        SceneName = re.search(r'class (.*?)[(:]', code).group(1)

        with open(f"/videos/{SceneName}.py", "w") as f:
            f.write(code)

        try:
            if text.high_quality:
                os.system(f"manim -pqh /videos/{SceneName}.py {SceneName}")
                os.system(f"cp /app/media/videos/{SceneName}/1080p60/{SceneName}.mp4 /videos/1080p60/")
                return {"video_path": f"/videos/1080p60/{SceneName}.mp4"}
            else:
                os.system(f"manim -pql /videos/{SceneName}.py {SceneName}")
                os.system(f"cp /app/media/videos/{SceneName}/480p15/{SceneName}.mp4 /videos/480p15/")
                return {"video_path": f"/videos/480p15/{SceneName}.mp4"}
        except Exception as e:
            messages.append({"role": "user", "content": f"{str(e)}"})
            return messages
        
    response = get_response(messages)

    for i in range(5):
        if isinstance(response, list):
            # if this just returns the list of messages, then we need to keep going
            response = get_response(messages)
        else:
            return response

        

