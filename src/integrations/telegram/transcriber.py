"""Audio transcription service with Groq Whisper (default) and Gemini (fallback)."""

import io
from typing import Literal
from groq import Groq, RateLimitError
from agno.agent import Agent
from agno.models.google import Gemini
from agno.media import Audio
from src.config import settings
from src.logger import logger


class AudioTranscriber:
    """Transcribe audio using Groq Whisper (free) or Gemini (fallback)."""

    def __init__(self, provider: Literal["groq", "gemini"] = "groq"):
        """Initialize transcriber.
        
        Args:
            provider: Transcription provider ("groq" or "gemini")
        """
        self.provider = provider
        
        if provider == "groq":
            groq_api_key = getattr(settings, 'groq_api_key', None)
            if not groq_api_key:
                logger.warning("GROQ_API_KEY not found, falling back to Gemini")
                self.provider = "gemini"
                self._init_gemini()
            else:
                self.client = Groq(api_key=groq_api_key)
                logger.info("Audio transcriber initialized with Groq Whisper (free)")
        else:
            self._init_gemini()
        
        # Always initialize Gemini as fallback
        if self.provider == "groq":
            self._init_gemini()
    
    def _init_gemini(self):
        """Initialize Gemini transcriber."""
        self.agent = Agent(
            model=Gemini(id="gemini-2.0-flash-exp"),
            markdown=False,
        )
        if self.provider == "gemini":
            logger.info("Audio transcriber initialized with Gemini (paid)")

    def transcribe(self, audio_bytes: bytes, format: str = "ogg") -> str:
        """Transcribe audio to text.
        
        Args:
            audio_bytes: Audio file bytes
            format: Audio format (ogg, mp3, wav, etc.)
            
        Returns:
            Transcribed text
        """
        if self.provider == "groq":
            try:
                return self._transcribe_groq(audio_bytes, format)
            except RateLimitError as e:
                logger.warning(f"Groq rate limit exceeded, falling back to Gemini | error={str(e)}")
                return self._transcribe_gemini(audio_bytes, format)
            except Exception as e:
                logger.error(f"Groq transcription failed, falling back to Gemini | error={str(e)}")
                return self._transcribe_gemini(audio_bytes, format)
        else:
            return self._transcribe_gemini(audio_bytes, format)
    
    def _transcribe_groq(self, audio_bytes: bytes, format: str) -> str:
        """Transcribe using Groq Whisper (free)."""
        logger.info(f"Transcribing with Groq | format={format} size={len(audio_bytes)} bytes")
        
        audio_file = io.BytesIO(audio_bytes)
        audio_file.name = f"audio.{format}"
        
        transcription = self.client.audio.transcriptions.create(
            file=audio_file,
            model="whisper-large-v3-turbo",
            response_format="text"
        )
        
        text = transcription.strip()
        logger.info(f"Groq transcription complete | length={len(text)} chars")
        return text
    
    def _transcribe_gemini(self, audio_bytes: bytes, format: str) -> str:
        """Transcribe using Gemini (paid fallback)."""
        logger.info(f"Transcribing with Gemini | format={format} size={len(audio_bytes)} bytes")
        
        response = self.agent.run(
            "Transcribe this audio to text. Return only the transcribed text, nothing else.",
            audio=[Audio(content=audio_bytes, format=format)]
        )
        
        text = response.content.strip()
        logger.info(f"Gemini transcription complete | length={len(text)} chars")
        return text
