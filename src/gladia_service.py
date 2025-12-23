import os
import time
import requests
from typing import Optional, Dict, Any

from .config import GLADIA_API_KEY, GLADIA_API_URL, GLADIA_UPLOAD_URL


class GladiaService:
    """
    Handles audio transcription using Gladia API.
    Supports uploading audio files and retrieving transcriptions.
    """

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or GLADIA_API_KEY
        if self.api_key == "your-gladia-key-here":
            raise ValueError("Please set a valid Gladia API key in config.py or environment")

        self.headers = {
            "x-gladia-key": self.api_key,
        }

    def transcribe_file(
        self,
        file_path: str,
        language: str = "tr",
        on_progress: Optional[callable] = None,
    ) -> Dict[str, Any]:
        """
        Transcribes an audio file using Gladia API.

        Args:
            file_path: Path to the audio file
            language: Language code (default: 'tr' for Turkish)
            on_progress: Optional callback for progress updates

        Returns:
            Dictionary containing transcription result
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Audio file not found: {file_path}")

        # Step 1: Upload the audio file
        if on_progress:
            on_progress("Dosya yükleniyor...")

        audio_url = self._upload_file(file_path)

        # Step 2: Start transcription
        if on_progress:
            on_progress("Transkripsiyon başlatılıyor...")

        transcription_id = self._start_transcription(audio_url, language)

        # Step 3: Poll for results
        result = self._poll_for_result(transcription_id, on_progress)

        return result

    def _upload_file(self, file_path: str) -> str:
        """Uploads audio file to Gladia and returns the audio URL."""
        with open(file_path, "rb") as audio_file:
            files = {"audio": (os.path.basename(file_path), audio_file, "audio/wav")}

            response = requests.post(
                GLADIA_UPLOAD_URL,
                headers=self.headers,
                files=files,
            )

        if response.status_code != 200 and response.status_code != 201:
            raise Exception(f"Upload failed: {response.status_code} - {response.text}")

        data = response.json()
        return data.get("audio_url")

    def _start_transcription(self, audio_url: str, language: str) -> str:
        """Starts a transcription job and returns the transcription ID."""
        payload = {
            "audio_url": audio_url,
            "language": language,
            "enable_code_switching": False,
        }

        headers = {
            **self.headers,
            "Content-Type": "application/json",
        }

        response = requests.post(
            GLADIA_API_URL,
            headers=headers,
            json=payload,
        )

        if response.status_code != 200 and response.status_code != 201:
            raise Exception(f"Transcription start failed: {response.status_code} - {response.text}")

        data = response.json()
        return data.get("id")

    def _poll_for_result(
        self,
        transcription_id: str,
        on_progress: Optional[callable] = None,
        max_wait_seconds: int = 600,
        poll_interval: int = 2,
    ) -> Dict[str, Any]:
        """Polls for transcription result until complete or timeout."""
        result_url = f"{GLADIA_API_URL}/{transcription_id}"
        start_time = time.time()

        while time.time() - start_time < max_wait_seconds:
            response = requests.get(result_url, headers=self.headers)

            if response.status_code != 200:
                raise Exception(f"Poll failed: {response.status_code} - {response.text}")

            data = response.json()
            status = data.get("status")

            if status == "done":
                return self._parse_result(data)

            if status == "error":
                raise Exception(f"Transcription failed: {data.get('error_message', 'Unknown error')}")

            if on_progress:
                elapsed = int(time.time() - start_time)
                on_progress(f"İşleniyor... ({elapsed}s)")

            time.sleep(poll_interval)

        raise TimeoutError("Transcription timed out")

    def _parse_result(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Parses the transcription result into a clean format."""
        result = data.get("result", {})
        transcription = result.get("transcription", {})

        # Extract full transcript text
        full_text = transcription.get("full_transcript", "")

        # Extract utterances with timestamps
        utterances = []
        for utterance in transcription.get("utterances", []):
            utterances.append({
                "start": utterance.get("start", 0),
                "end": utterance.get("end", 0),
                "text": utterance.get("text", ""),
                "speaker": utterance.get("speaker", 0),
            })

        return {
            "full_text": full_text,
            "utterances": utterances,
            "language": transcription.get("language", "tr"),
            "duration": result.get("metadata", {}).get("audio_duration", 0),
        }


def format_transcript(result: Dict[str, Any], include_timestamps: bool = True) -> str:
    """
    Formats transcription result as readable text.

    Args:
        result: Transcription result dictionary
        include_timestamps: Whether to include timestamps

    Returns:
        Formatted transcript string
    """
    if not include_timestamps:
        return result.get("full_text", "")

    lines = []
    for utterance in result.get("utterances", []):
        start = utterance["start"]
        minutes = int(start // 60)
        seconds = int(start % 60)
        timestamp = f"[{minutes:02d}:{seconds:02d}]"
        lines.append(f"{timestamp} {utterance['text']}")

    return "\n".join(lines)
