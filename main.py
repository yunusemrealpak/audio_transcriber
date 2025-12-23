import os
import threading
import tkinter as tk
from tkinter import messagebox, filedialog
from datetime import datetime
from typing import Optional, List, Dict
import sounddevice as sd
import soundfile as sf
import numpy as np

import customtkinter as ctk

from src.audio_recorder import AudioRecorder
from src.gladia_service import GladiaService, format_transcript
from src.gemini_service import GeminiService, save_notes_to_markdown
from src.config import RECORDINGS_DIR


class BlockCard(ctk.CTkFrame):
    """
    A card widget representing a single audio block.
    Includes play/pause, selection, duration, and status.
    """

    def __init__(
        self,
        parent,
        filepath: str,
        on_selection_change: callable,
        on_delete: callable,
        **kwargs
    ):
        super().__init__(parent, **kwargs)

        self.filepath = filepath
        self.on_selection_change = on_selection_change
        self.on_delete = on_delete
        self.is_selected = True
        self.is_playing = False
        self.playback_thread = None
        self.stop_playback_flag = False

        # Get audio duration
        self.duration = self._get_duration()

        self._create_widgets()
        self._update_selection_style()

    def _get_duration(self) -> float:
        """Returns the duration of the audio file in seconds."""
        try:
            info = sf.info(self.filepath)
            return info.duration
        except:
            return 0.0

    def _format_duration(self, seconds: float) -> str:
        """Formats seconds as MM:SS."""
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes:02d}:{secs:02d}"

    def _create_widgets(self):
        """Creates the card widgets."""
        self.configure(corner_radius=8, border_width=2, border_color="gray30")

        # Main container with padding
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="x", padx=8, pady=6)

        # Left side: Play button
        self.play_button = ctk.CTkButton(
            container,
            text="▶",
            width=36,
            height=36,
            corner_radius=18,
            fg_color="#1DB954",
            hover_color="#1ed760",
            command=self._toggle_playback,
        )
        self.play_button.pack(side="left", padx=(0, 10))

        # Middle: Info
        info_frame = ctk.CTkFrame(container, fg_color="transparent")
        info_frame.pack(side="left", fill="x", expand=True)

        # Filename
        filename = os.path.basename(self.filepath)
        display_name = filename.replace(".wav", "").replace("block_", "Blok ")

        self.name_label = ctk.CTkLabel(
            info_frame,
            text=display_name,
            font=ctk.CTkFont(size=13, weight="bold"),
            anchor="w",
        )
        self.name_label.pack(anchor="w")

        # Duration and status
        status_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
        status_frame.pack(anchor="w", fill="x")

        self.duration_label = ctk.CTkLabel(
            status_frame,
            text=f"⏱ {self._format_duration(self.duration)}",
            font=ctk.CTkFont(size=11),
            text_color="gray60",
        )
        self.duration_label.pack(side="left")

        self.status_label = ctk.CTkLabel(
            status_frame,
            text="",
            font=ctk.CTkFont(size=11),
            text_color="#3498db",
        )
        self.status_label.pack(side="left", padx=(10, 0))

        # Right side: Selection checkbox and delete
        right_frame = ctk.CTkFrame(container, fg_color="transparent")
        right_frame.pack(side="right")

        self.delete_button = ctk.CTkButton(
            right_frame,
            text="🗑",
            width=30,
            height=30,
            fg_color="transparent",
            hover_color="gray30",
            command=self._on_delete_click,
        )
        self.delete_button.pack(side="right", padx=(5, 0))

        self.select_checkbox = ctk.CTkCheckBox(
            right_frame,
            text="",
            width=24,
            checkbox_width=24,
            checkbox_height=24,
            command=self._on_selection_toggle,
        )
        self.select_checkbox.pack(side="right")
        self.select_checkbox.select()

        # Progress bar for playback
        self.progress_bar = ctk.CTkProgressBar(self, height=3)
        self.progress_bar.pack(fill="x", padx=8, pady=(0, 4))
        self.progress_bar.set(0)

    def _toggle_playback(self):
        """Toggles audio playback."""
        if self.is_playing:
            self._stop_playback()
        else:
            self._start_playback()

    def _start_playback(self):
        """Starts audio playback."""
        if self.is_playing:
            return

        self.is_playing = True
        self.stop_playback_flag = False
        self.play_button.configure(text="⏸", fg_color="#e74c3c", hover_color="#c0392b")

        self.playback_thread = threading.Thread(target=self._playback_worker, daemon=True)
        self.playback_thread.start()

    def _stop_playback(self):
        """Stops audio playback."""
        self.stop_playback_flag = True
        sd.stop()
        self.is_playing = False
        self.play_button.configure(text="▶", fg_color="#1DB954", hover_color="#1ed760")
        self.progress_bar.set(0)

    def _playback_worker(self):
        """Background worker for audio playback."""
        import time

        try:
            data, samplerate = sf.read(self.filepath)

            # Start playback
            sd.play(data, samplerate)

            # Track progress based on time
            start_time = time.time()

            while not self.stop_playback_flag:
                elapsed = time.time() - start_time

                # Check if playback finished
                if elapsed >= self.duration:
                    break

                # Update progress bar
                progress = min(elapsed / self.duration, 1.0) if self.duration > 0 else 0
                self.after(0, lambda p=progress: self.progress_bar.set(p))

                time.sleep(0.1)

            # Playback finished naturally
            if not self.stop_playback_flag:
                self.after(0, lambda: self.progress_bar.set(1.0))
                time.sleep(0.2)
                self.after(0, self._on_playback_finished)

        except Exception as e:
            print(f"Playback error: {e}")
            self.after(0, self._on_playback_finished)

    def _on_playback_finished(self):
        """Called when playback finishes."""
        self.is_playing = False
        self.play_button.configure(text="▶", fg_color="#1DB954", hover_color="#1ed760")
        self.progress_bar.set(0)

    def _on_selection_toggle(self):
        """Handles selection toggle."""
        self.is_selected = self.select_checkbox.get()
        self._update_selection_style()
        self.on_selection_change()

    def _update_selection_style(self):
        """Updates card style based on selection state."""
        if self.is_selected:
            self.configure(border_color="#3498db", fg_color="gray17")
        else:
            self.configure(border_color="gray30", fg_color="gray20")

    def _on_delete_click(self):
        """Handles delete button click."""
        self._stop_playback()
        self.on_delete(self.filepath)

    def set_selected(self, selected: bool):
        """Sets the selection state."""
        self.is_selected = selected
        if selected:
            self.select_checkbox.select()
        else:
            self.select_checkbox.deselect()
        self._update_selection_style()

    def set_status(self, status: str):
        """Sets the status text."""
        self.status_label.configure(text=status)

    def destroy(self):
        """Cleanup before destroying."""
        self._stop_playback()
        super().destroy()


