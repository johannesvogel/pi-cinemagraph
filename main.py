print('Starting application...')

from process_cinemagraphs import process_cinemagraphs
from sys import platform

process_cinemagraphs()

if platform != "win32":
    from player import play
    play()

