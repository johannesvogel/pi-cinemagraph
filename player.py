import os
import signal
import sys

from random import shuffle
from time import sleep
from omxplayer.player import OMXPlayer
from pathlib import Path


def play():
  print('Starting player...')

  cinemagraphs_path = os.path.join('cinemagraphs', 'processed')
  cinemagraphs = os.listdir(cinemagraphs_path)
  shuffle(cinemagraphs)

  global current_player
  current_player = None

  for i, cinemagraph in enumerate(cinemagraphs):
    path_str = os.path.join(cinemagraphs_path, cinemagraph)
    path = Path(path_str)
    dbus_name = 'org.mpris.MediaPlayer2.omxplayer{}'.format(i)

    print('Now playing "{}".'.format(path_str))

    previous_player = current_player
    current_player = OMXPlayer(path, args=['--loop', '--no-osd', '-b'], dbus_name=dbus_name)

    if previous_player is not None:
      previous_player.quit()

    for alpha_fade_in in range(0, 255):
      current_player.set_alpha(alpha_fade_in)
      sleep(0.01)
    
    sleep(600)

    for alpha_fade_out in reversed(range(0, 255)):
      current_player.set_alpha(alpha_fade_out)
      sleep(0.02)
  
  current_player.quit()


def exit_handler(sig, frame):
  print('\nQuitting...')
  if current_player is not None:
    try:
      current_player.quit()
    except Exception as e:
      print(e)
  sleep(1)
  sys.exit(0)

signal.signal(signal.SIGINT, exit_handler)
