#  This file is part of the VIDEOconvertor distribution.
#  Copyright (c) 2021 Doctorstra ; All rights reserved. 
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, version 3.
#
#  This program is distributed in the hope that it will be useful, but
#  WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
#  General Public License for more details.
#
#  License can be found in < https://github.com/Doctorstra/VIDEO-converter/blob/public/LICENSE> .

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
from PIL import Image

def gen_thumb(video_path, thumb_path="thumb.jpg"):
    with VideoFileClip(video_path) as video:
        # Capture frame at the first second
        frame = video.get_frame(3.0)
        # Convert to Image and save as thumbnail
        img = Image.fromarray(frame)
        #img.thumbnail((320, 180))  # Resize thumbnail to 320x180
        img.save(thumb_path, "JPEG")
    return thumb_path

async def mp3(event, msg):
    Drone = event.client
    edit = await Drone.send_message(event.chat_id, "Trying to process!", reply_to=msg.id)
    if hasattr(msg.media, "document"):
        file = msg.media.document
    else:
        file = msg.media
    x = msg.file.name
    mime = msg.file.mime_type
    if x:
        name = msg.file.name
    elif 'mp4' in mime:
        name = "media_" + dt.now().isoformat("_", "seconds") + ".mp4"
    elif msg.video:
        name = "media_" + dt.now().isoformat("_", "seconds") + ".mp4"
    elif 'x-matroska' in mime:
        name = "media_" + dt.now().isoformat("_", "seconds") + ".mkv" 
    elif 'webm' in mime:
        name = "media_" + dt.now().isoformat("_", "seconds") + ".webm"      
    if x:
        out = ((msg.file.name).split("."))[0]
    else:
        out = dt.now().isoformat("_", "seconds")
    try:
        DT = time.time()
        await fast_download(name, file, Drone, edit, DT, "**DOWNLOADING:**")
    except Exception as e:
        os.rmdir("audioconvert")
        print(e)
        return await edit.edit(f"An error occured while downloading!\n\nContact [SUPPORT]({SUPPORT_LINK})")
    try:
        await edit.edit("Converting.")
        bash(f"ffmpeg -i {name} -codec:a libmp3lame -q:a 0 {out}.mp3")
    except Exception as e:
        os.rmdir("audioconvert")
        print(e)
        return await edit.edit(f"An error occured while converting!\n\nContact [SUPPORT]({SUPPORT_LINK})")
    try:
        UT = time.time()
        uploader = await fast_upload(f'{out}.mp3', f'{out}.mp3', UT, Drone, edit, '**UPLOADING:**')
        await Drone.send_file(event.chat_id, uploader, caption=f'**AUDIO EXTRACTED by** : @{BOT_UN}', force_document=True)
    except Exception as e:
        os.rmdir("audioconvert")
        print(e)
        return await edit.edit(f"An error occured while uploading!\n\nContact [SUPPORT]({SUPPORT_LINK})")
    await edit.delete()
    os.remove(name)
    os.remove(f'{out}.mp3')                           
                       
async def flac(event, msg):
    Drone = event.client
    edit = await Drone.send_message(event.chat_id, "Trying to process!", reply_to=msg.id)
    if hasattr(msg.media, "document"):
        file = msg.media.document
    else:
        file = msg.media
    x = msg.file.name
    mime = msg.file.mime_type
    if x:
        name = msg.file.name
    elif 'mp4' in mime:
        name = "media_" + dt.now().isoformat("_", "seconds") + ".mp4"
    elif msg.video:
        name = "media_" + dt.now().isoformat("_", "seconds") + ".mp4"
    elif 'x-matroska' in mime:
        name = "media_" + dt.now().isoformat("_", "seconds") + ".mkv" 
    elif 'webm' in mime:
        name = "media_" + dt.now().isoformat("_", "seconds") + ".webm"      
    if x:
        out = ((msg.file.name).split("."))[0]
    else:
        out = dt.now().isoformat("_", "seconds")
    try:
        DT = time.time()
        await fast_download(name, file, Drone, edit, DT, "**DOWNLOADING:**")
    except Exception as e:
        os.rmdir("audioconvert")
        print(e)
        return await edit.edit(f"An error occured while downloading!\n\nContact [SUPPORT]({SUPPORT_LINK})")
    try:
        await edit.edit("Converting.")
        bash(f"ffmpeg -i {name} -codec:a libmp3lame -q:a 0 {out}.mp3")
        bash(f'ffmpeg -i {out}.mp3 -c:a flac {out}.flac')
    except Exception as e:
        os.rmdir("audioconvert")
        print(e)
        return await edit.edit(f"An error occured while converting!\n\nContact [SUPPORT]({SUPPORT_LINK})")
    try:
        UT = time.time()
        uploader = await fast_upload(f'{out}.flac', f'{out}.flac', UT, Drone, edit, '**UPLOADING:**')
        await Drone.send_file(event.chat_id, uploader, caption=f'**AUDIO EXTRACTED by** : @{BOT_UN}', force_document=True)
    except Exception as e:
        os.rmdir("audioconvert")
        print(e)
        return await edit.edit(f"An error occured while uploading!\n\nContact [SUPPORT]({SUPPORT_LINK})")
    await edit.delete()
    os.remove(name)
    os.remove(f'{out}.mp3')                           
    os.remove(f'{out}.flac')                 

