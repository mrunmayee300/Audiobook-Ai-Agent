import streamlit as st
from utils.pdf_reader import extract_text_from_pdf
from utils.audio_utils import split_text, download_and_merge
from utils.murf_api import text_to_speech_murf
import os
import tempfile

# Page configuration
st.set_page_config(
    page_title="Audiobook AI Agent",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .feature-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .info-box {
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Main header
st.markdown('<h1 class="main-header">📖 Audiobook AI Agent</h1>', unsafe_allow_html=True)

# Sidebar with app information
with st.sidebar:
    st.header("ℹ️ About")
    st.markdown("""
    This app converts your PDF books into high-quality audiobooks using AI-powered text-to-speech technology.
    
    **Features:**
    - 📥 Upload PDF files
    - 🧠 Extract and process text
    - 🎙️ Convert to human-like voice
    - 🎧 Stream and download audio
    """)
    
    st.header("⚙️ Settings")
    voice_options = {
        "William (Male)": "en-US-William",
        "Sarah (Female)": "en-US-Sarah", 
        "David (Male)": "en-US-David",
        "Emma (Female)": "en-US-Emma"
    }
    selected_voice = st.selectbox("Choose Voice", list(voice_options.keys()), index=0)
    
    chunk_size = st.slider("Text Chunk Size", min_value=1000, max_value=5000, value=3000, step=500)
    st.caption("Larger chunks = faster processing, smaller chunks = better quality")

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.header("📥 Upload Your PDF Book")
    
    uploaded_file = st.file_uploader(
        "Choose a PDF file",
        type=['pdf'],
        help="Upload a PDF book or document to convert to audiobook"
    )
    
    if uploaded_file is not None:
        # Display file info
        file_details = {
            "Filename": uploaded_file.name,
            "File size": f"{uploaded_file.size / 1024 / 1024:.2f} MB",
            "File type": uploaded_file.type
        }
        
        st.markdown('<div class="info-box">', unsafe_allow_html=True)
        st.write("**File Information:**")
        for key, value in file_details.items():
            st.write(f"• {key}: {value}")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            temp_pdf_path = tmp_file.name
        
        st.success("✅ PDF uploaded successfully!")
        
        # Generate audiobook button
        if st.button("🎙️ Generate Audiobook", type="primary", use_container_width=True):
            if not os.getenv("MURF_API_KEY"):
                st.error("❌ Murf API key not found! Please add MURF_API_KEY to your .env file.")
            else:
                # Progress tracking
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                try:
                    # Step 1: Extract text
                    status_text.text("📖 Extracting text from PDF...")
                    progress_bar.progress(10)
                    
                    text = extract_text_from_pdf(temp_pdf_path)
                    if not text.strip():
                        st.error("❌ No text could be extracted from the PDF. Please check if the PDF contains readable text.")
                        st.stop()
                    
                    # Step 2: Split text into chunks
                    status_text.text("✂️ Splitting text into manageable chunks...")
                    progress_bar.progress(20)
                    
                    chunks = split_text(text, chunk_size)
                    st.info(f"📊 Text split into {len(chunks)} chunks for processing")
                    
                    # Step 3: Convert chunks to speech
                    audio_urls = []
                    for i, chunk in enumerate(chunks):
                        status_text.text(f"🎙️ Converting chunk {i+1}/{len(chunks)} to speech...")
                        progress = 20 + (i / len(chunks)) * 60
                        progress_bar.progress(int(progress))
                        
                        # Add debug info
                        st.write(f"Debug: Processing chunk {i+1} (length: {len(chunk)} characters)")
                        
                        audio_url = text_to_speech_murf(chunk, voice_options[selected_voice])
                        if audio_url:
                            audio_urls.append(audio_url)
                            st.write(f"✅ Chunk {i+1} converted successfully")
                        else:
                            st.error(f"❌ Failed to convert chunk {i+1}")
                            st.write(f"Debug: Chunk content preview: {chunk[:100]}...")
                            st.stop()
                    
                    # Step 4: Merge audio files
                    status_text.text("🔗 Merging audio chunks...")
                    progress_bar.progress(80)
                    
                    output_filename = f"audiobook_{uploaded_file.name.replace('.pdf', '')}.mp3"
                    download_and_merge(audio_urls, output_filename)
                    
                    # Step 5: Complete
                    progress_bar.progress(100)
                    status_text.text("✅ Audiobook generation complete!")
                    
                    st.markdown('<div class="success-box">', unsafe_allow_html=True)
                    st.success("🎉 Your audiobook is ready!")
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Display audio player
                    st.header("🎧 Listen to Your Audiobook")
                    st.audio(output_filename)
                    
                    # Download button
                    with open(output_filename, "rb") as f:
                        st.download_button(
                            label="⬇️ Download Audiobook",
                            data=f.read(),
                            file_name=output_filename,
                            mime="audio/mp3",
                            use_container_width=True
                        )
                    
                    # Clean up temporary files
                    os.unlink(temp_pdf_path)
                    
                except Exception as e:
                    st.error(f"❌ An error occurred: {str(e)}")
                    # Clean up on error
                    if os.path.exists(temp_pdf_path):
                        os.unlink(temp_pdf_path)

with col2:
    st.header("📋 Instructions")
    st.markdown("""
    1. **Upload PDF**: Select your PDF book file
    2. **Choose Voice**: Pick your preferred narrator voice
    3. **Adjust Settings**: Modify chunk size if needed
    4. **Generate**: Click the button to start conversion
    5. **Listen & Download**: Stream or download your audiobook
    
    **Tips:**
    - Ensure your PDF has readable text (not just images)
    - Larger files may take longer to process
    - Use smaller chunk sizes for better audio quality
    """)
    
    st.header("🔧 Requirements")
    st.markdown("""
    - Murf API key in `.env` file
    - ffmpeg installed on your system
    - Stable internet connection
    """)

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666;'>"
    "Built with ❤️ using Streamlit and Murf AI"
    "</div>",
    unsafe_allow_html=True
) 