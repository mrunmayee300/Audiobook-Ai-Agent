import requests
import os
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class MurfAPI:
    """Class to handle Murf AI API interactions for text-to-speech conversion."""
    
    def __init__(self):
        self.api_key = os.getenv("MURF_API_KEY")
        self.base_url = "https://api.murf.ai"
        
        if not self.api_key:
            raise ValueError("MURF_API_KEY not found in environment variables")
    
    def text_to_speech(self, text, voice_id="en-US-William", format="mp3"):
        """
        Convert text to speech using Murf AI API.
        
        Args:
            text (str): Text to convert to speech
            voice_id (str): Voice ID to use for synthesis
            format (str): Audio format (mp3, wav, etc.)
            
        Returns:
            str: URL to the generated audio file, or None if failed
        """
        try:
            # API endpoint for speech generation
            url = f"{self.base_url}/api/v1/speech/generate"
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "voiceId": voice_id,
                "text": text,
                "format": format,
                "quality": "high"
            }
            
            print(f"Making API request to {url}")
            print(f"Voice ID: {voice_id}")
            print(f"Text length: {len(text)} characters")
            
            # Make the API request
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            
            print(f"API Response Status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                audio_url = result.get("audioUrl")
                print(f"Audio URL received: {audio_url}")
                return audio_url
            else:
                print(f"API Error: {response.status_code}")
                print(f"Response text: {response.text}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"Request error: {str(e)}")
            return None
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            return None
    
    def get_available_voices(self):
        """
        Get list of available voices from Murf AI.
        
        Returns:
            list: List of available voice dictionaries
        """
        try:
            url = f"{self.base_url}/voices"
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            response = requests.get(url, headers=headers, timeout=30)
            
            if response.status_code == 200:
                return response.json().get("voices", [])
            else:
                print(f"Error fetching voices: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"Error getting voices: {str(e)}")
            return []
    
    def check_api_status(self):
        """
        Check if the API key is valid and the service is accessible.
        
        Returns:
            bool: True if API is accessible, False otherwise
        """
        try:
            url = f"{self.base_url}/voices"
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            return response.status_code == 200
            
        except Exception:
            return False

# Global instance for easy access
_murf_api = None

def get_murf_api():
    """Get or create a MurfAPI instance."""
    global _murf_api
    if _murf_api is None:
        _murf_api = MurfAPI()
    return _murf_api

def text_to_speech_murf(text, voice_id="en-US-William"):
    """
    Convenience function to convert text to speech using Murf AI.
    
    Args:
        text (str): Text to convert to speech
        voice_id (str): Voice ID to use for synthesis
        
    Returns:
        str: URL to the generated audio file, or None if failed
    """
    try:
        api = get_murf_api()
        return api.text_to_speech(text, voice_id)
    except Exception as e:
        print(f"Error in text_to_speech_murf: {str(e)}")
        return None

def validate_text_for_tts(text):
    """
    Validate and clean text for TTS processing.
    
    Args:
        text (str): Text to validate
        
    Returns:
        str: Cleaned text suitable for TTS
    """
    if not text or not text.strip():
        return ""
    
    # Remove excessive whitespace
    text = " ".join(text.split())
    
    # Ensure text ends with proper punctuation
    if text and text[-1] not in '.!?':
        text += '.'
    
    return text

def split_text_for_tts(text, max_length=3000):
    """
    Split text into chunks suitable for TTS processing.
    
    Args:
        text (str): Text to split
        max_length (int): Maximum length of each chunk
        
    Returns:
        list: List of text chunks
    """
    if len(text) <= max_length:
        return [text]
    
    # Split by sentences first
    sentences = text.split('. ')
    chunks = []
    current_chunk = ""
    
    for sentence in sentences:
        # Add period back if it's not the last sentence
        if sentence != sentences[-1]:
            sentence += '. '
        
        if len(current_chunk + sentence) <= max_length:
            current_chunk += sentence
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = sentence
    
    # Add the last chunk
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    return chunks 