from clint.textui import puts, colored, indent
from threading import Timer
from pick import pick
import threading, colorama, keyboard, random, queue, time, io

try: import msvcrt, win32console, win32con
except ImportError: windows = False
else: windows = True

colorama.init()

class Choice:
    def __init__(self, index: int, option: str):
        self.index = index
        self.option = option

def choose_from_list(title: str, options: list, indi: str = "*", minselcont: int = 1) -> Choice:
    option, index = pick(options, title, indi, min_selection_count=minselcont); index += 1
    return Choice(index, option)

class RepeatedTimer:
    def __init__(self, interval: float, function, *args, **kwargs):
        self._timer = None
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False

class win_buffer():
    def __init__(self):
        if not windows: OSError('Not Windows')
        self.buffer = [win32console.CreateConsoleScreenBuffer(DesiredAccess = win32con.GENERIC_READ | win32con.GENERIC_WRITE, ShareMode=0, SecurityAttributes=None, Flags=1), win32console.CreateConsoleScreenBuffer(DesiredAccess = win32con.GENERIC_READ | win32con.GENERIC_WRITE, ShareMode=0, SecurityAttributes=None, Flags=1)]
        self.writeto = self.buffer[0]

    def push(self):
        self.buffer[1] = self.buffer[0]
        self.buffer[0] = win32console.CreateConsoleScreenBuffer(DesiredAccess = win32con.GENERIC_READ | win32con.GENERIC_WRITE, ShareMode=0, SecurityAttributes=None, Flags=1)
        self.writeto = self.buffer[0]
        self.pushing = self.buffer[1]
        self.pushing.SetConsoleActiveScreenBuffer()

    def addto(self, text: str):
        self.buffer[0].WriteConsole(text)

class slowprint(io.StringIO):
    def __init__(self, delay: int = 0.1):
        self.queue = queue.Queue()
        #self.queue = []
        self.delay = delay
        self.doshit, self.stopdo = True, False
        
        self.timerctl = threading.Thread(target=self._do)
        self.timerctl.daemon = True
        self.timerctl.start()
    
    def write(self, text: str):
        self.queue.put(text)

    def _do(self):
        while self.doshit:
            if self.queue.qsize() > 0: 
                puts(self.queue.get(), newline=False)
                time.sleep(self.delay)
        else:
            if self.stopdo: return

    def _stop(self):
        if self.queue.qsize() == 0: 
            self.doshit = False
            self.stopdo = True
            self.stoptimer.stop()
    
    def getreadytostop(self):
        self.stoptimer = RepeatedTimer(0.1, function=self._stop)
        self.stoptimer.start()

def isdebug(args: list) -> bool: s = args.copy(); s.pop(0); return '-d' in args or '--debug' in s

def progress_bar(current: int, total: int, name: str = "Progress", bar_length: int = 50, juststring: bool = False):
    fraction = current / total
    arrow = int(fraction * bar_length - 1) * '-' + '>'
    padding = int(bar_length - len(arrow)) * ' '
    endst = f'{name}: [{arrow}{padding}] {int(fraction*100)}%'.removeprefix(': ' if name.__len__() == 0 else '')
    if juststring: return endst
    else: 
        ending = '\n' if current >= total else '\r'
        print(endst, end=ending)

def progress_bar2(start_time: float, current_time: float = time.time(), timetotal: int = 30, size: int = 1, ljust: int = 4):
    remains = timetotal - (current_time - start_time)
    progbarsize = timetotal * size
    timepassed = (round(remains * size) - progbarsize) * -1
    progbarstring = '█' * timepassed + '░' * int(progbarsize - timepassed) + ' ' + str(round(remains, 2)).ljust(ljust, '0') + 's'
    return progbarstring

def ask_bool(prompt: str) -> bool:
    try: return {"true": True, "yes": True, "y": True, "false": False, "no": False, "n": False}[input(prompt).lower()]
    except KeyError: print("invalid input")

def ask_int(prompt: str) -> int:
    while True:
        try: return int(input(prompt))
        except ValueError: print("not a number")

def printc(n: str, *d, f: bool = False, nc = False, firstclr: object = colored.blue, sepL: int = 0, sepC: str = ' ', Beg: str = colored.green('//|'), BegL: int = 4, end: str = '\n', returnstring: bool = False, stream: None = None) -> str | None:
    sep = sepC * sepL; w = ''.join(map(str, d))
    if not f: 
        if nc: outstr = (n + sep + w + end)
        else: outstr = (firstclr(n) + sep + w + end)
    else: 
        if nc: outstr = (w + sep + n + end)
        else: outstr = (firstclr(w) + sep + n + end)
    if returnstring: return outstr
    else: 
        with indent(BegL, quote=Beg): 
            if stream == None: puts(outstr, newline=False)
            else: puts(outstr, stream=stream, newline=False)

def formatdict(thing: dict | list , item_color: object = colored.white, key_color: object = colored.white) -> str:
    if type(thing) == dict:
        retirm = '{ '
        for k, v in thing.items(): retirm += f"{key_color(k)}: {item_color(v)}, "
        retirmo = retirm.removesuffix(', ') + ' }'
    elif type(thing) == list:
        retirm = '[ '
        for i in thing: retirm += f"{item_color(i)}, "
        retirmo = retirm.removesuffix(', ') + ' ]'
    else: raise ValueError(f"{type(thing)} is not a dict or list >> '{thing}'")
    return retirmo

def printd(n: str, d: str = '', f: bool = False, A: bool = False, sepL: int = 0, sepC: str = ' ', Beg: str = colored.red('>>|'), BegL: int = 4):
    if A: printc(n, d, f=f, sepL=sepL, sepC=sepC, Beg=Beg, BegL=BegL)

def wind_getonekey(f: bool = True) -> str:
    if not windows: return ''
    if f: return str(msvcrt.getch(), 'utf-8')
    else: return msvcrt.getch()

def clearsc(type: int = 1):
    if type == 1: print('\033[2J')
    elif type == 2: print('\n' * 25)

def clearinp(t: int = 25, e: bool = False):
    for i in range(t):
        keyboard.press_and_release("\b")
        if e: printc(f"on the {i + 1} backspace")

if __name__ == '__main__': exit()