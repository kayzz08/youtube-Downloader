import streamlit as st
import yt_dlp
import os
import time

# Configure the page
st.set_page_config(
    page_title="YouTube Video Downloader",
    page_icon="📥",
    layout="centered"
)

st.title("📥 YouTube Video Downloader")
st.write("Paste a YouTube URL below to download the video")

# Input for YouTube URL
url = st.text_input("YouTube URL:", placeholder="https://www.youtube.com/watch?v=...")

# Quality selection - using formats that don't require merging
quality = st.selectbox("Select quality:", 
                      ["best[ext=mp4]", "worst[ext=mp4]", "best[height<=720][ext=mp4]", "best[height<=480][ext=mp4]"])

if st.button("Download Video"):
    if url:
        try:
            with st.spinner("Downloading... Please wait"):
                # Use formats that don't require merging (single file mp4)
                ydl_opts = {
                    'format': quality,
                    'outtmpl': '%(title)s.%(ext)s',
                }

                # Download video
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    file_name = ydl.prepare_filename(info)
                    
                    # Read the file for download
                    with open(file_name, 'rb') as file:
                        video_bytes = file.read()
                
                # Create download button
                st.success("Download complete!")
                st.download_button(
                    label="Download MP4 File",
                    data=video_bytes,
                    file_name=file_name,
                    mime="video/mp4"
                )
                
                # Clean up
                os.remove(file_name)
                
        except Exception as e:
            st.error(f"Error: {str(e)}")
    else:
        st.warning("Please enter a YouTube URL")