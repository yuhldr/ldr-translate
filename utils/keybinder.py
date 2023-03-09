from pynput import mouse, keyboard
from pynput.mouse import Button
from pynput.keyboard import Key, KeyCode
import queue
import threading
import re

__event_queue = queue.Queue()
__callback_list = []
__state = set()
keybinder_thread: threading.Thread = None
keyboard_listener: threading.Thread = None
mouse_listener: threading.Thread = None
close_event = threading.Event()


def on_click(x, y, button: mouse.Button, pressed: bool):
    if not close_event.is_set():
        __event_queue.put((button, pressed))


def on_press(key):
    if not close_event.is_set():
        __event_queue.put((key, True))


def on_release(key):
    if not close_event.is_set():
        __event_queue.put((key, False))


def parse(keylist):
    special_keys = re.findall(r"(\<.+?\>)", keylist)
    for key in special_keys:
        keylist = keylist.replace(key, "")
    normal_keys = keylist
    keylist = set()
    for i in normal_keys:
        try:
            keylist.add(KeyCode.from_char(i.lower()))
        except KeyError:
            print("invalid normal key")
    for i in special_keys:
        tmp: str = i[1:-1].lower()
        if "button" in tmp:
            keylist.add(Button(int(tmp[6:])))
        elif tmp in ("left", "right", "middle"):
            keylist.add(Button[tmp])
        else:
            keylist.add(Key[tmp])
    return keylist


def bind(keylist, callback, *args):
    keylist = parse(keylist)
    print(keylist)
    __callback_list.append((keylist, callback, args))


def unbind(keylist, callback, *args):
    keylist = parse(keylist)
    __callback_list.remove((keylist, callback, args))


def consumer():
    while True:
        event = __event_queue.get()
        if event is None:
            # clear
            __event_queue.task_done()
            while not __event_queue.empty():
                __event_queue.get()
                __event_queue.task_done()
            __state.clear()
            return
        if event[1]:
            __state.add(event[0])
            for i in filter(lambda x: __state == x[0], __callback_list):
                print("active", i)
                func = i[1]
                args = i[2]
                func(*args)
        if not event[1]:
            if event[0] in __state:
                __state.remove(event[0])
        __event_queue.task_done()

def key2str(key):
    try:
        key = key.name
    except:
        key = key.char
    return key

def capture_hotkey(process_callback=None, result_callback = None):
    state = set()
    count = 0
    lock = threading.Lock()
    over_event = threading.Event()
    def press(key):
        if over_event.is_set():
            return False
        state.add(key2str(key))
        if process_callback:
            print(state)
            process_callback(state)
    def click(x, y, button: mouse.Button, pressed: bool):
        if over_event.is_set():
            return False
        if pressed:
            state.add(key2str(button))
            if process_callback:
                print(state)
                process_callback(state)
        if not pressed:
            nonlocal count
            lock.acquire()
            count -= 1
            if len(state) + count == 0:
                lock.release()
                over_event.set()
                result_callback(state)
                return False
            lock.release()
    def release(key):
        if over_event.is_set():
            return False
        nonlocal count
        lock.acquire()
        count -= 1
        if len(state) + count == 0:
            lock.release()
            over_event.set()
            result_callback(state)
            return False
        lock.release() 
    _keyboard_listener = keyboard.Listener(
            on_press=press,
            on_release=release)
    _keyboard_listener.start()
    _mouse_listener = mouse.Listener(
            on_click=click)
    _mouse_listener.start()
    return over_event, _keyboard_listener, _mouse_listener


def start_keybinder(daemon=True):
    close_event.clear()
    global keyboard_listener, mouse_listener, keyboard_listener
    if keyboard_listener is None:
        keyboard_listener = keyboard.Listener(
            on_press=on_press,
            on_release=on_release)
        keyboard_listener.start()
    if mouse_listener is None:
        mouse_listener = mouse.Listener(
            on_click=on_click)
        mouse_listener.start()
    keybinder_thread = threading.Thread(target=consumer, daemon=daemon)
    keybinder_thread.start()
    return keybinder_thread


def stop_keybinder():
    print("stop keybinder")
    close_event.set()
    __event_queue.put(None)
    __event_queue.join()


if __name__ == "__main__":
    # bind("<Ctrl><B9>C", lambda: print("hello"))
    # start_keybinder().join()
    print(capture_hotkey(lambda x: print(x)))