async def wav(event, msg):
    Drone = event.client
    edit = await Drone.send_message(event.chat_id, "Trying to process!", reply_to=msg.id)
    if hasattr(msg.media, "document"):
        file = msg.media.document
    else:
        file = msg.media
    x = msg.file.name
    mime = msg.file.mime_type
    if x:
        name = msg.file.name
    elif 'mp4' in mime:
        name = "media_" + dt.now().isoformat("_", "seconds") + ".mp4"
    elif msg.video:
        name = "media_" + dt.now().isoformat("_", "seconds") + ".mp4"
    elif 'x-matroska' in mime:
        name = "media_" + dt.now().isoformat("_", "seconds") + ".mkv" 
    elif 'webm' in mime:
        name = "media_" + dt.now().isoformat("_", "seconds") + ".webm"      
    if x:
        out = ((msg.file.name).split("."))[0]
    else:
        out = dt.now().isoformat("_", "seconds")
    try:
        DT = time.time()
        await fast_download(name, file, Drone, edit, DT, "**DOWNLOADING:**")
    except Exception as e:
        os.rmdir("audioconvert")
        print(e)
        return await edit.edit(f"An error occured while downloading!\n\nContact [SUPPORT]({SUPPORT_LINK})")
    try:
        await edit.edit("Converting.")
        bash(f"ffmpeg -i {name} -codec:a libmp3lame -q:a 0 {out}.mp3")
        bash(f'ffmpeg -i {out}.mp3 {out}.wav')
    except Exception as e:
        os.rmdir("audioconvert")
        print(e)
        return await edit.edit(f"An error occured while converting!\n\nContact [SUPPORT]({SUPPORT_LINK})")
    try:
        UT = time.time()
        uploader = await fast_upload(f'{out}.wav', f'{out}.wav', UT, Drone, edit, '**UPLOADING:**')
        await Drone.send_file(event.chat_id, uploader, caption=f'**AUDIO EXTRACTED by** : @{BOT_UN}', force_document=True)
    except Exception as e:
        os.rmdir("audioconvert")
        print(e)
        return await edit.edit(f"An error occured while uploading!\n\nContact [SUPPORT]({SUPPORT_LINK})")
    await edit.delete()
    os.remove(name)
    os.remove(f'{out}.mp3')                           
    os.remove(f'{out}.wav')                 
                                       
async def mp4(event, msg):
    Drone = event.client
    edit = await Drone.send_message(event.chat_id, "Trying to process!", reply_to=msg.id)
    if hasattr(msg.media, "document"):
        file = msg.media.document
    else:
        file = msg.media
    x = msg.file.name
    mime = msg.file.mime_type
    if x:
        name = msg.file.name
    elif 'mp4' in mime:
        name = "media_" + dt.now().isoformat("_", "seconds") + ".mp4"
    elif msg.video:
        name = "media_" + dt.now().isoformat("_", "seconds") + ".mp4"
    elif 'x-matroska' in mime:
        name = "media_" + dt.now().isoformat("_", "seconds") + ".mkv" 
    elif 'webm' in mime:
        name = "media_" + dt.now().isoformat("_", "seconds") + ".webm"      
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
    try:
        await edit.edit("Converting.")
        rename(name, f'{out}.mp4')
    except Exception as e:
        print(e)
        return await edit.edit(f"An error occured while converting!\n\nContact [SUPPORT]({SUPPORT_LINK})")
    try:
        thumb_path='thumb.jpg'
        with VideoFileClip(out) as video:
            frame = video.get_frame(3.0)
            img = Image.fromarray(frame)
            img.save(thumb_path, "JPEG")
        metadata = video_metadata(f'{out}.mp4')
        width = metadata["width"]
        height = metadata["height"]
        duration = metadata["duration"]
        attributes = [DocumentAttributeVideo(duration=duration, w=width, h=height, supports_streaming=True)]           
        UT = time.time()
        uploader = await fast_upload(f'{out}.mp4', f'{out}.mp4', UT, Drone, edit, '**UPLOADING:**')
        await Drone.send_file(event.chat_id, uploader, thumb=thumb_path, caption=f'**CONVERTED by** : @{BOT_UN}', attributes=attributes, force_document=False)
        if os.path.exists(thumb_path):
           os.remove(thumb_path)
    except Exception as e:
        print(e)
        return await edit.edit(f"An error occured while uploading!\n\nContact [SUPPORT]({SUPPORT_LINK})")
    await edit.delete()                      
    os.remove(f'{out}.mp4')                 
                                           
