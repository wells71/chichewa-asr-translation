import streamlit as st
import requests
from io import BytesIO
import time

# API Configuration
ASR_API_URL = "https://zerolat3ncy-chichewa-asr-translation.hf.space"
EN_NYA_API_URL = "https://zerolat3ncy-en-chichewa-translation.hf.space"

st.set_page_config(
    page_title="Chichewa ASR & Translation",
    page_icon="🔊",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 600;
        color: #ffffff;
        margin-bottom: 1.5rem;
    }
    .result-box {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 4px solid #0066cc;
        margin: 1rem 0;
        font-size: 1rem;
        line-height: 1.6;
        color: #1f1f1f;
    }
    .info-text {
        color: #666;
        font-size: 0.95rem;
        margin-bottom: 1.5rem;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">Chichewa Speech Recognition & Translation System</div>', unsafe_allow_html=True)

st.markdown("""
<div class="info-text">
This system provides automated speech recognition and bidirectional translation services for Chichewa (Nyanja) and English.
Select a service below to begin.
</div>
""", unsafe_allow_html=True)

# Navigation tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "Audio to English Pipeline", 
    "Audio Transcription", 
    "Chichewa to English", 
    "English to Chichewa"
])

# Tab 1: Complete Pipeline
with tab1:
    st.subheader("Audio to English Translation Pipeline")
    st.markdown("Upload a Chichewa audio file for automatic transcription and translation to English.")
    
    audio_file_full = st.file_uploader(
        "Select audio file",
        type=['wav', 'mp3', 'm4a', 'flac', 'ogg'],
        key="full_pipeline",
        help="Supported formats: WAV, MP3, M4A, FLAC, OGG"
    )
    
    if audio_file_full:
        st.audio(audio_file_full)
        
        if st.button("Process Audio", key="btn_full", type="primary"):
            with st.spinner("Processing..."):
                try:
                    files = {"file": (audio_file_full.name, audio_file_full, audio_file_full.type)}
                    response = requests.post(
                        f"{ASR_API_URL}/audio-to-english",
                        files=files,
                        timeout=120
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.markdown("**Chichewa Transcription**")
                            st.markdown(f'<div class="result-box">{result["chichewa"]}</div>', unsafe_allow_html=True)
                        
                        with col2:
                            st.markdown("**English Translation**")
                            st.markdown(f'<div class="result-box">{result["english"]}</div>', unsafe_allow_html=True)
                        
                        st.success("Processing completed successfully.")
                    else:
                        st.error(f"Error {response.status_code}: {response.text}")
                
                except requests.exceptions.Timeout:
                    st.error("Request timed out. Please try with a shorter audio file or try again later.")
                except requests.exceptions.ConnectionError:
                    st.error("Unable to connect to the API. Please check your internet connection.")
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")

# Tab 2: Transcription Only
with tab2:
    st.subheader("Audio Transcription Service")
    st.markdown("Upload a Chichewa audio file to receive a text transcription.")
    
    audio_file_transcribe = st.file_uploader(
        "Select audio file",
        type=['wav', 'mp3', 'm4a', 'flac', 'ogg'],
        key="transcribe_only",
        help="Supported formats: WAV, MP3, M4A, FLAC, OGG"
    )
    
    if audio_file_transcribe:
        st.audio(audio_file_transcribe)
        
        if st.button("Transcribe Audio", key="btn_transcribe", type="primary"):
            with st.spinner("Transcribing..."):
                try:
                    files = {"file": (audio_file_transcribe.name, audio_file_transcribe, audio_file_transcribe.type)}
                    response = requests.post(
                        f"{ASR_API_URL}/transcribe",
                        files=files,
                        timeout=120
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        st.markdown("**Transcription Result**")
                        st.markdown(f'<div class="result-box">{result["transcription"]}</div>', unsafe_allow_html=True)
                        st.success("Transcription completed successfully.")
                    else:
                        st.error(f"Error {response.status_code}: {response.text}")
                
                except requests.exceptions.Timeout:
                    st.error("Request timed out. Please try with a shorter audio file or try again later.")
                except requests.exceptions.ConnectionError:
                    st.error("Unable to connect to the API. Please check your internet connection.")
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")

# Tab 3: Chichewa to English
with tab3:
    st.subheader("Chichewa to English Translation")
    st.markdown("Enter Chichewa text to translate to English.")
    
    chichewa_text = st.text_area(
        "Chichewa Text",
        height=150,
        placeholder="Enter Chichewa text here...",
        key="nya_to_en_input"
    )
    
    if st.button("Translate", key="btn_nya_to_en", type="primary"):
        if chichewa_text.strip():
            with st.spinner("Translating..."):
                try:
                    response = requests.post(
                        f"{ASR_API_URL}/translate",
                        json={"text": chichewa_text},
                        timeout=60
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.markdown("**Source (Chichewa)**")
                            st.markdown(f'<div class="result-box">{result["chichewa"]}</div>', unsafe_allow_html=True)
                        
                        with col2:
                            st.markdown("**Translation (English)**")
                            st.markdown(f'<div class="result-box">{result["english"]}</div>', unsafe_allow_html=True)
                        
                        st.success("Translation completed successfully.")
                    else:
                        st.error(f"Error {response.status_code}: {response.text}")
                
                except requests.exceptions.Timeout:
                    st.error("Request timed out. Please try again.")
                except requests.exceptions.ConnectionError:
                    st.error("Unable to connect to the API. Please check your internet connection.")
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
        else:
            st.warning("Please enter text to translate.")

# Tab 4: English to Chichewa
with tab4:
    st.subheader("English to Chichewa Translation")
    st.markdown("Enter English text to translate to Chichewa.")
    
    english_text = st.text_area(
        "English Text",
        height=150,
        placeholder="Enter English text here...",
        key="en_to_nya_input"
    )
    
    if st.button("Translate", key="btn_en_to_nya", type="primary"):
        if english_text.strip():
            with st.spinner("Translating..."):
                try:
                    response = requests.post(
                        f"{EN_NYA_API_URL}/translate",
                        json={"text": english_text},
                        timeout=60
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.markdown("**Source (English)**")
                            st.markdown(f'<div class="result-box">{result["english"]}</div>', unsafe_allow_html=True)
                        
                        with col2:
                            st.markdown("**Translation (Chichewa)**")
                            st.markdown(f'<div class="result-box">{result["chichewa"]}</div>', unsafe_allow_html=True)
                        
                        st.success("Translation completed successfully.")
                    else:
                        st.error(f"Error {response.status_code}: {response.text}")
                
                except requests.exceptions.Timeout:
                    st.error("Request timed out. Please try again.")
                except requests.exceptions.ConnectionError:
                    st.error("Unable to connect to the API. Please check your internet connection.")
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
        else:
            st.warning("Please enter text to translate.")

# Footer
st.markdown("---")
st.markdown("""
