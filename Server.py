import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('127.0.0.1', 8000))
s.setblocking(False)
plist = []
slist = []
while True:
    data = None
    addr = None
    try:
        data, addr = s.recvfrom(1024)
    except Exception as _:
        pass
    if data == b'Pending':
        if len(plist) > 0:
            slist.append((addr, plist.pop()))
            s.sendto(b'Start', slist[len(slist)-1][0])
            s.sendto(b'Start', slist[len(slist)-1][1])
        else:
            plist.append(addr)
    if data is not None and data[:5] == b'Score':
        for pair in slist:
            if addr == pair[0]:
                s.sendto(data, pair[1])
                break
            if addr == pair[1]:
                s.sendto(data, pair[0])
                break
    if data is not None and data == b'Over':
        for pair in slist:
            if addr == pair[0]:
                s.sendto(data, pair[1])
                slist.remove(pair)
                break
            if addr == pair[1]:
                s.sendto(data, pair[0])
                slist.remove(pair)
                break
