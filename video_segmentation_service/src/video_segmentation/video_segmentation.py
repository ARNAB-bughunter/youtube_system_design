import subprocess, os

VIDEO_FOLDER = 'video_output'
RESOLUTIONS = {
    "144": {"w": "256", "h": "144","bitrates":"400k"},
    "240": {"w": "426", "h": "240","bitrates":"600k"},
    "360": {"w": "640", "h": "360","bitrates":"800k"},
    "480": {"w": "854", "h": "480","bitrates":"1000k"},
    "1080": {"w": "1920", "h": "1080","bitrates":"2500k"}
}



def create_video_folder():
    """Create the upload folder if it doesn't exist."""
    if not os.path.exists(VIDEO_FOLDER):
        os.makedirs(VIDEO_FOLDER)


def create_master_file(output_dir):

    master_playlist = os.path.join(output_dir, "master.m3u8")
    with open(master_playlist, "w") as f:
        f.write("#EXTM3U\n")
        f.write("#EXT-X-VERSION:3\n")
        
        for res, details in RESOLUTIONS.items():
            width = details["w"]
            height = details["h"]
            bitrate = int(details["bitrates"].replace('k', '000'))  # Convert to bits
            f.write(f"# {res}p - {width}x{height}\n")
            f.write(f"#EXT-X-STREAM-INF:BANDWIDTH={bitrate},RESOLUTION={width}x{height}\n")
            f.write(f"{res}_video/index.m3u8\n")

    print("Master playlist created successfully.")

def video_segmentation(video_path, video_id):
    
    for key, resolution_data in RESOLUTIONS.items():
        print(resolution_data["w"],resolution_data["h"],resolution_data["bitrates"])

        try:
            m3u8_file_path =  os.path.join(VIDEO_FOLDER,video_id,f"{key}_video")
            os.makedirs(m3u8_file_path)
        except IOError as e:
            pass

        command = f'''ffmpeg -i {video_path} -vf "scale=w={resolution_data["w"]}:h={resolution_data["h"]}" -codec:v h264 -b:v {resolution_data["bitrates"]} -codec:a aac -hls_time 10 -hls_playlist_type vod -hls_segment_filename {m3u8_file_path}/segment%03d.ts -start_number 0 {m3u8_file_path}/index.m3u8'''
        print("start covertion")
        subprocess.run(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("covertion end")
        print(os.path.join(m3u8_file_path,"index.m3u8"))
    
    master_m3u8_file_path = os.path.join(VIDEO_FOLDER,video_id)
    create_master_file(master_m3u8_file_path)








