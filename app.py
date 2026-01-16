import streamlit as st
import requests

# =============================
# API Configuration
# =============================
ASR_API_URL = "https://zerolat3ncy-chichewa-asr-translation.hf.space"
EN_NYA_API_URL = "https://zerolat3ncy-en-chichewa-translation.hf.space"

# =============================
# Page config
# =============================
st.set_page_config(
    page_title="Chichewa ASR & Translation",
    page_icon="🔊",
    layout="wide"
)

# =============================
# Helpers
# =============================
def safe_post(url, **kwargs):
    try:
        r = requests.post(url, **kwargs)
    except requests.exceptions.Timeout:
        st.error("Request timed out. Please try again.")
        st.stop()
    except requests.exceptions.ConnectionError:
        st.error("Unable to connect to the API.")
        st.stop()

    if r.status_code != 200:
        st.error(f"HF error {r.status_code}")
        st.text(r.text[:1000])
        st.stop()

    content_type = r.headers.get("content-type", "")
    if "json" not in content_type:
        st.error("HF returned non-JSON (model loading or crashed)")
        st.text(r.text[:1000])
        st.stop()

    return r.json()


def load_audio_bytes(uploaded_file, max_mb=10):
    audio_bytes = uploaded_file.read()
    size_mb = len(audio_bytes) / (1024 * 1024)

    if size_mb > max_mb:
        st.error(f"Audio too large ({size_mb:.1f}MB). Max allowed is {max_mb}MB.")
        st.stop()

    return audio_bytes


# =============================
# Custom CSS
# =============================
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

# =============================
# Header
# =============================
st.markdown(
    '<div class="main-header">Chichewa Speech Recognition & Translation System</div>',
    unsafe_allow_html=True
)

st.markdown("""
<div class="info-text">
This system provides automated speech recognition and bidirectional translation
services for Chichewa (Nyanja) and English.
</div>
""", unsafe_allow_html=True)

# =============================
# Tabs
# =============================
tab1, tab2, tab3, tab4 = st.tabs([
    "Audio → English Pipeline",
    "Audio Transcription",
    "Chichewa → English",
    "English → Chichewa"
])

# ======================================================
# TAB 1: AUDIO → ENGLISH PIPELINE
# ======================================================
with tab1:
    st.subheader("Audio to English Translation Pipeline")

    audio_file = st.file_uploader(
        "Upload Chichewa audio",
        type=["wav", "mp3", "m4a", "flac", "ogg"]
    )

    if audio_file:
        st.audio(audio_file)

        if st.button("Process Audio", type="primary"):
            with st.spinner("Processing audio..."):
                audio_bytes = load_audio_bytes(audio_file)

                files = {
                    "file": (audio_file.name, audio_bytes, audio_file.type)
                }

                result = safe_post(
                    f"{ASR_API_URL}/audio-to-english",
                    files=files,
                    timeout=120
                )

                col1, col2 = st.columns(2)

                with col1:
                    st.markdown("**Chichewa Transcription**")
                    st.markdown(
                        f'<div class="result-box">{result["chichewa"]}</div>',
                        unsafe_allow_html=True
                    )

                with col2:
                    st.markdown("**English Translation**")
                    st.markdown(
                        f'<div class="result-box">{result["english"]}</div>',
                        unsafe_allow_html=True
                    )

                st.success("Processing completed successfully.")

# ======================================================
# TAB 2: TRANSCRIPTION ONLY
# ======================================================
with tab2:
    st.subheader("Audio Transcription Service")

    audio_file = st.file_uploader(
        "Upload Chichewa audio",
        type=["wav", "mp3", "m4a", "flac", "ogg"],
        key="transcribe"
    )

    if audio_file:
        st.audio(audio_file)

        if st.button("Transcribe Audio", type="primary"):
            with st.spinner("Transcribing..."):
                audio_bytes = load_audio_bytes(audio_file)

                files = {
                    "file": (audio_file.name, audio_bytes, audio_file.type)
                }

                result = safe_post(
                    f"{ASR_API_URL}/transcribe",
                    files=files,
                    timeout=120
                )

                st.markdown("**Transcription Result**")
                st.markdown(
                    f'<div class="result-box">{result["transcription"]}</div>',
                    unsafe_allow_html=True
                )

                st.success("Transcription completed successfully.")

# ======================================================
# TAB 3: CHICHEWA → ENGLISH
# ======================================================
with tab3:
    st.subheader("Chichewa to English Translation")

    chichewa_text = st.text_area(
        "Enter Chichewa text",
        height=150
    )

    if st.button("Translate", type="primary"):
        if not chichewa_text.strip():
            st.warning("Please enter text to translate.")
        else:
            with st.spinner("Translating..."):
                result = safe_post(
                    f"{ASR_API_URL}/translate",
                    json={"text": chichewa_text},
                    timeout=60
                )

                col1, col2 = st.columns(2)

                with col1:
                    st.markdown("**Source (Chichewa)**")
                    st.markdown(
                        f'<div class="result-box">{result["chichewa"]}</div>',
                        unsafe_allow_html=True
                    )

                with col2:
                    st.markdown("**Translation (English)**")
                    st.markdown(
                        f'<div class="result-box">{result["english"]}</div>',
                        unsafe_allow_html=True
                    )

                st.success("Translation completed successfully.")

# ======================================================
# TAB 4: ENGLISH → CHICHEWA
# ======================================================
with tab4:
    st.subheader("English to Chichewa Translation")

    english_text = st.text_area(
        "Enter English text",
        height=150
    )

    if st.button("Translate", type="primary"):
        if not english_text.strip():
            st.warning("Please enter text to translate.")
        else:
            with st.spinner("Translating..."):
                result = safe_post(
                    f"{EN_NYA_API_URL}/translate",
                    json={"text": english_text},
                    timeout=60
                )

                col1, col2 = st.columns(2)

                with col1:
                    st.markdown("**Source (English)**")
                    st.markdown(
                        f'<div class="result-box">{result["english"]}</div>',
                        unsafe_allow_html=True
                    )

                with col2:
                    st.markdown("**Translation (Chichewa)**")
                    st.markdown(
                        f'<div class="result-box">{result["chichewa"]}</div>',
                        unsafe_allow_html=True
                    )

                st.success("Translation completed successfully.")

# =============================
# Footer
# =============================
st.markdown("---")
