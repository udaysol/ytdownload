import yt_dlp
import sys
import os
import subprocess

def progress(d):
    if d['status'] == 'downloading':
        print(f"Downloading: {d['_percent_str']} at {d['_speed_str']} ETA: {d['_eta_str']}", end='\r')
        sys.stdout.flush() 
    elif d['status'] == 'finished':
        print("\nDownload complete!")  

def crop_to_square(input_file):
    output_file = f"cropped_{os.path.splitext(input_file)[0]}.webp"  # Ensure proper output extension
    converted_file = f"{os.path.splitext(input_file)[0]}.jpeg"

    try:
        # Step 1: Crop the thumbnail to a square
        print(f"Cropping thumbnail: {input_file}")
        subprocess.run([
            "ffmpeg", "-i", input_file,
            "-vf", "crop=min(iw\\,ih):min(iw\\,ih):((iw-min(iw\\,ih))/2):((ih-min(iw\\,ih))/2)",
            "-frames:v", "1",  # Ensure single frame output
            "-y", output_file
        ], check=True)
        print(f"Cropped thumbnail saved as: {output_file}")

        # Step 2: Convert cropped thumbnail to JPEG with explicit pixel format
        print(f"Converting thumbnail to JPEG: {converted_file}")
        subprocess.run([
            "ffmpeg", "-i", output_file,
            "-frames:v", "1",  # Handle single frame output
            "-pix_fmt", "yuvj420p",  # Specify pixel format for JPEG
            "-y", converted_file
        ], check=True)
        print(f"Converted thumbnail saved as: {converted_file}")

        # Step 3: Optionally replace the original cropped file with JPEG
        os.remove(output_file)
        # print(f"Replaced cropped file with JPEG: {output_file}")

    except subprocess.CalledProcessError as e:
        print(f"Error during FFmpeg processing: {e}")
    except FileNotFoundError:
        print("FFmpeg not found. Please install FFmpeg to use this feature.")

def embed_thumbnail(audio_file, thumbnail_path):
    """Reprocess the audio file to embed the cropped thumbnail."""
    try:
        print(f"Embedding cropped thumbnail into: {audio_file}")
        subprocess.run([
            "ffmpeg", "-i", audio_file, "-i", thumbnail_path,
            "-map", "0", "-map", "1", "-c", "copy",
            "-metadata:s:v", "title=Album cover", "-metadata:s:v", "comment=Cover (front)",
            "-y", f"final_{audio_file}"
        ], check=True)
        os.replace(f"final_{audio_file}", audio_file)
        print(f"Thumbnail embedded successfully into: {audio_file}")
        os.remove(thumbnail_path)
    except subprocess.CalledProcessError as e:
        print(f"Error embedding thumbnail: {e}")
    except FileNotFoundError:
        print("FFmpeg not found. Please install FFmpeg to use this feature.")


def download_and_crop_thumbnail(url):
    ydl_opts = {
        'skip_download': True,
        'writethumbnail': True,
        'outtmpl': '%(title)s.%(ext)s',
        'quiet': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url)
        thumbnail_file = f"{info['title']}.webp"
        print(f"Thumbnail saved as: {thumbnail_file}")

        if os.path.exists(thumbnail_file):
            crop_to_square(thumbnail_file)
        else:
            print("Thumbnail file not found!")


def download_audio(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': '%(title)s.%(ext)s',
        'postprocessors': [
            {'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '320'},
            {'key': 'FFmpegMetadata'},
        ],
        'prefer_ffmpeg': True,
        'progress_hooks': [progress],
        'quiet': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url)
            output_filename = ydl.prepare_filename(info)
            video_id = info.get("id")

            title = info.get('title')
            extension = "jpeg"  # yt-dlp saves thumbnails as .webp
            thumbnail_path = f"{title}.{extension}"

            # Embed the cropped thumbnail
            audio_file = os.path.splitext(output_filename)[0] + ".mp3"
            if os.path.exists(audio_file):
                embed_thumbnail(audio_file, thumbnail_path)
            else:
                print(f"Audio file not found: {audio_file}")
        except Exception as e:
            print(f"Error downloading audio: {e}")

def download_video(url):
    ydl_opts = {
    'format': 'bestvideo+bestaudio/best',
    'outtmpl': '%(title)s.%(ext)s',
    'progress_hooks': [progress],
    'quiet': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def download_playlist(url, media_type):
    if media_type == 'audio':
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': '%(title)s.%(ext)s',
            'postprocessors': [
                {'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '320'},
                {'key': 'EmbedThumbnail'}, 
                {'key': 'FFmpegMetadata'},
            ],
            'writethumbnail': True,
            'thumbnails':[{
                'prefernce': 1,
                'id': 'maxresdefault',
            }],
            'prefer_ffmpeg': True,
            'progress_hooks': [progress], 
            'quiet': True,  # Prevent extra output
            'noplaylist': False
        }
    
    else:
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': '%(title)s.%(ext)s',
            'progress_hooks': [progress],
            'quiet': True,
            'noplaylist': False
        }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)  # Get video info without downloading
        video_id = info.get("id")
        thumbnail_filename = f"{video_id}.webp"

        ydl.download([url])