async def mkv(event, msg):
    Drone = event.client
    edit = await Drone.send_message(event.chat_id, "Trying to process!", reply_to=msg.id)
    if hasattr(msg.media, "document"):
        file = msg.media.document
    else:
        file = msg.media
    x = msg.file.name
    mime = msg.file.mime_type
    if x:
        name = msg.file.name
    elif 'mp4' in mime:
        name = "media_" + dt.now().isoformat("_", "seconds") + ".mp4"
    elif msg.video:
        name = "media_" + dt.now().isoformat("_", "seconds") + ".mp4"
    elif 'x-matroska' in mime:
        name = "media_" + dt.now().isoformat("_", "seconds") + ".mkv" 
    elif 'webm' in mime:
        name = "media_" + dt.now().isoformat("_", "seconds") + ".webm"      
    if x:
        out = ((msg.file.name).split("."))[0] + ".mkv"
    else:
        out = dt.now().isoformat("_", "seconds") + ".mkv"
    try:
        DT = time.time()
        await fast_download(name, file, Drone, edit, DT, "**DOWNLOADING:**")
    except Exception as e:
        print(e)
        return await edit.edit(f"An error occured while downloading!\n\nContact [SUPPORT]({SUPPORT_LINK})")
    try:
        await edit.edit("Converting.")
        rename(name, f'{out}')
    except Exception as e:
        print(e)
        return await edit.edit(f"An error occured while converting!\n\nContact [SUPPORT]({SUPPORT_LINK})")
    try:
        UT = time.time()
        uploader = await fast_upload(f'{out}', f'{out}', UT, Drone, edit, '**UPLOADING:**')
        await Drone.send_file(event.chat_id, uploader, caption=f'**CONVERTED by** : @{BOT_UN}', force_document=True)
    except Exception as e:
        print(e)
        return await edit.edit(f"An error occured while uploading!\n\nContact [SUPPORT]({SUPPORT_LINK})")
    await edit.delete()                        
    os.remove(f'{out}')
             
async def webm(event, msg):
    Drone = event.client
    edit = await Drone.send_message(event.chat_id, "Trying to process!", reply_to=msg.id)
    if hasattr(msg.media, "document"):
        file = msg.media.document
    else:
        file = msg.media
    x = msg.file.name
    mime = msg.file.mime_type
    if x:
        name = msg.file.name
    elif 'mp4' in mime:
        name = "media_" + dt.now().isoformat("_", "seconds") + ".mp4"
    elif msg.video:
        name = "media_" + dt.now().isoformat("_", "seconds") + ".mp4"
    elif 'x-matroska' in mime:
        name = "media_" + dt.now().isoformat("_", "seconds") + ".mkv" 
    elif 'webm' in mime:
        name = "media_" + dt.now().isoformat("_", "seconds") + ".webm"      
    if x:
        out = ((msg.file.name).split("."))[0] + ".webm"
    else:
        out = dt.now().isoformat("_", "seconds") + ".webm"
    try:
        DT = time.time()
        await fast_download(name, file, Drone, edit, DT, "**DOWNLOADING:**")
    except Exception as e:
        print(e)
        return await edit.edit(f"An error occured while downloading!\n\nContact [SUPPORT]({SUPPORT_LINK})")
    try:
        await edit.edit("Converting.")
        rename(name, f'{out}')
    except Exception as e:
        print(e)
        return await edit.edit(f"An error occured while converting!\n\nContact [SUPPORT]({SUPPORT_LINK})")
    try:
        UT = time.time()
        uploader = await fast_upload(f'{out}', f'{out}', UT, Drone, edit, '**UPLOADING:**')
        await Drone.send_file(event.chat_id, uploader, caption=f'**CONVERTED by** : @{BOT_UN}', force_document=True)
    except Exception as e:
        print(e)
        return await edit.edit(f"An error occured while uploading!\n\nContact [SUPPORT]({SUPPORT_LINK})")
    await edit.delete()                 
    os.remove(f'{out}')
             
