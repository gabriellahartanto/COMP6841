from pynput.keyboard import Key, Controller
import time

keyboard = Controller()

time.sleep(5)

# Change window
keyboard.press(Key.cmd)
keyboard.press(Key.tab)
keyboard.release(Key.cmd)
keyboard.release(Key.tab)

time.sleep(1)

# New window
keyboard.press(Key.cmd)
keyboard.press('t')
keyboard.release(Key.cmd)
keyboard.release('t')

# # Close window
# keyboard.press(Key.cmd)
# keyboard.press('w')
# keyboard.release(Key.cmd)
# keyboard.release('w')

# Press and release space
keyboard.press(Key.space)
keyboard.release(Key.space)

# Type a lower case A; this will work even if no key on the
# physical keyboard is labelled 'A'
keyboard.press('a')
keyboard.release('a')

# Type two upper case As
keyboard.press('A')
keyboard.release('A')
with keyboard.pressed(Key.shift):
    keyboard.press('a')
    keyboard.release('a')

# Type 'Hello World' using the shortcut type method
keyboard.type('Hello World')

keyboard.press(Key.enter)
keyboard.release(Key.enter)

keyboard.press(Key.cmd)
keyboard.press(Key.space)
keyboard.release(Key.cmd)
keyboard.release(Key.space)

time.sleep(1)

keyboard.type('Discord')
time.sleep(0.5)
keyboard.press(Key.enter)
keyboard.release(Key.enter)
time.sleep(0.5)

keyboard.type('HI WILL!!!!!')
keyboard.press(Key.enter)
keyboard.release(Key.enter)
