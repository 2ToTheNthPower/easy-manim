import streamlit as st
import requests
from openai import OpenAI

txt = st.text_area(
    label="Describe your math animation!",
    height=200,
)

client = OpenAI()

model_options = [model.id for model in client.models.list()]

with st.sidebar:
    model_name = st.selectbox("Model", options=model_options, index=model_options.index("gpt-4-turbo"))

    high_quality = st.toggle("High Quality", False)


if st.button("Generate Animation"):

    st.write(f"Generating animation for: {txt}")
    # Call the manim API to generate the video
    response = requests.post("http://manim:8000/generate_video/", json={"text": txt, "high_quality": high_quality, "model_name": model_name})
    st.write(response)
    data = response.json()

    if "error" in data.keys():
        st.write(f"Error: {data['error']}")
    else:
        st.write(f"Video generated: {data['video_path']}")
        video_file = open(data['video_path'], 'rb')
        video_bytes = video_file.read()
        st.video(video_bytes)