async def file(event, msg):
    Drone = event.client
    edit = await Drone.send_message(event.chat_id, "Trying to process!", reply_to=msg.id)
    if hasattr(msg.media, "document"):
        file = msg.media.document
    else:
        file = msg.media
    x = msg.file.name
    mime = msg.file.mime_type
    if x:
        name = msg.file.name
    elif 'mp4' in mime:
        name = "media_" + dt.now().isoformat("_", "seconds") + ".mp4"
    elif msg.video:
        name = "media_" + dt.now().isoformat("_", "seconds") + ".mp4"
    elif 'x-matroska' in mime:
        name = "media_" + dt.now().isoformat("_", "seconds") + ".mkv" 
    elif 'webm' in mime:
        name = "media_" + dt.now().isoformat("_", "seconds") + ".webm"      
    try:
        DT = time.time()
        await fast_download(name, file, Drone, edit, DT, "**DOWNLOADING:**")
    except Exception as e:
        print(e)
        return await edit.edit(f"An error occured while downloading!\n\nContact [SUPPORT]({SUPPORT_LINK})")
    try:
        UT = time.time()
        uploader = await fast_upload(f'{name}', f'{name}', UT, Drone, edit, '**UPLOADING:**')
        await Drone.send_file(event.chat_id, uploader, caption=f'**CONVERTED by** : @{BOT_UN}', force_document=True)
    except Exception as e:
        print(e)
        return await edit.edit(f"An error occured while uploading!\n\nContact [SUPPORT]({SUPPORT_LINK})")
    await edit.delete()
    os.remove(name)                           
    
async def video(event, msg):
    Drone = event.client
    edit = await Drone.send_message(event.chat_id, "Trying to process!", reply_to=msg.id)
    if hasattr(msg.media, "document"):
        file = msg.media.document
    else:
        file = msg.media
    x = msg.file.name
    mime = msg.file.mime_type
    if x:
        name = msg.file.name
    elif 'mp4' in mime:
        name = "media_" + dt.now().isoformat("_", "seconds") + ".mp4"
    elif msg.video:
        name = "media_" + dt.now().isoformat("_", "seconds") + ".mp4"
    elif 'x-matroska' in mime:
        name = "media_" + dt.now().isoformat("_", "seconds") + ".mkv" 
    elif 'webm' in mime:
        name = "media_" + dt.now().isoformat("_", "seconds") + ".webm"      
    if x:
        out = ((msg.file.name).split("."))[0] + '.mp4'
    else:
        out = dt.now().isoformat("_", "seconds") + '.mp4'
    try:
        DT = time.time()
        await fast_download(name, file, Drone, edit, DT, "**DOWNLOADING:**")
    except Exception as e:
        print(e)
        return await edit.edit(f"An error occured while downloading!\n\nContact [SUPPORT]({SUPPORT_LINK})")
    try:
        await edit.edit("Converting.")
        rename(name, f'{out}')
    except Exception as e:
        print(e)
        return await edit.edit(f"An error occured while converting!\n\nContact [SUPPORT]({SUPPORT_LINK})")
    try:
        #jpg = await gen_thumb(out)
        thumb_path='thumb.jpg'
        with VideoFileClip(out) as video:
            frame = video.get_frame(3.0)
            img = Image.fromarray(frame)
            img.save(thumb_path, "JPEG")
        metadata = video_metadata(out)
        width = metadata["width"]
        height = metadata["height"]
        duration = metadata["duration"]
        attributes = [DocumentAttributeVideo(duration=duration, w=width, h=height, supports_streaming=True)]           
        UT = time.time()
        uploader = await fast_upload(f'{out}', f'{out}', UT, Drone, edit, '**UPLOADING:**')
        await Drone.send_file(event.chat_id, uploader,thumb=thumb_path, caption=f'**CONVERTED by** : @{BOT_UN}', attributes=attributes, force_document=False)
        if os.path.exists(thumb_path):
           os.remove(thumb_path)
    except Exception as e:
        print(e)
        return await edit.edit(f"An error occured while uploading!\n\n{e}")
    await edit.delete()
    os.remove(out)                           
    
