import os
import sys

from moviepy.editor import VideoFileClip, concatenate_videoclips

FINAL_CLIP_LENGTH = 90  # seconds

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
    clip_length = clip.duration
    loops = int(FINAL_CLIP_LENGTH / clip_length)

    looped_clip = clip.loop(n=loops)
    looped_clip.write_videofile(
      processed_path,
      audio=False,
      codec='mpeg4',
      bitrate='2500k',
    )

  print('Processed {} new cinemagraph(s).'.format(len(cinemagraphs)))
