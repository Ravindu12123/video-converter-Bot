import os, subprocess, time
from .. import BOT_UN
from telethon import events
from LOCAL.localisation import SUPPORT_LINK, JPG, JPG2
from ethon.telefunc import fast_download, fast_upload
from ethon.pyfunc import bash, video_metadata
from ethon.pyutils import rename
from datetime import datetime as dt
from telethon.tl.types import DocumentAttributeVideo
from moviepy.editor import VideoFileClip
import shutil

#clean dir after all.---------------
def clean_dir(directory_path):
    # Check if the specified directory exists
    if not os.path.isdir(directory_path):
        print(f"Directory {directory_path} does not exist.")
        return

    # Iterate through all files and folders in the directory
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        
        try:
            # Check if it's a file or directory and delete accordingly
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)  # Remove file or symbolic link
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)  # Remove directory and all its contents
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")
            return jsonify({"error": f"Failed to delete files.","reson":f"{e}"}), 400

    print(f"Directory {directory_path} cleaned successfully.")

#optimising-------------------‐----------‐--
def optimize_video(input_path, output_path):
    with VideoFileClip(input_path) as video:
        video.write_videofile(output_path, bitrate="500k", preset="ultrafast", audio=True)


#accepting command--------------------------
async def voptimize(event, msg):
    Drone = event.client
    edit = await Drone.send_message(event.chat_id, "Trying to process!", reply_to=msg.id)
    if hasattr(msg.media, "document"):
        file = msg.media.document
    else:
        file = msg.media
    x = msg.file.name
    mime = msg.file.mime_type
    ftmp4=0
    if x:
        name = msg.file.name
        if 'mp4' in mime:
          ftmp4=1
    elif 'mp4' in mime:
        name = "media_" + dt.now().isoformat("_", "seconds") + ".mp4"
        ftmp4=1
    elif msg.video:
        ftmp4=1
        name = "media_" + dt.now().isoformat("_", "seconds") + ".mp4"
    elif 'x-matroska' in mime:
        name = "media_" + dt.now().isoformat("_", "seconds") + ".mkv" 
    elif 'webm' in mime:
        name = "media_" + dt.now().isoformat("_", "seconds") + ".webm"      
    else:
        return await edit.edit("**Sorry🥶,Cannot find or make name for that file!!**")
    if x:
        out = ((msg.file.name).split("."))[0] 
    else:
        out = dt.now().isoformat("_", "seconds")
    try:
        DT = time.time()
        await fast_download(name, file, Drone, edit, DT, "**DOWNLOADING:**")
    except Exception as e:
        print(e)
        return await edit.edit(f"An error occured while downloading!\n\nContact [SUPPORT]({SUPPORT_LINK})")
    if ftmp4==1:
      try:
        await edit.edit("**Converting...\n\nNote:\n  🔰because file was not a mp4 file!**")
        rename(name, f'{out}.mp4')
      except Exception as e:
        print(e)
        return await edit.edit(f"An error occured while converting!\n\nContact [SUPPORT]({SUPPORT_LINK})")
    
    
    try:
        UT = time.time()
        uploader = await fast_upload(f'{out}.mp4', f'{out}.mp4', UT, Drone, edit, '**UPLOADING:**')
        await Drone.send_file(event.chat_id, uploader, thumb=JPG, caption=f'**CONVERTED by** : @{BOT_UN}', force_document=True)
    except Exception as e:
        print(e)
        return await edit.edit(f"An error occured while uploading!\n\nContact [SUPPORT]({SUPPORT_LINK})")
    await edit.delete()                      
    os.remove(f'{out}.mp4')
