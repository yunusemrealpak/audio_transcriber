# 🎙️ Audio Transcriber

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

**[English](#)** | **[Türkçe](./README_TR.md)**

A professional audio recording and transcription application for Windows. Record microphone and system audio simultaneously, automatically split into 10-minute blocks, transcribe with Gladia AI, and generate smart notes with Gemini.

## ✨ Features

- 🎤 **Multi-Source Recording** - Record microphone and system audio simultaneously
- 📦 **Smart Block Management** - Automatic 10-minute blocks for cost optimization
- 🎮 **Playback Preview** - Listen to each block before transcribing
- ✅ **Flexible Selection** - Choose which blocks to transcribe
- 📝 **Gladia Transcription** - High-accuracy Turkish transcription
- 🤖 **Gemini AI Notes** - Automatic note generation and summarization
- 💾 **Markdown Export** - Save and share notes easily
- 🎨 **Modern UI** - Professional interface built with CustomTkinter
- 🗑️ **Block Management** - Delete unwanted blocks
- 📊 **Batch Operations** - Select all/none with one click
- ⏱️ **Progress Tracking** - Real-time recording and playback progress

## 📸 Screenshots

> *Coming soon - UI screenshots will be added*

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- Windows OS (for system audio recording)
- [Gladia API Key](https://app.gladia.io/)
- [Gemini API Key](https://aistudio.google.com/apikey)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/audio_transcriber.git
   cd audio_transcriber
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # Linux/Mac
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure API keys**

   Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

   Edit `.env` and add your API keys:
   ```env
   GLADIA_API_KEY=your-gladia-key-here
   GEMINI_API_KEY=your-gemini-key-here
   ```

5. **Run the application**
   ```bash
   python main.py
   ```

## 📖 Usage

### Basic Workflow

1. **Select Audio Sources**
   - Choose microphone from dropdown
   - Choose system audio (Stereo Mix/MOTIV Mix) if needed

2. **Record Audio**
   - Click ⏺️ "Start Recording" button
   - Recording automatically splits into 10-minute blocks
   - Click ⏹️ "Stop" when done

3. **Preview Blocks**
   - Click ▶️ on any block card to listen
   - Progress bar shows playback status
   - Click ⏸️ to pause

4. **Select Blocks**
   - Use checkboxes to select blocks for transcription
   - "All" button selects all blocks
   - "None" button deselects all

5. **Transcribe**
   - Click "Transcribe Selected →"
   - Watch progress for each block
   - View transcript in the right panel

6. **Generate Notes**
   - Click 🤖 "Generate Notes with Gemini"
   - AI analyzes transcript and creates structured notes
   - Notes appear in the bottom panel

7. **Export**
   - Click 💾 "Save as Markdown"
   - Choose location and filename
   - Share your notes!

### Enabling System Audio (Windows)

To record system audio, enable "Stereo Mix":

1. Right-click speaker icon → **Sound Settings**
2. Click **Sound Control Panel** → **Recording** tab
3. Right-click empty space → **Show Disabled Devices**
4. Right-click **Stereo Mix** → **Enable**
5. Set as default or select in the app

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GLADIA_API_KEY` | API key from Gladia.io | Yes |
| `GEMINI_API_KEY` | API key from Google AI Studio | Yes |

### Settings (config.py)

| Setting | Default | Description |
|---------|---------|-------------|
| `SAMPLE_RATE` | 44100 | Audio sample rate in Hz |
| `BLOCK_DURATION_MINUTES` | 10 | Recording block duration |
| `RECORDINGS_DIR` | "recordings" | Directory for audio files |
| `GEMINI_MODEL` | "gemini-2.5-flash" | Gemini model version |

## 💰 Cost Estimation

| Service | Unit Price | 10 min | 1 hour |
|---------|-----------|--------|--------|
| Gladia | ~$0.0002/sec | ~$0.12 | ~$0.70 |
| Gemini Flash | Free* | $0 | $0 |

*Gemini 2.5 Flash is free within daily limits.

## 📁 Project Structure

```
audio_transcriber/
├── src/                 # Source code
│   ├── __init__.py
│   ├── audio_recorder.py    # Audio recording module
│   ├── gladia_service.py    # Gladia API integration
│   ├── gemini_service.py    # Gemini AI integration
│   └── config.py            # Configuration
├── main.py              # Main application entry point
├── recordings/          # Audio files (auto-created)
├── requirements.txt     # Dependencies
├── .env.example         # Environment variables template
├── .gitignore           # Git ignore rules
├── LICENSE              # MIT License
├── README.md            # English documentation
└── README_TR.md         # Turkish documentation
```

## 🔧 Troubleshooting

### "Microphone not found" error
- Check default microphone in Windows Sound Settings
- Verify microphone permissions for the application

### "Loopback not found" error
- Enable "Stereo Mix" or "Stereo Karışımı" in Windows:
  - Sound Settings → Recording → Right-click → Show Disabled Devices
  - Enable Stereo Mix/Karışımı

### Gladia API errors
- Verify API key is correct
- Check internet connection
- Verify credit balance in Gladia dashboard

### Gemini API errors
- Verify API key is correct
- Check if daily limit exceeded
- Ensure model name is correct

## 🎯 Roadmap

- [ ] Real-time transcription
- [ ] Speaker diarization (identify different speakers)
- [ ] Multiple note templates
- [ ] Automatic language detection
- [ ] Audio quality indicator
- [ ] Keyboard shortcuts/hotkeys
- [ ] Multi-language support
- [ ] Export to PDF and DOCX
- [ ] Cloud storage integration
- [ ] Collaboration features

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Gladia](https://gladia.io/) - Transcription API
- [Google Gemini](https://ai.google.dev/) - AI note generation
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) - Modern UI framework
- [sounddevice](https://python-sounddevice.readthedocs.io/) - Audio I/O library
- [soundfile](https://github.com/bastibe/python-soundfile) - Audio file operations

## 📧 Contact

Yunus Emre Alpak - [@yunusemrealpak](https://github.com/yunusemrealpak)

Project Link: [https://github.com/yourusername/audio_transcriber](https://github.com/yourusername/audio_transcriber)

---

<div align="center">
Made with ❤️ by Yunus Emre Alpak
</div>
