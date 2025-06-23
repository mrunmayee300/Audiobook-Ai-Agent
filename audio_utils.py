from pydub import AudioSegment
from io import BytesIO
import requests
import os
import tempfile
import re

def split_text(text, chunk_size=3000):
    """
    Split text into chunks of specified size, trying to break at sentence boundaries.
    
    Args:
        text (str): Text to split
        chunk_size (int): Maximum size of each chunk
        
    Returns:
        list: List of text chunks
    """
    if len(text) <= chunk_size:
        return [text]
    
    # Split by sentences first
    sentences = re.split(r'(?<=[.!?])\s+', text)
    chunks = []
    current_chunk = ""
    
    for sentence in sentences:
        # If adding this sentence would exceed chunk size
        if len(current_chunk + sentence) > chunk_size and current_chunk:
            chunks.append(current_chunk.strip())
            current_chunk = sentence
        else:
            current_chunk += " " + sentence if current_chunk else sentence
    
    # Add the last chunk
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    # If any chunk is still too long, force split
    final_chunks = []
    for chunk in chunks:
        if len(chunk) > chunk_size:
            # Force split at word boundaries
            words = chunk.split()
            temp_chunk = ""
            for word in words:
                if len(temp_chunk + " " + word) <= chunk_size:
                    temp_chunk += " " + word if temp_chunk else word
                else:
                    if temp_chunk:
                        final_chunks.append(temp_chunk.strip())
                    temp_chunk = word
            if temp_chunk:
                final_chunks.append(temp_chunk.strip())
        else:
            final_chunks.append(chunk)
    
    return final_chunks

def download_audio_from_url(url, timeout=30):
    """
    Download audio file from URL.
    
    Args:
        url (str): URL to download audio from
        timeout (int): Request timeout in seconds
        
    Returns:
        AudioSegment: Downloaded audio segment
    """
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        
        # Create audio segment from response content
        audio = AudioSegment.from_file(BytesIO(response.content), format="mp3")
        return audio
        
    except requests.exceptions.RequestException as e:
        print(f"Error downloading audio from {url}: {str(e)}")
        return None
    except Exception as e:
        print(f"Error processing audio from {url}: {str(e)}")
        return None

def download_and_merge(audio_urls, output_path="audiobook.mp3"):
    """
    Download multiple audio files and merge them into a single file.
    
    Args:
        audio_urls (list): List of audio URLs to download and merge
        output_path (str): Path for the output merged audio file
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        if not audio_urls:
            print("No audio URLs provided")
            return False
        
        print(f"Downloading and merging {len(audio_urls)} audio chunks...")
        
        # Download and merge audio segments
        final_audio = AudioSegment.empty()
        
        for i, url in enumerate(audio_urls):
            print(f"Processing chunk {i+1}/{len(audio_urls)}...")
            
            audio_segment = download_audio_from_url(url)
            if audio_segment is None:
                print(f"Failed to download audio from {url}")
                continue
            
            # Add a small pause between chunks for better flow
            if final_audio:
                pause = AudioSegment.silent(duration=500)  # 0.5 second pause
                final_audio += pause
            
            final_audio += audio_segment
        
        if not final_audio:
            print("No audio segments were successfully downloaded")
            return False
        
        # Export the merged audio
        print(f"Exporting merged audio to {output_path}...")
        final_audio.export(output_path, format="mp3", bitrate="192k")
        
        print(f"Successfully created audiobook: {output_path}")
        return True
        
    except Exception as e:
        print(f"Error merging audio files: {str(e)}")
        return False

def get_audio_duration(audio_path):
    """
    Get the duration of an audio file.
    
    Args:
        audio_path (str): Path to the audio file
        
    Returns:
        float: Duration in seconds
    """
    try:
        audio = AudioSegment.from_mp3(audio_path)
        return len(audio) / 1000.0  # Convert milliseconds to seconds
    except Exception as e:
        print(f"Error getting audio duration: {str(e)}")
        return 0

def format_duration(seconds):
    """
    Format duration in seconds to human-readable format.
    
    Args:
        seconds (float): Duration in seconds
        
    Returns:
        str: Formatted duration string
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    
    if hours > 0:
        return f"{hours}h {minutes}m {secs}s"
    elif minutes > 0:
        return f"{minutes}m {secs}s"
    else:
        return f"{secs}s"

def normalize_audio(audio_segment):
    """
    Normalize audio volume for consistent levels.
    
    Args:
        audio_segment (AudioSegment): Audio segment to normalize
        
    Returns:
        AudioSegment: Normalized audio segment
    """
    try:
        # Normalize to -20 dBFS
        normalized = audio_segment.normalize()
        return normalized
    except Exception as e:
        print(f"Error normalizing audio: {str(e)}")
        return audio_segment

def add_fade_effects(audio_segment, fade_in_ms=100, fade_out_ms=100):
    """
    Add fade in and fade out effects to audio.
    
    Args:
        audio_segment (AudioSegment): Audio segment to process
        fade_in_ms (int): Fade in duration in milliseconds
        fade_out_ms (int): Fade out duration in milliseconds
        
    Returns:
        AudioSegment: Audio segment with fade effects
    """
    try:
        # Add fade in
        if fade_in_ms > 0:
            audio_segment = audio_segment.fade_in(fade_in_ms)
        
        # Add fade out
        if fade_out_ms > 0:
            audio_segment = audio_segment.fade_out(fade_out_ms)
        
        return audio_segment
    except Exception as e:
        print(f"Error adding fade effects: {str(e)}")
        return audio_segment

def estimate_processing_time(text_length, chunks_count):
    """
    Estimate the time needed to process text to speech.
    
    Args:
        text_length (int): Length of text in characters
        chunks_count (int): Number of text chunks
        
    Returns:
        float: Estimated processing time in minutes
    """
    # Rough estimation: 1 character = 0.1 seconds of audio
    audio_duration = text_length * 0.1 / 60  # Convert to minutes
    
    # Add overhead for API calls and processing
    overhead = chunks_count * 0.5  # 30 seconds per chunk
    
    return audio_duration + overhead 