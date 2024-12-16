# YouTube Downloader with yt-dlp

This project is a Python-based tool that uses `yt-dlp` and `ffmpeg` to download videos, audio, or playlists from YouTube. It supports cropping thumbnails to a square format for better compatibility with audio album covers and embeds them into the downloaded audio files.

---

## Features

- Download individual videos or audio from YouTube.
- Download entire playlists in audio or video format.
- Automatically crops thumbnails to a square format for album cover compatibility.
- Embeds cropped thumbnails into audio files (for single audio downloads only).
- Supports high-quality MP3 audio extraction (320 kbps).
- Simple CLI interface for ease of use.

---

## Requirements

Before running this project, ensure you have the following installed:

1. **Python 3.7 or later**
2. **yt-dlp**  
   Install via pip:  
   ```bash
   pip install yt-dlp
   ```
3. **FFmpeg**  
   Ensure FFmpeg is installed and added to your system's PATH.  
   - On Linux:  
     ```bash
     sudo apt install ffmpeg
     ```
   - On macOS:  
     ```bash
     brew install ffmpeg
     ```
   - On Windows:  
     Download from [FFmpeg.org](https://ffmpeg.org/) and follow installation instructions.

---

## Usage

### Running the Program
1. Clone or download the repository.
2. Open a terminal and navigate to the project directory.
3. Run the script using Python:
   ```bash
   python ytdownload.py
   ```

### Options
When prompted, provide the required inputs as described below:

#### 1. **Download Type**
- Choose between `audio`, `video`, or `playlist`.

#### 2. **For Single Audio**
- The script downloads the audio, crops the thumbnail to a square format, and embeds the cropped thumbnail into the MP3 file.

#### 3. **For Video**
- Downloads the video in the highest available quality.

#### 4. **For Playlist**
- You can choose to download either the audio or video for all items in the playlist.
- **Note:** Cropped thumbnails are currently **not supported** for playlist audio downloads.

---

## Known Issues

### Thumbnail Cropping in Playlists
Currently, the script does not crop thumbnails or embed cropped thumbnails into MP3 files for playlist audio downloads. Thumbnails for playlist audio are directly embedded without cropping. This issue will be addressed in future updates.

---

## Example Output

### Single Audio Download
1. Input:
   ```bash
   Enter the Video or Playlist URL: https://www.youtube.com/watch?v=example
   Choose download type - 'audio', 'video', or 'playlist': audio
   ```
2. Output:
   ```
   Download complete!
   Thumbnail cropped successfully: example.webp
   Thumbnail embedded successfully into: example.mp3
   ```

### Playlist Download
1. Input:
   ```bash
   Enter the Video or Playlist URL: https://www.youtube.com/playlist?list=example
   Choose download type - 'audio', 'video', or 'playlist': playlist
   Choose 'audio' or 'video': audio
   ```
2. Output:
   ```
   Downloading playlist: Example Playlist
   [INFO] Downloaded audio: song1.mp3
   [INFO] Downloaded audio: song2.mp3
   ```

---

## Contributing

Feel free to open issues or pull requests if you have improvements or bug fixes for this project.