class AudioTranscriberApp(ctk.CTk):
    """
    Main application window for Audio Transcriber.
    Provides UI for recording, transcribing, and generating notes.
    """

    def __init__(self):
        super().__init__()

        self.title("Audio Transcriber")
        self.geometry("1100x750")
        self.minsize(900, 650)

        # Set appearance
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Initialize services
        self.recorder = AudioRecorder(on_block_created=self._on_block_created)
        self.gladia_service: Optional[GladiaService] = None
        self.gemini_service: Optional[GeminiService] = None

        # Log available audio devices
        print("\n=== Available Audio Input Devices ===")
        for dev_id, name, channels in self.recorder.get_all_input_devices():
            print(f"  [{dev_id}] {name} ({channels} ch)")
        print("=====================================\n")

        # State
        self.is_recording = False
        self.block_cards: Dict[str, BlockCard] = {}
        self.transcripts: dict = {}
        self.current_notes: str = ""

        # Build UI
        self._create_widgets()
        self._load_existing_blocks()
        self._update_timer()

    def _create_widgets(self):
        """Creates all UI widgets."""
        # Main container with grid layout
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.main_frame.grid_columnconfigure(0, weight=0, minsize=320)
        self.main_frame.grid_columnconfigure(1, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)

        # Left panel - Recording controls and blocks
        self.left_panel = ctk.CTkFrame(self.main_frame)
        self.left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        self._create_recording_controls()
        self._create_blocks_panel()

        # Right panel - Transcript and Notes
        self.right_panel = ctk.CTkFrame(self.main_frame)
        self.right_panel.grid(row=0, column=1, sticky="nsew")

        self._create_transcript_panel()
        self._create_notes_panel()

    def _create_recording_controls(self):
        """Creates recording control widgets."""
        # Header
        header_frame = ctk.CTkFrame(self.left_panel, fg_color="transparent")
        header_frame.pack(fill="x", padx=15, pady=(15, 10))

        title_label = ctk.CTkLabel(
            header_frame,
            text="🎙 Ses Kaydı",
            font=ctk.CTkFont(size=20, weight="bold"),
        )
        title_label.pack(side="left")

        # Device selection
        device_frame = ctk.CTkFrame(self.left_panel)
        device_frame.pack(fill="x", padx=15, pady=5)

        # Microphone
        mic_label = ctk.CTkLabel(
            device_frame,
            text="Mikrofon",
            font=ctk.CTkFont(size=12, weight="bold"),
        )
        mic_label.pack(anchor="w", padx=10, pady=(10, 2))

        self.mic_var = ctk.StringVar(value="Seçiniz...")
        self.mic_devices = self.recorder.get_input_devices()
        mic_options = ["Kapalı"] + [name for _, name in self.mic_devices]

        self.mic_dropdown = ctk.CTkComboBox(
            device_frame,
            values=mic_options,
            variable=self.mic_var,
            width=280,
            height=32,
        )
        self.mic_dropdown.pack(padx=10, pady=(0, 8))
        if self.mic_devices:
            self.mic_var.set(self.mic_devices[0][1])

        # System Audio
        loopback_label = ctk.CTkLabel(
            device_frame,
            text="Sistem Sesi",
            font=ctk.CTkFont(size=12, weight="bold"),
        )
        loopback_label.pack(anchor="w", padx=10, pady=(5, 2))

        self.loopback_var = ctk.StringVar(value="Kapalı")
        self.loopback_devices = self.recorder.get_loopback_devices()
        loopback_options = ["Kapalı"] + [name for _, name in self.loopback_devices]

        self.loopback_dropdown = ctk.CTkComboBox(
            device_frame,
            values=loopback_options,
            variable=self.loopback_var,
            width=280,
            height=32,
        )
        self.loopback_dropdown.pack(padx=10, pady=(0, 10))
        if self.loopback_devices:
            self.loopback_var.set(self.loopback_devices[0][1])

        # Timer display
        timer_frame = ctk.CTkFrame(self.left_panel, fg_color="transparent")
        timer_frame.pack(fill="x", padx=15, pady=10)

        self.timer_label = ctk.CTkLabel(
            timer_frame,
            text="00:00:00",
            font=ctk.CTkFont(size=36, weight="bold"),
        )
        self.timer_label.pack()

        # Block progress
        progress_frame = ctk.CTkFrame(self.left_panel, fg_color="transparent")
        progress_frame.pack(fill="x", padx=15)

        self.block_progress_label = ctk.CTkLabel(
            progress_frame,
            text="Blok: 00:00 / 10:00",
            font=ctk.CTkFont(size=11),
            text_color="gray60",
        )
        self.block_progress_label.pack()

        self.block_progress = ctk.CTkProgressBar(progress_frame, height=6)
        self.block_progress.pack(fill="x", pady=(5, 0))
        self.block_progress.set(0)

        # Record buttons
        button_frame = ctk.CTkFrame(self.left_panel, fg_color="transparent")
        button_frame.pack(fill="x", padx=15, pady=15)

        self.record_button = ctk.CTkButton(
            button_frame,
            text="⏺  Kayda Başla",
            command=self._toggle_recording,
            height=45,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#c0392b",
            hover_color="#e74c3c",
        )
        self.record_button.pack(side="left", fill="x", expand=True, padx=(0, 5))

        self.stop_button = ctk.CTkButton(
            button_frame,
            text="⏹",
            command=self._stop_recording,
            width=50,
            height=45,
            font=ctk.CTkFont(size=14),
            state="disabled",
        )
        self.stop_button.pack(side="right")

    def _create_blocks_panel(self):
        """Creates the blocks list panel."""
        # Separator
        separator = ctk.CTkFrame(self.left_panel, height=2, fg_color="gray30")
        separator.pack(fill="x", padx=15, pady=(5, 15))

        # Header with count and actions
        header_frame = ctk.CTkFrame(self.left_panel, fg_color="transparent")
        header_frame.pack(fill="x", padx=15)

        blocks_label = ctk.CTkLabel(
            header_frame,
            text="📁 Kayıt Blokları",
            font=ctk.CTkFont(size=14, weight="bold"),
        )
        blocks_label.pack(side="left")

        self.blocks_count_label = ctk.CTkLabel(
            header_frame,
            text="(0)",
            font=ctk.CTkFont(size=12),
            text_color="gray60",
        )
        self.blocks_count_label.pack(side="left", padx=5)

        # Select all / none buttons
        actions_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        actions_frame.pack(side="right")

        self.select_all_button = ctk.CTkButton(
            actions_frame,
            text="Tümü",
            width=50,
            height=24,
            font=ctk.CTkFont(size=11),
            fg_color="gray30",
            hover_color="gray40",
            command=self._select_all_blocks,
        )
        self.select_all_button.pack(side="left", padx=2)

        self.select_none_button = ctk.CTkButton(
            actions_frame,
            text="Hiçbiri",
            width=50,
            height=24,
            font=ctk.CTkFont(size=11),
            fg_color="gray30",
            hover_color="gray40",
            command=self._select_no_blocks,
        )
        self.select_none_button.pack(side="left", padx=2)

        # Scrollable blocks list
        self.blocks_scroll = ctk.CTkScrollableFrame(
            self.left_panel,
            fg_color="transparent",
        )
        self.blocks_scroll.pack(fill="both", expand=True, padx=10, pady=(10, 5))

        # Empty state label
        self.empty_label = ctk.CTkLabel(
            self.blocks_scroll,
            text="Henüz kayıt yok.\nKayda başlayın veya\nmevcut dosyaları yükleyin.",
            font=ctk.CTkFont(size=12),
            text_color="gray50",
            justify="center",
        )
        self.empty_label.pack(pady=30)

        # Bottom actions
        bottom_frame = ctk.CTkFrame(self.left_panel, fg_color="transparent")
        bottom_frame.pack(fill="x", padx=15, pady=10)

        self.selected_count_label = ctk.CTkLabel(
            bottom_frame,
            text="0 blok seçili",
            font=ctk.CTkFont(size=11),
            text_color="gray60",
        )
        self.selected_count_label.pack(side="left")

        self.transcribe_button = ctk.CTkButton(
            bottom_frame,
            text="Seçilenleri Çevir →",
            command=self._transcribe_selected,
            height=36,
            font=ctk.CTkFont(size=13, weight="bold"),
        )
        self.transcribe_button.pack(side="right")

    def _create_transcript_panel(self):
        """Creates the transcript display panel."""
        transcript_frame = ctk.CTkFrame(self.right_panel)
        transcript_frame.pack(fill="both", expand=True, padx=5, pady=5)

        # Header
        header = ctk.CTkFrame(transcript_frame, fg_color="transparent")
        header.pack(fill="x", padx=10, pady=(10, 5))

        ctk.CTkLabel(
            header,
            text="📝 Transkript",
            font=ctk.CTkFont(size=14, weight="bold"),
        ).pack(side="left")

        self.clear_transcript_button = ctk.CTkButton(
            header,
            text="Temizle",
            width=70,
            height=28,
            fg_color="gray30",
            hover_color="gray40",
            command=self._clear_transcript,
        )
        self.clear_transcript_button.pack(side="right")

        # Text area
        self.transcript_text = ctk.CTkTextbox(
            transcript_frame,
            font=ctk.CTkFont(size=12),
        )
        self.transcript_text.pack(fill="both", expand=True, padx=10, pady=5)

        # Action button
        action_frame = ctk.CTkFrame(transcript_frame, fg_color="transparent")
        action_frame.pack(fill="x", padx=10, pady=(5, 10))

        self.generate_notes_button = ctk.CTkButton(
            action_frame,
            text="🤖 Gemini ile Not Çıkar",
            command=self._generate_notes,
            height=38,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#8e44ad",
            hover_color="#9b59b6",
        )
        self.generate_notes_button.pack(side="left")

    def _create_notes_panel(self):
        """Creates the notes display panel."""
        notes_frame = ctk.CTkFrame(self.right_panel)
        notes_frame.pack(fill="both", expand=True, padx=5, pady=5)

        # Header
        header = ctk.CTkFrame(notes_frame, fg_color="transparent")
        header.pack(fill="x", padx=10, pady=(10, 5))

        ctk.CTkLabel(
            header,
            text="📋 Notlar",
            font=ctk.CTkFont(size=14, weight="bold"),
        ).pack(side="left")

        self.clear_notes_button = ctk.CTkButton(
            header,
            text="Temizle",
            width=70,
            height=28,
            fg_color="gray30",
            hover_color="gray40",
            command=self._clear_notes,
        )
        self.clear_notes_button.pack(side="right")

        # Text area
        self.notes_text = ctk.CTkTextbox(
            notes_frame,
            font=ctk.CTkFont(size=12),
        )
        self.notes_text.pack(fill="both", expand=True, padx=10, pady=5)

        # Action buttons
        action_frame = ctk.CTkFrame(notes_frame, fg_color="transparent")
        action_frame.pack(fill="x", padx=10, pady=(5, 10))

        self.export_button = ctk.CTkButton(
            action_frame,
            text="💾 Markdown Olarak Kaydet",
            command=self._export_notes,
            height=38,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#27ae60",
            hover_color="#2ecc71",
        )
        self.export_button.pack(side="left")

        # Status bar
        self.status_label = ctk.CTkLabel(
            action_frame,
            text="Hazır",
            font=ctk.CTkFont(size=11),
            text_color="gray60",
        )
        self.status_label.pack(side="right", padx=10)

    def _toggle_recording(self):
        """Starts or stops recording."""
        if not self.is_recording:
            self._start_recording()

    def _start_recording(self):
        """Starts audio recording."""
        mic_device_id = None
        loopback_device_id = None

        mic_name = self.mic_var.get()
        if mic_name != "Kapalı" and mic_name != "Seçiniz...":
            for dev_id, name in self.mic_devices:
                if name == mic_name:
                    mic_device_id = dev_id
                    break

        loopback_name = self.loopback_var.get()
        if loopback_name != "Kapalı" and loopback_name != "Seçiniz...":
            for dev_id, name in self.loopback_devices:
                if name == loopback_name:
                    loopback_device_id = dev_id
                    break

        if mic_device_id is None and loopback_device_id is None:
            messagebox.showwarning("Uyarı", "En az bir ses kaynağı seçmelisiniz!")
            return

        try:
            self.recorder.start_recording(mic_device_id, loopback_device_id)
            self.is_recording = True

            self.record_button.configure(
                text="⏺  Kaydediliyor...",
                fg_color="#e74c3c",
                state="disabled"
            )
            self.stop_button.configure(state="normal")
            self.mic_dropdown.configure(state="disabled")
            self.loopback_dropdown.configure(state="disabled")

            self._set_status("Kayıt başladı...")
        except Exception as e:
            messagebox.showerror("Hata", f"Kayıt başlatılamadı: {e}")

    def _stop_recording(self):
        """Stops audio recording."""
        if not self.is_recording:
            return

        blocks = self.recorder.stop_recording()
        self.is_recording = False

        self.record_button.configure(
            text="⏺  Kayda Başla",
            fg_color="#c0392b",
            state="normal"
        )
        self.stop_button.configure(state="disabled")
        self.mic_dropdown.configure(state="normal")
        self.loopback_dropdown.configure(state="normal")

        self.timer_label.configure(text="00:00:00")
        self.block_progress.set(0)
        self.block_progress_label.configure(text="Blok: 00:00 / 10:00")

        self._set_status(f"Kayıt durduruldu. {len(blocks)} blok kaydedildi.")

    def _on_block_created(self, filepath: str):
        """Callback when a new block is created during recording."""
        self.after(0, lambda: self._add_block_card(filepath))

    def _add_block_card(self, filepath: str):
        """Adds a block card to the list."""
        if filepath in self.block_cards:
            return

        # Hide empty label
        self.empty_label.pack_forget()

        # Create card
        card = BlockCard(
            self.blocks_scroll,
            filepath,
            on_selection_change=self._update_selection_count,
            on_delete=self._delete_block,
        )
        card.pack(fill="x", pady=4)

        self.block_cards[filepath] = card
        self._update_blocks_count()
        self._update_selection_count()

    def _delete_block(self, filepath: str):
        """Deletes a block."""
        if filepath in self.block_cards:
            confirm = messagebox.askyesno(
                "Blok Sil",
                f"Bu bloğu silmek istediğinize emin misiniz?\n{os.path.basename(filepath)}"
            )
            if confirm:
                self.block_cards[filepath].destroy()
                del self.block_cards[filepath]

                # Delete file
                try:
                    os.remove(filepath)
                except:
                    pass

                self._update_blocks_count()
                self._update_selection_count()

                # Show empty label if no blocks
                if not self.block_cards:
                    self.empty_label.pack(pady=30)

    def _load_existing_blocks(self):
        """Loads existing blocks from recordings directory."""
        if not os.path.exists(RECORDINGS_DIR):
            return

        for filename in sorted(os.listdir(RECORDINGS_DIR)):
            if filename.endswith(".wav"):
                filepath = os.path.join(RECORDINGS_DIR, filename)
                self._add_block_card(filepath)

    def _select_all_blocks(self):
        """Selects all blocks."""
        for card in self.block_cards.values():
            card.set_selected(True)
        self._update_selection_count()

    def _select_no_blocks(self):
        """Deselects all blocks."""
        for card in self.block_cards.values():
            card.set_selected(False)
        self._update_selection_count()

    def _update_blocks_count(self):
        """Updates the blocks count label."""
        count = len(self.block_cards)
        self.blocks_count_label.configure(text=f"({count})")

    def _update_selection_count(self):
        """Updates the selection count label."""
        selected = sum(1 for card in self.block_cards.values() if card.is_selected)
        self.selected_count_label.configure(text=f"{selected} blok seçili")

    def _get_selected_blocks(self) -> List[str]:
        """Returns list of selected block filepaths."""
        return [
            filepath
            for filepath, card in self.block_cards.items()
            if card.is_selected
        ]

    def _transcribe_selected(self):
        """Transcribes selected blocks."""
        selected = self._get_selected_blocks()

        if not selected:
            messagebox.showwarning("Uyarı", "Lütfen en az bir blok seçin!")
            return

        # Initialize Gladia service
        if self.gladia_service is None:
            try:
                self.gladia_service = GladiaService()
            except ValueError as e:
                messagebox.showerror("Hata", str(e))
                return

        self.transcribe_button.configure(state="disabled")
        self._set_status("Transkripsiyon başlıyor...")

        thread = threading.Thread(
            target=self._transcribe_worker,
            args=(selected,),
            daemon=True,
        )
        thread.start()

    def _transcribe_worker(self, filepaths: List[str]):
        """Background worker for transcription."""
        all_text = []

        for i, filepath in enumerate(filepaths):
            try:
                # Update card status
                self.after(0, lambda p=filepath: self.block_cards.get(p, None) and
                          self.block_cards[p].set_status("Çevriliyor..."))
                self.after(0, lambda p=filepath: self._set_status(
                    f"Çevriliyor ({i+1}/{len(filepaths)}): {os.path.basename(p)}"
                ))

                result = self.gladia_service.transcribe_file(
                    filepath,
                    on_progress=lambda msg: self.after(0, lambda m=msg: self._set_status(m)),
                )

                formatted = format_transcript(result, include_timestamps=True)
                self.transcripts[filepath] = formatted
                all_text.append(f"--- {os.path.basename(filepath)} ---\n{formatted}")

                # Update card status
                self.after(0, lambda p=filepath: self.block_cards.get(p, None) and
                          self.block_cards[p].set_status("✓ Tamamlandı"))

            except Exception as e:
                self.after(0, lambda p=filepath: self.block_cards.get(p, None) and
                          self.block_cards[p].set_status("✗ Hata"))
                self.after(0, lambda e=e: messagebox.showerror(
                    "Hata", f"Transkripsiyon hatası: {e}"
                ))

        final_text = "\n\n".join(all_text)
        self.after(0, lambda: self._update_transcript(final_text))
        self.after(0, lambda: self.transcribe_button.configure(state="normal"))
        self.after(0, lambda: self._set_status("Transkripsiyon tamamlandı."))

    def _update_transcript(self, text: str):
        """Updates the transcript text area."""
        self.transcript_text.delete("1.0", "end")
        self.transcript_text.insert("1.0", text)

    def _generate_notes(self):
        """Generates notes from transcript using Gemini."""
        transcript = self.transcript_text.get("1.0", "end").strip()

        if not transcript:
            messagebox.showwarning("Uyarı", "Önce bir transkript oluşturun!")
            return

        if self.gemini_service is None:
            try:
                self.gemini_service = GeminiService()
            except ValueError as e:
                messagebox.showerror("Hata", str(e))
                return

        self.generate_notes_button.configure(state="disabled")
        self._set_status("Notlar oluşturuluyor...")

        thread = threading.Thread(
            target=self._generate_notes_worker,
            args=(transcript,),
            daemon=True,
        )
        thread.start()

    def _generate_notes_worker(self, transcript: str):
        """Background worker for note generation."""
        try:
            notes = self.gemini_service.generate_notes(transcript)
            self.current_notes = notes

            self.after(0, lambda: self._update_notes(notes))
            self.after(0, lambda: self._set_status("Notlar oluşturuldu."))

        except Exception as e:
            self.after(0, lambda: messagebox.showerror(
                "Hata", f"Not oluşturma hatası: {e}"
            ))

        finally:
            self.after(0, lambda: self.generate_notes_button.configure(state="normal"))

    def _update_notes(self, notes: str):
        """Updates the notes text area."""
        self.notes_text.delete("1.0", "end")
        self.notes_text.insert("1.0", notes)

    def _export_notes(self):
        """Exports notes to a markdown file."""
        notes = self.notes_text.get("1.0", "end").strip()

        if not notes:
            messagebox.showwarning("Uyarı", "Kaydedilecek not bulunmuyor!")
            return

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        default_name = f"notes_{timestamp}.md"

        filepath = filedialog.asksaveasfilename(
            defaultextension=".md",
            filetypes=[("Markdown files", "*.md"), ("All files", "*.*")],
            initialfile=default_name,
        )

        if filepath:
            try:
                save_notes_to_markdown(notes, filepath)
                self._set_status(f"Notlar kaydedildi: {os.path.basename(filepath)}")
                messagebox.showinfo("Başarılı", f"Notlar kaydedildi:\n{filepath}")
            except Exception as e:
                messagebox.showerror("Hata", f"Kaydetme hatası: {e}")

    def _clear_transcript(self):
        """Clears the transcript text area."""
        self.transcript_text.delete("1.0", "end")
        self.transcripts.clear()

    def _clear_notes(self):
        """Clears the notes text area."""
        self.notes_text.delete("1.0", "end")
        self.current_notes = ""

    def _set_status(self, message: str):
        """Updates the status bar."""
        self.status_label.configure(text=message)

    def _update_timer(self):
        """Updates the recording timer display."""
        if self.is_recording:
            total_seconds = int(self.recorder.get_recording_duration())
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            seconds = total_seconds % 60
            self.timer_label.configure(text=f"{hours:02d}:{minutes:02d}:{seconds:02d}")

            block_seconds = int(self.recorder.get_current_block_duration())
            block_minutes = block_seconds // 60
            block_secs = block_seconds % 60
            self.block_progress_label.configure(
                text=f"Blok: {block_minutes:02d}:{block_secs:02d} / 10:00"
            )
            self.block_progress.set(block_seconds / 600)

        self.after(1000, self._update_timer)


def main():
    """Application entry point."""
    app = AudioTranscriberApp()
    app.mainloop()


if __name__ == "__main__":
    main()
