import streamlit as st
import google.generativeai as genai
import tempfile
import os

st.set_page_config(page_title="Repurpose.ai Pro", page_icon="⚡")

st.title("⚡ Repurpose.ai (Pro)")
st.subheader("Turn Video, Audio, or Text into Strategy.")

# Load the key from the cloud secrets
api_key = st.secrets["GOOGLE_API_KEY"]

genai.configure(api_key=api_key)

# --- CONFIGURATION ---
generation_config = {
  "temperature": 0.7,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
}

system_instruction = """
**Role:** You are an elite Content Strategist.
**Goal:** Analyze the input (video, audio, or text) and create 3 assets:
1. LinkedIn Post (Hook, Bullets, Engagement)
2. Twitter Thread (5 tweets)
3. SEO Blog Outline (Title, H1/H2, Intro)
**Format:** Use Markdown. Separate assets with horizontal rules.
"""

# Connect to the Multimodal Brain
try:
    model = genai.GenerativeModel(
      model_name="gemini-2.5-flash", 
      generation_config=generation_config,
      system_instruction=system_instruction,
    )
except Exception as e:
    st.error(f"Error connecting: {e}")

st.markdown("---")

# --- THE INTERFACE ---
# Create tabs for different input types
tab1, tab2 = st.tabs(["📝 Text Input", "YZ File Upload (Video/PDF/Audio)"])

# TAB 1: TEXT
with tab1:
    user_text = st.text_area("Paste your raw text or idea:", height=200)
    if st.button("Generate from Text 🚀"):
        if not user_text:
            st.warning("Please enter some text.")
        else:
            with st.spinner("Analyzing text..."):
                response = model.generate_content(user_text)
                st.success("Done!")
                st.markdown("---")
                st.markdown(response.text)

# TAB 2: FILES
with tab2:
    st.info("Supported: MP4, MP3, WAV, PDF, JPEG, PNG")
    uploaded_file = st.file_uploader("Upload your asset:", type=["mp4", "mp3", "wav", "pdf", "jpg", "png", "txt"])
    
    if uploaded_file is not None:
        if st.button("Generate from File 🚀"):
            with st.spinner("Uploading to Brain & Analyzing (this may take a moment)..."):
                try:
                    # 1. Save uploaded file to a temporary file on your computer
                    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
                        tmp_file.write(uploaded_file.getvalue())
                        tmp_path = tmp_file.name

                    # 2. Upload that file to Google Gemini
                    remote_file = genai.upload_file(tmp_path)
                    
                    # 3. Ask the AI to analyze it
                    response = model.generate_content([remote_file, "Analyze this file and generate the content pack."])
                    
                    # 4. Cleanup (delete the temp file)
                    os.remove(tmp_path)
                    
                    # 5. Show results
                    st.success("Analysis Complete!")
                    st.markdown("---")
                    st.markdown(response.text)
                    
                except Exception as e:
                    st.error(f"An error occurred: {e}")

st.markdown("---")
st.caption("Powered by Gemini 2.5 Multimodal")