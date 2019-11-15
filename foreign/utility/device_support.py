import pyaudio
import cv2

from desktopmagic.screengrab_win32 import getDisplayRects


def device_support(silent):
  device_obj = {}

  try:
    device_obj['monitors'] = len(getDisplayRects())
  except:
    device_obj['monitors'] = '???'

  if silent:
    device_obj['cams'] = '???'
  else:
    cams = [0, []]

    while True:
      cam = cv2.VideoCapture(cams[0])
      check, frame = cam.read()
      if not check:
        break
      cams[0] += 1
      cams[1].append(f'[{cam.get(3)},{cam.get(4)}]')
      
    device_obj['cams'] = '{} {}'.format(cams[0], ', '.join(cams[1]))

  try:
    p = pyaudio.PyAudio()
  except:
    device_obj['io-channels'] = '???'
  else:
    try:
      device_obj['io-channels'] = '{},'.format(p.get_default_input_device_info()['maxInputChannels'])
    except:
      device_obj['io-channels'] = 'None,'
    
    try:
      device_obj['io-channels'] += str(p.get_default_output_device_info()['maxOutputChannels'])
    except:
      device_obj['io-channels'] += 'None'
  
  return device_obj