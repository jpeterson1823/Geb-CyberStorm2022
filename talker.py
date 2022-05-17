from pynput.keyboard import Key, Listener, Controller
from time import sleep
from sys import stdin, stdout
from random import randint

sleep(5)

keyboard = Controller()

string = "I'm watching you"

for char in string:
    keyboard.press(char)
    sleep(randint(1,5)*0.05)
    keyboard.release(char)
    sleep(randint(1,5)*0.1)

    
I
