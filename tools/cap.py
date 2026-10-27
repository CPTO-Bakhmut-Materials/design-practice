"""Screen-capture harness for the lesson screenshots (Hyprland + ydotool + grim).

Apps are launched on workspace 2 with a sandboxed profile (clean default UI,
user's own settings untouched). Capturing switches to workspace 2, takes the
shot with grim, and `back()` returns to workspace 1.
"""
import json, os, subprocess, time

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
SANDBOX = os.path.join(ROOT, '.sandbox')
YSOCK = '/run/user/1000/.ydotool_socket'
WS = int(os.environ.get('CAP_WS', 2))  # set CAP_WS when workspace 2 is in use

# linux/input-event-codes.h
KEYS = {
    'esc': 1, 'escape': 1, '1': 2, '2': 3, '3': 4, '4': 5, '5': 6, '6': 7, '7': 8, '8': 9, '9': 10, '0': 11,
    'minus': 12, 'equal': 13, 'backspace': 14, 'tab': 15,
    'q': 16, 'w': 17, 'e': 18, 'r': 19, 't': 20, 'y': 21, 'u': 22, 'i': 23, 'o': 24, 'p': 25,
    'enter': 28, 'ctrl': 29, 'a': 30, 's': 31, 'd': 32, 'f': 33, 'g': 34, 'h': 35, 'j': 36,
    'k': 37, 'l': 38, 'shift': 42, 'z': 44, 'x': 45, 'c': 46, 'v': 47, 'b': 48, 'n': 49, 'm': 50,
    'comma': 51, 'dot': 52, 'slash': 53, 'alt': 56, 'space': 57,
    'f1': 59, 'f2': 60, 'f3': 61, 'f4': 62, 'f5': 63, 'f6': 64, 'f7': 65, 'f8': 66, 'f9': 67, 'f10': 68,
    'home': 102, 'up': 103, 'pageup': 104, 'left': 105, 'right': 106, 'end': 107, 'down': 108,
    'pagedown': 109, 'delete': 111, 'super': 125, 'kpplus': 78, 'kpminus': 74,
}


def env():
    e = dict(os.environ)
    for k, sub in (('XDG_CONFIG_HOME', 'config'), ('XDG_DATA_HOME', 'data'), ('XDG_CACHE_HOME', 'cache')):
        e[k] = os.path.join(SANDBOX, sub)
        os.makedirs(e[k], exist_ok=True)
    home = os.path.join(SANDBOX, 'home')
    os.makedirs(home, exist_ok=True)
    link = os.path.join(home, 'brand-day')
    if not os.path.exists(link):
        os.symlink(os.path.join(ROOT, 'brand-day'), link)
    e['HOME'] = home
    fonts = os.path.join(e['XDG_DATA_HOME'], 'fonts')
    if not os.path.exists(fonts):
        os.symlink(os.path.join(ROOT, 'brand-day', 'fonts'), fonts)
    e.update(LANG='en_US.UTF-8', LANGUAGE='en_US:en', LC_ALL='en_US.UTF-8', YDOTOOL_SOCKET=YSOCK,
             INKSCAPE_PROFILE_DIR=os.path.join(SANDBOX, 'config', 'inkscape'))
    return e


def run(*a, **kw):
    return subprocess.run(a, check=True, capture_output=True, text=True, env=env(), **kw).stdout


def hypr(*a):
    return run('hyprctl', *a)


def dispatch(*a):
    return hypr('dispatch', *a)


def clients():
    return json.loads(hypr('clients', '-j'))


def find(cls=None, title=None):
    for c in clients():
        if cls and cls.lower() not in c['class'].lower():
            continue
        if title and title.lower() not in c['title'].lower():
            continue
        return c
    return None


def launch(cmd, cls, title=None, timeout=60):
    """Start cmd (shell string) silently on workspace 2 with sandbox env; wait for its window."""
    e = env()
    exports = ' '.join(f"{k}='{e[k]}'" for k in ('HOME', 'XDG_CONFIG_HOME', 'XDG_DATA_HOME', 'XDG_CACHE_HOME', 'LANG',
                                                  'LANGUAGE', 'LC_ALL', 'INKSCAPE_PROFILE_DIR'))
    dispatch('exec', f"[workspace {WS} silent] env {exports} {cmd}")
    t0 = time.time()
    while time.time() - t0 < timeout:
        c = find(cls, title)
        if c and c['mapped']:
            return c
        time.sleep(0.5)
    raise TimeoutError(f'window {cls} did not appear')


