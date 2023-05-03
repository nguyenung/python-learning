import os, time
from moviepy.video.io.VideoFileClip import VideoFileClip

"""
Run script here to get total video duration in all sub-folder
├── sub-folder-1
│   ├── video-1a.mp4
│   ├── text-file.txt
│   └── video-1b.mp4
├── sub-folder-2
│   ├── video-2a.mp4
│   ├── rar.zip
│   └── code.py

Result will be like

# sub-folder-1 :  02:38
# sub-folder-2 :  00:13
# ===== Total time run:  98 seconds

"""

def is_video(filename):
    """
    This function takes a filename and checks if the file extension
    matches one of the video file extensions (.mp4, .avi, .mov, .mkv).

    Args:
        filename (str): The name of the file to be checked.

    Returns:
        bool: True if the file is a video file, False otherwise.
    """
    VIDEO_EXTENSIONS = ['.mp4', '.avi', '.mov', '.mkv']
    file_ext = os.path.splitext(filename)[1]
    return file_ext.lower() in VIDEO_EXTENSIONS

def get_video_duration(filename):
    """
    Get video duration in seconds
    
    Args:
        filename (srt): Video path
    Returns:
        int: video duration in seconds
    """
    video = VideoFileClip(filename)
    duration = video.duration
    video.close()
    return int(duration)

def calculate_total_time(total_seconds, mode = 'full'):
    """
    This function takes in a number of total seconds and an optional mode parameter.
    It calculates the total time in hours, minutes, and seconds and returns it in the specified mode.
    
    If the mode is 'full', it returns the total time in hours, minutes, and seconds.
    If the mode is 'short', it rounds the minutes up to the nearest minute
    if the seconds are 30 or more and returns the total time in hours and minutes.
    
    The function returns the calculated time as a string in the format:
    "HH:MM:SS" for the full mode
    "HH:MM" for the short mode.
    """
    total_seconds = int(total_seconds)
    hours, remaining_seconds = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remaining_seconds, 60)
    if mode == 'full':
        if hours > 0:
            return f"{hours}:{minutes:02d}:{seconds:02d}"
        else:
            return f"{minutes:02d}:{seconds:02d}"
    else:
        if minutes == 0:
            minutes = 1
        else:
            if seconds >= 30:
                minutes += 1
        return f"{hours:02d}:{minutes:02d}"
    

start_time = time.time()
# Get list of directories and sort alphabetically
dir_list = os.listdir()
dir_list = sorted(dir_list)

# Initialize an empty list to store all video files
file_list = []

# Initialize an empty dictionary to store all videos
all_videos = {}

# Iterate through directories and subdirectories
for directory in dir_list:
    # If the item is a directory, get the list of files inside it
    if os.path.isdir(directory):
        files = os.listdir(directory)
        # Initialize an empty list to store video files in this directory
        tmp_list = []
        # Iterate through files in the directory
        for file in files:
            # If the file is a video, add it to the list of video files
            if os.path.isfile(os.path.join(directory, file)):
                if is_video(os.path.join(directory, file)):
                    video_file = os.path.join(directory, file)
                    file_list.append(video_file)
                    # Add video file to the list of videos in this directory
                    tmp_list.append({
                        'file': video_file,
                        'duration': get_video_duration(video_file)
                    })
        # Add the list of videos in this directory to the dictionary of all videos
        all_videos[directory] = tmp_list

# Iterate through all directories and print the total duration of videos in each directory
for dir in all_videos.keys():
    # Calculate the total duration of videos in this directory
    total_duration = 0
    for video in all_videos[dir]:
        total_duration += video['duration']
    
    # Format the total duration and print the result
    formatted_duration = calculate_total_time(total_duration, 'short')
    print(dir, ':', formatted_duration)

# Calculate and print total run time in seconds
end_time = time.time()
total_time_run = int(end_time - start_time)
print('===== Total time run: ', total_time_run, 'seconds')
