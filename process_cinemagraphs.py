import os
import sys

from time import sleep
from moviepy.editor import VideoFileClip, vfx
from decimal import Decimal

TARGET_CLIP_LENGTH = 90  # seconds
TARGET_WIDTH = 1024
TARGET_HEIGHT = 600

def process_cinemagraphs():
  cinemagraphs = []
  print('Looking for new cinemagraphs...')

  for f in os.listdir('cinemagraphs'):
    path_to_file = os.path.join('cinemagraphs', f)
    path_to_processed_file = os.path.join('cinemagraphs', 'processed', f)
    if os.path.isfile(path_to_file) and not os.path.isfile(path_to_processed_file):
      cinemagraphs.append(path_to_file)

  if len(cinemagraphs) < 1:
    print('No new cinemagraphs.')
    return

  print('Found {} new cinemagraph(s).'.format(len(cinemagraphs)))

  for i, cinemagraph in enumerate(cinemagraphs):
    filename = os.path.basename(cinemagraph)
    processed_path = os.path.join('cinemagraphs', 'processed', filename)

    print('({}/{}) Processing "{}".'.format(i+1, len(cinemagraphs), filename))

    clip = VideoFileClip(cinemagraph)
    resolution = clip.size
    clip.reader.close()
    if hasattr(clip, 'audio') and hasattr(clip.audio, 'reader'):
      clip.audio.reader.close_proc()
    del clip

    width = resolution[0]
    height = resolution[1]
    
    scale = max(TARGET_WIDTH/width, TARGET_HEIGHT/height)

    new_width = int(round(width*scale, 0))
    new_height = int(round(height*scale, 0))

    resized_clip = VideoFileClip(
      cinemagraph,
      target_resolution=(new_height, new_width),
      resize_algorithm='bilinear'
    )

    x_center = int(round(new_width/2, 0))
    y_center = int(round(new_height/2, 0))

    cropped_clip = vfx.crop(
      resized_clip, 
      x_center=x_center , 
      y_center=y_center, 
      width=TARGET_WIDTH, 
      height=TARGET_HEIGHT
    )

    clip_length = cropped_clip.duration
    loops = int(TARGET_CLIP_LENGTH / clip_length)

    looped_clip = cropped_clip.loop(n=loops)
    looped_clip.write_videofile(
      processed_path,
      audio=False,
      codec='mpeg4',
      bitrate='5000k',
    )

  print('Processed {} new cinemagraph(s).'.format(len(cinemagraphs)))

process_cinemagraphs()
