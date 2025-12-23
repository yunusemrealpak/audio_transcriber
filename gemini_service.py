from google import genai
from typing import Optional

from config import GEMINI_API_KEY, GEMINI_MODEL


class GeminiService:
    """
    Handles note generation from transcripts using Gemini AI.
    """

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or GEMINI_API_KEY
        if self.api_key == "your-gemini-key-here":
            raise ValueError("Please set a valid Gemini API key in config.py or environment")

        self.client = genai.Client(api_key=self.api_key)
        self.model = GEMINI_MODEL

    def generate_notes(
        self,
        transcript: str,
        custom_prompt: Optional[str] = None,
    ) -> str:
        """
        Generates structured notes from a transcript using Gemini.

        Args:
            transcript: The transcript text to summarize
            custom_prompt: Optional custom prompt to use

        Returns:
            Generated notes as markdown string
        """
        if not transcript or not transcript.strip():
            raise ValueError("Transcript is empty")

        prompt = custom_prompt or self._get_default_prompt()
        full_prompt = f"{prompt}\n\n---\n\nTranskript:\n{transcript}"

        response = self.client.models.generate_content(
            model=self.model,
            contents=full_prompt,
        )

        return response.text

    def _get_default_prompt(self) -> str:
        """Returns the default note generation prompt."""
        return """Sen bir toplantı/ders notu çıkarma asistanısın.
Aşağıdaki transkripti analiz et ve yapılandırılmış notlar oluştur.

Notların şu formatta olmalı:

## Özet
(2-3 cümlelik genel özet)

## Ana Konular
(Tartışılan ana konuların listesi)

## Önemli Noktalar
(Dikkat çeken önemli bilgiler, kararlar, fikirler)

## Eylem Maddeleri
(Varsa yapılması gereken işler, görevler)

## Anahtar Kelimeler
(İçerikle ilgili anahtar kelimeler)

Notları Türkçe olarak, açık ve anlaşılır bir şekilde yaz.
Gereksiz detayları atla, önemli bilgilere odaklan.
Markdown formatını kullan."""

    def generate_summary(self, transcript: str) -> str:
        """
        Generates a brief summary of the transcript.

        Args:
            transcript: The transcript text

        Returns:
            Brief summary string
        """
        prompt = """Aşağıdaki transkriptin kısa bir özetini yaz (maksimum 3-4 cümle).
Sadece en önemli noktaları içer.

Transkript:
"""
        full_prompt = f"{prompt}\n{transcript}"
        response = self.client.models.generate_content(
            model=self.model,
            contents=full_prompt,
        )
        return response.text

    def extract_action_items(self, transcript: str) -> str:
        """
        Extracts action items from the transcript.

        Args:
            transcript: The transcript text

        Returns:
            List of action items as string
        """
        prompt = """Aşağıdaki transkriptten yapılması gereken işleri (action items) çıkar.
Her maddeyi "- [ ]" formatında listele.
Eğer yapılacak iş yoksa "Yapılacak iş bulunamadı." yaz.

Transkript:
"""
        full_prompt = f"{prompt}\n{transcript}"
        response = self.client.models.generate_content(
            model=self.model,
            contents=full_prompt,
        )
        return response.text


def save_notes_to_markdown(notes: str, output_path: str) -> None:
    """
    Saves generated notes to a markdown file.

    Args:
        notes: The notes content
        output_path: Path to save the markdown file
    """
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(notes)