_prev_ws = ['1']


def show():
    cur = str(json.loads(hypr('activeworkspace', '-j'))['id'])
    if cur != str(WS):
        _prev_ws[0] = cur
    dispatch('workspace', str(WS))
    time.sleep(0.4)


def back():
    dispatch('workspace', _prev_ws[0])


def focus(c):
    dispatch('focuswindow', f"address:{c['address']}")


def close(c):
    dispatch('closewindow', f"address:{c['address']}")


def geom(c):
    c = next(x for x in clients() if x['address'] == c['address'])
    (x, y), (w, h) = c['at'], c['size']
    return x, y, w, h


def wait(s=0.5):
    time.sleep(s)


# --- input -----------------------------------------------------------------
def move(x, y):
    run('ydotool', 'mousemove', '--absolute', '-x', str(int(x)), '-y', str(int(y)))
    for _ in range(3):
        cx, cy = (int(v) for v in hypr('cursorpos').split(','))
        dx, dy = int(x) - cx, int(y) - cy
        if dx == 0 and dy == 0:
            break
        run('ydotool', 'mousemove', '-x', str(dx), '-y', str(dy))
        time.sleep(0.05)


def click(x, y, button='left', double=False):
    move(x, y)
    code = {'left': '0xC0', 'right': '0xC1', 'middle': '0xC2'}[button]
    run('ydotool', 'click', *(['-r', '2', '-D', '80'] if double else []), code)
    time.sleep(0.25)


def drag(x1, y1, x2, y2, steps=12, hold=False):
    """Press at (x1,y1), move to (x2,y2). If hold, leave the button down (call release())."""
    move(x1, y1)
    run('ydotool', 'click', '0x40')  # left down
    for i in range(1, steps + 1):
        move(x1 + (x2 - x1) * i / steps, y1 + (y2 - y1) * i / steps)
        time.sleep(0.02)
    if not hold:
        release()


def release():
    run('ydotool', 'click', '0x80')
    time.sleep(0.2)


def key(combo):
    """combo like 'ctrl+shift+e' or 'f10'."""
    names = combo.lower().split('+')
    codes = [KEYS[n] for n in names]
    seq = [f'{c}:1' for c in codes] + [f'{c}:0' for c in reversed(codes)]
    run('ydotool', 'key', *seq)
    time.sleep(0.25)


def type_text(s):
    """Type text via clipboard (works for Cyrillic regardless of keyboard layout)."""
    subprocess.run(['wl-copy', s], check=True)
    time.sleep(0.1)
    key('ctrl+v')


def type_ascii(s):
    if s.startswith('-'):  # ydotool would parse a leading '-' as an option
        key('minus')
        s = s[1:]
    if s:
        run('ydotool', 'type', '-d', '20', s)
    time.sleep(0.2)


# --- capture -----------------------------------------------------------------
def shot(path, c=None, region=None, cursor=True):
    """Capture window c (full window) or region=(x,y,w,h) to path."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if region is None:
        region = geom(c)
    x, y, w, h = region
    args = ['grim'] + (['-c'] if cursor else []) + ['-g', f'{x},{y} {w}x{h}', path]
    run(*args)
    return path


def field(x, y, val):
    """Type a value into a toolbar/dialog entry and commit with Enter."""
    click(x, y)
    key('ctrl+a')
    type_ascii(str(val))
    key('enter')
    time.sleep(0.4)


def floatwin(c, w, h):
    """Make a (dialog) window floating, resize it and center it on the screen."""
    a = f"address:{c['address']}"
    if not c.get('floating'):
        dispatch('togglefloating', a)
    dispatch('resizewindowpixel', f'exact {w} {h},{a}')
    dispatch('centerwindow') if False else None
    dispatch('movewindowpixel', f'exact {(1920 - w) // 2} {(1200 - h) // 2 + 15},{a}')
    time.sleep(0.6)
    return geom(c)
