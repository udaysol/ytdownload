import dwn_scr

url = input('Enter the Video or Playlist URL: ')
download_type = input("Choose download type - 'audio', 'video', or 'playlist'(Wide Album Covers): ").strip().lower()

if download_type == 'audio':
    dwn_scr.download_and_crop_thumbnail(url)
    dwn_scr.download_audio(url)
elif download_type == 'video':
    dwn_scr.download_video(url)
elif download_type == 'playlist':
    media_type = input("'Choose 'audio' or 'video': ").strip().lower()
    if media_type in ['audio', 'video']:
        dwn_scr.download_playlist(url, media_type)
    else:
        print("Invalid Media Type!")
else:
    print("Invalid Download Type!")