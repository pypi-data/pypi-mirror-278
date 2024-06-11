import struct
import socket


def pack_varint(data: int) -> bytes:
    ordinal = b''
    while data != 0:
        byte = data & 0x7F
        data >>= 7
        ordinal += struct.pack('B', byte | (0x80 if data > 0 else 0))
    return ordinal


def read_varint(sock: socket.socket) -> int:
    data = 0
    for i in range(5):
        ordinal = sock.recv(1)
        if len(ordinal) == 0:
            break

        byte = ord(ordinal)
        data |= (byte & 0x7F) << 7 * i
        if not byte & 0x80:
            break
    return data
