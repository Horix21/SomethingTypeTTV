import curses
from curses import wrapper
import time
import requests

def request():
    
    return str(r)

def startGame(stdscr):
    stdscr.clear()
    stdscr.addstr("Welcome to SomethingType (The Terminal Version)!\nPress any key to continue!")
    stdscr.refresh()
    stdscr.getkey()

def displayText(stdscr, targetText, currentText, wpm=0):
    stdscr.addstr(targetText)
    stdscr.addstr(1, 0, f"WPM: {wpm}")

    for i, char in enumerate(currentText):
        correctChar = targetText[i]
        color = curses.color_pair(1)
        if char != correctChar:
            color = curses.color_pair(2)
        stdscr.addstr(0, i, char, color)

def test(stdscr):
    
    api_url = "http://localhost:3000/quotes"
    try:
        response = requests.get(api_url)
    except Exception as e:
        stdscr.addstr(4, 0, "Could not connect to server API. Likely caused by server not running. Press control + c to exit.", curses.color_pair(2))
        return

    targetText = str(response.json()['quote'])

    currentText = []
    wpm = 0
    startTime = time.time()
    stdscr.nodelay(True)

    while True:
        timeElapsed = max(time.time() - startTime, 1)
        wpm = round(len(currentText) / (timeElapsed / 60) / 5)

        stdscr.clear()
        
        displayText(stdscr, targetText, currentText, wpm)

        stdscr.refresh()

        if "".join(currentText) == targetText:
            stdscr.nodelay(False)
            break
        
        try:
            key = stdscr.getkey()
        except:
            continue

        if ord(key) == 27:
            break

        if key in ("KEY_BACKSPACE", '\b', "\x7f"):
            if len(currentText) > 0:
                currentText.pop()
        elif len(currentText) < len(targetText):
            currentText.append(key)

        

def main(stdscr):
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)

    
    startGame(stdscr)
    while True:
        test(stdscr)

        stdscr.addstr(2, 0, "You completed the text! Press any key to continue...")
        stdscr.addstr(3, 0, "Do you want to play again? (y/n)")
        key = stdscr.getkey()
        if (key == 'n' or key == 'N'):
            break;
    


wrapper(main)