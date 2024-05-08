# NOTES:
# If keys seem to be "stuck", show open hand to camera to reset positions
# Windows doesn't seem to run shortcuts after task manager shortcut has been run

import cv2
import mediapipe as mp
import time
from pynput.keyboard import Key, Controller

keyboard = Controller()

cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

pTime = 0
cTime = 0

#Init states
show_desktop_triggered = False
screenshot_triggered = False
explorer_triggered = False
task_manager_triggered = False

#Detects touch between two fingers
def touch(tipx, tipy, endx, endy):
    return abs(tipx - endx) < 30 and abs(tipy - endy) < 30

#While loop for tracking hand
while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    locix = lociy = locmx = locmy = locrx = locry = locpx = locpy = loctx = locty = 1000

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                
                #Recording finger tip positions
                if id == 8:
                    locix, lociy = cx, cy
                elif id == 12:
                    locmx, locmy = cx, cy
                elif id == 16:
                    locrx, locry = cx, cy
                elif id == 20:
                    locpx, locpy = cx, cy
                elif id == 4:
                    loctx, locty = cx, cy

        # Show Desktop: Index and Thumb
        if touch(locix, lociy, loctx, locty):
            if not show_desktop_triggered:
                keyboard.press(Key.cmd)
                keyboard.press('d')
                show_desktop_triggered = True
        elif show_desktop_triggered:
            keyboard.release('d')
            keyboard.release(Key.cmd)
            show_desktop_triggered = False

        # Screenshot: Middle and Thumb
        if touch(locmx, locmy, loctx, locty):
            if not screenshot_triggered:
                keyboard.press(Key.cmd)
                keyboard.press(Key.print_screen)
                screenshot_triggered = True
        elif screenshot_triggered:
            keyboard.release(Key.print_screen)
            keyboard.release(Key.cmd)
            screenshot_triggered = False
        
        # Explorer: Ring and Thumb
        if touch(locrx, locry, loctx, locty):
            if not explorer_triggered:
                keyboard.press(Key.cmd)
                keyboard.press('e')
                explorer_triggered = True
        elif explorer_triggered:
            keyboard.release('e')
            keyboard.release(Key.cmd)
            explorer_triggered = False

        # Task Manager: Pinky and Thumb
        if touch(locpx, locpy, loctx, locty):
            if not task_manager_triggered:
                keyboard.press(Key.ctrl)
                keyboard.press(Key.shift)
                keyboard.press(Key.esc)
                task_manager_triggered = True
        elif task_manager_triggered:
            keyboard.release(Key.esc)
            keyboard.release(Key.shift)
            keyboard.release(Key.ctrl)
            task_manager_triggered = False

    cv2.waitKey(1)
