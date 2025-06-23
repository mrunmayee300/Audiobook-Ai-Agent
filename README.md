# 📖 Audiobook AI Agent

An intelligent web application that converts PDF books into high-quality audiobooks using AI-powered text-to-speech technology. Built with Streamlit and powered by Murf AI.

## ✨ Features

- **📥 PDF Upload**: Upload any PDF book or document
- **🧠 Smart Text Extraction**: Advanced text processing with PyMuPDF
- **🎙️ AI Voice Synthesis**: High-quality TTS using Murf AI API
- **🎧 Audio Streaming**: Listen to your audiobook directly in the browser
- **⬇️ Download Support**: Download the complete audiobook as MP3
- **⚙️ Customizable Settings**: Choose voice, chunk size, and processing options
- **📊 Progress Tracking**: Real-time progress updates during conversion

## 🏗️ Architecture

```
audiobook_ai_agent/
│
├── main.py                    # Streamlit frontend controller
├── utils/
│   ├── pdf_reader.py          # PDF extraction and text processing
│   ├── murf_api.py            # Murf AI API integration
│   └── audio_utils.py         # Audio processing and merging
│
├── .env                       # API key configuration (create from env_template.txt)
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## 🚀 Quick Start

### 1. Prerequisites

- **Python 3.8+** installed on your system
- **ffmpeg** installed and added to system PATH
- **Murf AI API key** (get one from [murf.ai](https://murf.ai/))

### 2. Installation

```bash
# Clone or download this repository
cd audiobook_ai_agent

# Install Python dependencies
pip install -r requirements.txt

# Install ffmpeg (if not already installed)
# Windows: Download from https://ffmpeg.org/download.html
# macOS: brew install ffmpeg
# Ubuntu/Debian: sudo apt install ffmpeg
```

### 3. Configuration

```bash
# Copy the environment template
cp env_template.txt .env

# Edit .env file and add your Murf API key
# MURF_API_KEY=your_actual_api_key_here
```

### 4. Run the Application

```bash
# Start the Streamlit app
streamlit run main.py
```

The app will open in your browser at `http://localhost:8501`

## 📖 Usage Guide

### Step 1: Upload PDF
- Click "Browse files" to select your PDF book
- Supported format: PDF files with readable text
- Maximum recommended file size: 50MB

### Step 2: Configure Settings
- **Choose Voice**: Select from available Murf AI voices
  - William (Male) - Professional and clear
  - Sarah (Female) - Warm and engaging
  - David (Male) - Deep and authoritative
  - Emma (Female) - Bright and friendly

- **Chunk Size**: Adjust text processing chunks
  - Smaller chunks (1000-2000): Better quality, slower processing
  - Larger chunks (3000-5000): Faster processing, good quality

### Step 3: Generate Audiobook
- Click "Generate Audiobook" to start the conversion process
- Monitor progress in real-time
- Wait for completion (processing time depends on text length)

### Step 4: Listen & Download
- Stream your audiobook directly in the browser
- Download the complete MP3 file for offline listening
- File naming: `audiobook_[original_filename].mp3`

## 🔧 Technical Details

### Text Processing Pipeline

1. **PDF Extraction**: PyMuPDF extracts text while preserving formatting
2. **Text Cleaning**: Remove artifacts, fix OCR issues, normalize spacing
3. **Chunking**: Split text into optimal sizes for TTS processing
4. **Voice Synthesis**: Murf AI converts each chunk to high-quality audio
5. **Audio Merging**: Pydub combines all chunks with smooth transitions
6. **Final Output**: High-quality MP3 audiobook with consistent audio levels

### API Integration

The app uses Murf AI's REST API for text-to-speech conversion:

```python
# Example API call
POST https://api.murf.ai/speech/generate
{
    "voiceId": "en-US-William",
    "text": "Your text here",
    "format": "mp3",
    "quality": "high"
}
```

### Audio Processing

- **Format**: MP3 with 192kbps bitrate
- **Quality**: High-quality voice synthesis
- **Transitions**: 0.5-second pauses between chunks
- **Normalization**: Consistent audio levels across the entire audiobook

## 🛠️ Troubleshooting

### Common Issues

**"MURF_API_KEY not found"**
- Ensure you've created a `.env` file from `env_template.txt`
- Verify your API key is correct and active
- Check that the `.env` file is in the project root directory

**"ffmpeg not found"**
- Install ffmpeg and add it to your system PATH
- Windows: Download from https://ffmpeg.org/download.html
- Restart your terminal/command prompt after installation

**"No text could be extracted"**
- Ensure your PDF contains readable text (not just images)
- Try a different PDF file to test
- Some scanned PDFs may require OCR preprocessing

**"API Error"**
- Check your internet connection
- Verify your Murf API key is valid and has sufficient credits
- Check Murf AI service status

### Performance Tips

- **Smaller files**: Process faster and use fewer API credits
- **Optimal chunk size**: 2000-3000 characters for best balance
- **Voice selection**: Different voices may have varying processing times
- **Network**: Stable internet connection for API calls

## 📊 System Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| Python | 3.8 | 3.9+ |
| RAM | 4GB | 8GB+ |
| Storage | 1GB free | 5GB+ free |
| Network | Broadband | High-speed |

## 🔒 Security & Privacy

- **API Keys**: Stored locally in `.env` file (never shared)
- **File Processing**: All processing happens locally
- **Data Privacy**: No files are stored on external servers
- **Temporary Files**: Automatically cleaned up after processing

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

### Development Setup

```bash
# Clone the repository
git clone <repository-url>
cd audiobook_ai_agent

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run in development mode
streamlit run main.py --server.port 8501
```

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Murf AI** for providing the text-to-speech API
- **Streamlit** for the web framework
- **PyMuPDF** for PDF processing
- **Pydub** for audio manipulation

## 📞 Support

If you encounter any issues or have questions:

1. Check the troubleshooting section above
2. Review the Murf AI documentation
3. Open an issue on the project repository
4. Contact the development team

---

**Happy Audiobook Creation! 🎧📚** 