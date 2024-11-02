import os, subprocess, time
from .. import Drone,BOT_UN
from telethon import events, Button
from LOCAL.localisation import SUPPORT_LINK, JPG, JPG2
from ethon.telefunc import fast_download, fast_upload
from ethon.pyfunc import bash, video_metadata
from ethon.pyutils import rename
from datetime import datetime as dt
from telethon.tl.types import DocumentAttributeVideo
from moviepy.editor import VideoFileClip
import shutil
from proglog import ProgressBarLogger


pbt=[
    [Button.inline("Update progress",data="pro_up")]
]
#progress={}
progress='resting...'
inp="x"
mdir="videooptimize"
#remove dir if exist------‐---------
def rdir(directory_path):
    if os.path.exists(directory_path) and os.path.isdir(directory_path):
        try:
            shutil.rmtree(directory_path)
            print(f"Directory '{directory_path}' has been removed.")
        except Exception as e:
            print(f"Failed to remove directory '{directory_path}'. Reason: {e}")
    else:
        print(f"Directory '{directory_path}' does not exist.")


#create thumb--------------------‐
def generate_thumbnail(video_path, thumb_path="thumb.jpg"):
    with VideoFileClip(video_path) as video:
        # Capture frame at the first second
        frame = video.get_frame(1.0)
        # Convert to Image and save as thumbnail
        img = Image.fromarray(frame)
        img.thumbnail((320, 180))  # Resize thumbnail to 320x180
        img.save(thumb_path, "JPEG")
    return thumb_path


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


def optimize_video(input_path, output_path,edit):
    progress='optimizing: 0%'
    class MyBarLogger(ProgressBarLogger):
        
      def callback(self, **changes):
        for (parameter, value) in changes.items():
            progress["st"]='Parameter %s is now %s' % (parameter, value)
            
      def bars_callback(self, bar, attr, value,old_value=None):
        percentage = (value / self.bars[bar]['total']) * 100
        npr=f"Optimizing: {percentage:.2f}%"
        if float(percentage) % 1 == 0:
          progress["pres"]=npr
    logger = MyBarLogger()
    try:
        with VideoFileClip(input_path) as video:
            video.write_videofile(
                output_path,
                bitrate="500k",
                preset="ultrafast",
                audio=True,
                logger=logger  # Pass the progress callback
            )
        progress = "Optimized"
    except Exception as e:
        progress = f"Error: {str(e)}"
        print(f"Error optimizing : {e}")
    finally:
        print("Optimization complete!")

@Drone.on(events.callbackquery.CallbackQuery(data="pro_up"))
async def _showprog(event):
    np=progress
    if inp !="x":
        np=f"{inp} \n{progress}"
    event.reply(np);


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
    outn=os.path.join(mdir,f"{out}.mp4")
    name=os.path.join(mdir,name)
    try:
        DT = time.time()
        await fast_download(name, file, Drone, edit, DT, "**DOWNLOADING:**")
    except Exception as e:
        #rdir(mdir)
        print(e)
        return await edit.edit(f"An error occured while downloading!\n\nContact [SUPPORT]({SUPPORT_LINK})")
    if ftmp4 == 0:
      try:
        await edit.edit("**Converting...\n\nNote:\n  🔰because file was not a mp4 file!**")
        rename(name, outn)
      except Exception as e:
        print(e)
        #rdir(mdir)
        return await edit.edit(f"An error occured while converting!\n\n{e}")
    else:
      await edit.edit("**file type:mp4**")
    ls=os.path.join(mdir,f"optimized_{out}.mp4")
    try:
        await edit.edit("**OPTIMIZING**")
        if ftmp4 == 0:
            name=outn
        input_path=name
        output_path=ls
        #await optimize_video(outn,ls,edit)
        # else:
        # await optimize_video(name,ls,edit)
        class MyBarLogger(ProgressBarLogger):
          def callback(self, **changes):
             for (parameter, value) in changes.items():
                inp=f"value"
              
          def bars_callback(self, bar, attr, value,old_value=None):
             percentage = (value / self.bars[bar]['total']) * 100
             npr=f"Optimizing: {percentage:.2f}%"
             if float(percentage) % 1 == 0:
                progress=npr
        logger = MyBarLogger()
        with VideoFileClip(input_path) as video:
          video.write_videofile(
            output_path,
            bitrate="500k",
            preset="ultrafast",
            audio=True,
            logger=logger
          )
        print("Optimization complete!")
    except Exception as e:
        #rdir(mdir)
        print(e)
        return await edit.edit(f"An Erro while optimizing! er:{e}")
 
    #uploading--------------------‐
    UT = time.time()
    metadata = video_metadata(ls)
    width = metadata["width"]
    height = metadata["height"]
    duration = metadata["duration"]
    attributes = [DocumentAttributeVideo(duration=duration, w=width, h=height, supports_streaming=True)]
    try:
        jpg = await generate_thumbnail(ls,os.path.join(mdir,"thumb.jpg"))
        uploader = await fast_upload(f'{ls}', f'{ls}', UT, Drone, edit, '**UPLOADING:**')
        await Drone.send_file(event.chat_id, uploader, caption=text, thumb=jpg, attributes=attributes, force_document=False)
    except Exception:
        try:
            uploader = await fast_upload(f'{ls}', f'{ls}', UT, Drone, edit, '**UPLOADING:**')
            await Drone.send_file(event.chat_id, uploader, caption=text, thumb=JPG, force_document=True)
        except Exception as e:
            #rdir(mdir)
            print(e)
            return await edit.edit(f"An error occured while uploading.\n\n{e}", link_preview=False)
    await edit.delete()
    await clean_dir(mdir)
    
