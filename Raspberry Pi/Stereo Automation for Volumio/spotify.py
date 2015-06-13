# Script partly taken from https://github.com/Schnouki/spop/tree/master/dspop
# This script is meant to work only with spop (which is actually the Spotify service running on Volumio)

import json
import socket

# {{{ Parameters
# Possible values: {index}, {artist}, {track}, {album}, {duration}, {uri}, {playing}
TRACK_FMT = "{playing}{index} - {artist} - {album} - {track} ({duration})"
SEARCH_ALBUM_FMT = "({year}) {artist} - {album} ({tracks} tracks)"
SEARCH_PLAYLIST_FMT = "{name} (by {owner}, {tracks} tracks)"
SEARCH_TRACK_FMT = "{artist} - {album} - {track} ({duration})"

DMENU_OPTS = ["-i", "-l", "40"]
ROFI_OPTS = ["-dmenu" , "-columns" , "1"]

# }}}
# {{{ Spop client
class SpopClient:
    def __init__(self, host, port):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.connect((host, port))
        self.greeting = self._sock.recv(1024).decode().strip()

    def _command(self, command, *args):
        esc_args = ['"'+arg.replace('"', '\\"')+'"' if type(arg) is str else str(arg) for arg in args]
        esc_args.insert(0, command)
        cmd = " ".join(esc_args) + "\n"
        self._sock.send(cmd.encode())

        buf = b""
        while True:
            tmp = self._sock.recv(1024)
            buf += tmp
            try:
                obj = json.loads(buf.decode())
                return obj
            except:
                pass

    def __getattr__(self, name):
        if name in ("repeat", "shuffle", "qclear", "qls", "ls", "goto", "add", "next", "prev", "toggle", "play", "offline_toggle",
                    "search", "status", "uadd", "uinfo", "uplay"):
            def func(*attrs):
                return self._command(name.replace("_", "-"), *attrs)
            return func
        else:
            raise AttributeError
