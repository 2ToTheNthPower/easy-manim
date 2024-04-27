import streamlit as st
import requests

txt = st.text_area(
    label="Describe your math animation!",
    height=200,
)

if st.toggle("High Quality"):
    high_quality = True
else:
    high_quality = False

if st.button("Generate Animation"):

    st.write(f"Generating animation for: {txt}")
    # Call the manim API to generate the video
    response = requests.post("http://manim:8000/generate_video/", json={"text": txt, "high_quality": high_quality})
    st.write(response)
    data = response.json()

    if "error" in data.keys():
        st.write(f"Error: {data['error']}")
    else:
        st.write(f"Video generated: {data['video_path']}")
        video_file = open(data['video_path'], 'rb')
        video_bytes = video_file.read()
        st.video(video_bytes)