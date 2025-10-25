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

# Quality selection
quality = st.selectbox("Select quality:", ["best", "720p", "480p", "360p"])

if st.button("Download Video"):
    if url:
        try:
            with st.spinner("Downloading... Please wait"):
                # Set up download options
                if quality == "720p":
                    format_selection = 'bestvideo[height<=720]+bestaudio/best[height<=720]'
                elif quality == "480p":
                    format_selection = 'bestvideo[height<=480]+bestaudio/best[height<=480]'
                elif quality == "360p":
                    format_selection = 'bestvideo[height<=360]+bestaudio/best[height<=360]'
                else:
                    format_selection = 'bestvideo+bestaudio/best'
                
                ydl_opts = {
                    'format': format_selection,
                    'merge_output_format': 'mp4',
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