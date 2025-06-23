import fitz  # PyMuPDF
import re

def extract_text_from_pdf(pdf_path):
    """
    Extract text from a PDF file using PyMuPDF.
    
    Args:
        pdf_path (str): Path to the PDF file
        
    Returns:
        str: Extracted text with cleaned formatting
    """
    try:
        # Open the PDF document
        doc = fitz.open(pdf_path)
        
        # Extract text from all pages
        text = ""
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            # type: ignore[attr-defined]
            page_text = page.get_text("text")
            text += page_text + "\n"
        
        # Close the document
        doc.close()
        
        # Clean up the extracted text
        cleaned_text = clean_text(text)
        
        return cleaned_text
        
    except Exception as e:
        raise Exception(f"Error extracting text from PDF: {str(e)}")

def clean_text(text):
    """
    Clean and format the extracted text for better TTS processing.
    
    Args:
        text (str): Raw extracted text
        
    Returns:
        str: Cleaned and formatted text
    """
    # Remove excessive whitespace and newlines
    text = re.sub(r'\n+', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    
    # Remove page numbers and headers/footers (common patterns)
    text = re.sub(r'\b\d+\s*$', '', text, flags=re.MULTILINE)  # Page numbers at end of lines
    text = re.sub(r'^\d+\s*', '', text, flags=re.MULTILINE)    # Page numbers at start of lines
    
    # Clean up common PDF artifacts
    text = re.sub(r'[^\w\s\.\,\!\?\;\:\-\(\)\[\]\{\}\"\']', '', text)
    
    # Fix common OCR issues
    text = text.replace('|', 'I')  # Common OCR mistake
    text = text.replace('0', 'O')  # In certain contexts
    
    # Ensure proper sentence spacing
    text = re.sub(r'\.([A-Z])', r'. \1', text)
    text = re.sub(r'\?([A-Z])', r'? \1', text)
    text = re.sub(r'\!([A-Z])', r'! \1', text)
    
    # Remove leading/trailing whitespace
    text = text.strip()
    
    return text

def get_pdf_info(pdf_path):
    """
    Get basic information about the PDF file.
    
    Args:
        pdf_path (str): Path to the PDF file
        
    Returns:
        dict: Dictionary containing PDF metadata
    """
    try:
        doc = fitz.open(pdf_path)
        
        meta = doc.metadata or {}
        info = {
            'page_count': len(doc),
            'title': meta.get('title', 'Unknown'),
            'author': meta.get('author', 'Unknown'),
            'subject': meta.get('subject', ''),
            'creator': meta.get('creator', 'Unknown')
        }
        
        doc.close()
        return info
        
    except Exception as e:
        raise Exception(f"Error getting PDF info: {str(e)}")

def estimate_reading_time(text, words_per_minute=150):
    """
    Estimate the reading time for the extracted text.
    
    Args:
        text (str): The text to estimate reading time for
        words_per_minute (int): Average reading speed in words per minute
        
    Returns:
        float: Estimated reading time in minutes
    """
    word_count = len(text.split())
    reading_time = word_count / words_per_minute
    return reading_time 