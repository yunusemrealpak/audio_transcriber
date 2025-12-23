import os
import time
import threading
import numpy as np
import sounddevice as sd
import soundfile as sf
from datetime import datetime
from typing import Callable, Optional, List, Tuple

from config import SAMPLE_RATE, BLOCK_DURATION_MINUTES, RECORDINGS_DIR


class AudioRecorder:
    """
    Handles audio recording from microphone and system audio (loopback).
    Automatically splits recordings into configurable time blocks.
    """

    def __init__(
        self,
        on_block_created: Optional[Callable[[str], None]] = None,
        block_duration_minutes: int = BLOCK_DURATION_MINUTES,
    ):
        self.sample_rate = SAMPLE_RATE
        self.block_duration = block_duration_minutes * 60  # Convert to seconds
        self.on_block_created = on_block_created

        self.is_recording = False
        self.recorded_blocks: List[str] = []

        self._mic_stream = None
        self._loopback_stream = None
        self._recording_thread = None
        self._mic_buffer = []
        self._loopback_buffer = []
        self._start_time = None
        self._current_block_start = None
        self._lock = threading.Lock()
        self._output_channels = 1  # Will be set based on device capabilities

        # Ensure recordings directory exists
        os.makedirs(RECORDINGS_DIR, exist_ok=True)

    def _get_device_channels(self, device_id: int) -> int:
        """Returns the number of input channels for a device (max 2)."""
        device_info = sd.query_devices(device_id)
        return min(device_info["max_input_channels"], 2)

    def get_input_devices(self) -> List[Tuple[int, str]]:
        """Returns a list of available input devices (microphones)."""
        devices = []
        for i, device in enumerate(sd.query_devices()):
            if device["max_input_channels"] > 0:
                devices.append((i, device["name"]))
        return devices

    def get_loopback_devices(self) -> List[Tuple[int, str]]:
        """
        Returns a list of available loopback devices (system audio).
        On Windows, looks for devices with 'Stereo Mix', 'What U Hear', 'Loopback', or WASAPI loopback.
        """
        devices = []
        loopback_keywords = [
            "stereo mix",
            "stereo karışımı",
            "what u hear",
            "loopback",
            "wave out",
            "wasapi",
            "sistem sesi",
            "system audio",
            "motiv mix",
        ]

        for i, device in enumerate(sd.query_devices()):
            if device["max_input_channels"] > 0:
                name_lower = device["name"].lower()
                if any(keyword in name_lower for keyword in loopback_keywords):
                    devices.append((i, device["name"]))

        return devices

    def get_all_input_devices(self) -> List[Tuple[int, str, int]]:
        """
        Returns all input devices with their channel count for debugging.
        Returns: List of (device_id, name, max_channels)
        """
        devices = []
        for i, device in enumerate(sd.query_devices()):
            if device["max_input_channels"] > 0:
                devices.append((i, device["name"], device["max_input_channels"]))
        return devices

    def start_recording(
        self,
        mic_device_id: Optional[int] = None,
        loopback_device_id: Optional[int] = None,
    ) -> bool:
        """
        Starts recording from specified devices.
        At least one device must be specified.
        """
        if self.is_recording:
            return False

        if mic_device_id is None and loopback_device_id is None:
            raise ValueError("At least one audio source must be specified")

        self.is_recording = True
        self._mic_buffer = []
        self._loopback_buffer = []
        self._start_time = time.time()
        self._current_block_start = self._start_time
        self.recorded_blocks = []

        self._recording_thread = threading.Thread(
            target=self._recording_loop,
            args=(mic_device_id, loopback_device_id),
            daemon=True,
        )
        self._recording_thread.start()

        return True

    def stop_recording(self) -> List[str]:
        """Stops recording and returns list of recorded block file paths."""
        if not self.is_recording:
            return self.recorded_blocks

        self.is_recording = False

        if self._recording_thread:
            self._recording_thread.join(timeout=2.0)

        # Save any remaining audio as final block
        self._save_current_block()

        return self.recorded_blocks

    def _recording_loop(
        self, mic_device_id: Optional[int], loopback_device_id: Optional[int]
    ):
        """Main recording loop that captures audio from devices."""
        try:
            streams = []

            if mic_device_id is not None:
                mic_channels = self._get_device_channels(mic_device_id)
                self._output_channels = max(self._output_channels, mic_channels)
                print(f"Mic device {mic_device_id}: {mic_channels} channels")

                mic_stream = sd.InputStream(
                    samplerate=self.sample_rate,
                    channels=mic_channels,
                    device=mic_device_id,
                    callback=self._mic_callback,
                    blocksize=1024,
                )
                streams.append(mic_stream)
                mic_stream.start()
                print("Mic stream started successfully")

            if loopback_device_id is not None:
                loopback_channels = self._get_device_channels(loopback_device_id)
                self._output_channels = max(self._output_channels, loopback_channels)
                print(f"Loopback device {loopback_device_id}: {loopback_channels} channels")

                loopback_stream = sd.InputStream(
                    samplerate=self.sample_rate,
                    channels=loopback_channels,
                    device=loopback_device_id,
                    callback=self._loopback_callback,
                    blocksize=1024,
                )
                streams.append(loopback_stream)
                loopback_stream.start()
                print("Loopback stream started successfully")

            print(f"Recording started with {len(streams)} stream(s)")

            while self.is_recording:
                time.sleep(0.1)

                # Check if we need to create a new block
                elapsed = time.time() - self._current_block_start
                if elapsed >= self.block_duration:
                    self._save_current_block()
                    self._current_block_start = time.time()

            # Stop all streams
            for stream in streams:
                stream.stop()
                stream.close()

            print("Recording stopped, streams closed")

        except Exception as e:
            print(f"Recording error: {e}")
            import traceback
            traceback.print_exc()
            self.is_recording = False

    def _mic_callback(self, indata, frames, time_info, status):
        """Callback for microphone audio data."""
        if status:
            print(f"Mic status: {status}")
        with self._lock:
            self._mic_buffer.append(indata.copy())

    def _loopback_callback(self, indata, frames, time_info, status):
        """Callback for loopback audio data."""
        if status:
            print(f"Loopback status: {status}")
        with self._lock:
            self._loopback_buffer.append(indata.copy())

    def _save_current_block(self):
        """Saves current audio buffer as a block file."""
        with self._lock:
            if not self._mic_buffer and not self._loopback_buffer:
                return

            # Mix audio sources
            mixed_audio = self._mix_audio()

            if mixed_audio is None or len(mixed_audio) == 0:
                return

            # Generate filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            block_num = len(self.recorded_blocks) + 1
            filename = f"block_{block_num:03d}_{timestamp}.wav"
            filepath = os.path.join(RECORDINGS_DIR, filename)

            # Save audio file
            sf.write(filepath, mixed_audio, self.sample_rate)

            self.recorded_blocks.append(filepath)

            # Clear buffers
            self._mic_buffer = []
            self._loopback_buffer = []

            # Notify callback
            if self.on_block_created:
                self.on_block_created(filepath)

    def _mix_audio(self) -> Optional[np.ndarray]:
        """Mixes microphone and loopback audio into a single array."""
        mic_audio = None
        loopback_audio = None

        if self._mic_buffer:
            mic_audio = np.concatenate(self._mic_buffer, axis=0)

        if self._loopback_buffer:
            loopback_audio = np.concatenate(self._loopback_buffer, axis=0)

        if mic_audio is None and loopback_audio is None:
            return None

        if mic_audio is None:
            return loopback_audio

        if loopback_audio is None:
            return mic_audio

        # Mix both sources - align lengths
        min_len = min(len(mic_audio), len(loopback_audio))
        mic_audio = mic_audio[:min_len]
        loopback_audio = loopback_audio[:min_len]

        # Average the two sources
        mixed = (mic_audio + loopback_audio) / 2.0

        return mixed.astype(np.float32)

    def get_recording_duration(self) -> float:
        """Returns current recording duration in seconds."""
        if not self.is_recording or self._start_time is None:
            return 0.0
        return time.time() - self._start_time

    def get_current_block_duration(self) -> float:
        """Returns current block duration in seconds."""
        if not self.is_recording or self._current_block_start is None:
            return 0.0
        return time.time() - self._current_block_start
