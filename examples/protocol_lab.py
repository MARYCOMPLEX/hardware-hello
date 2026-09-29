"""HH1 教学协议；不是原项目 LinkIt。python3 examples/protocol_lab.py"""
import struct
import unittest
from dataclasses import dataclass

MAGIC = b"HH"
MAX_PAYLOAD = 256
HEADER = struct.Struct("<BBHH")

def crc16(data):
    crc = 0xFFFF
    for byte in data:
        crc ^= byte << 8
        for _ in range(8):
            crc = ((crc << 1) ^ (0x1021 if crc & 0x8000 else 0)) & 0xFFFF
    return crc

@dataclass(frozen=True)
class Frame:
    kind: int
    sequence: int
    payload: bytes

def encode(kind, sequence, payload):
    if not 0 <= kind <= 255 or not 0 <= sequence <= 65535:
        raise ValueError("type/sequence out of range")
    if len(payload) > MAX_PAYLOAD:
        raise ValueError("payload too long")
    body = HEADER.pack(1, kind, sequence, len(payload)) + payload
    return MAGIC + body + struct.pack("<H", crc16(body))

def temperature(frame):
    if frame.kind != 1 or len(frame.payload) != 2:
        raise ValueError("not a temperature frame")
    return struct.unpack("<h", frame.payload)[0] / 100

class Decoder:
    """Incremental parser. Integration must expire stalled partial frames.

    The internal buffer is bounded by one maximum frame (266 bytes).
    feed returns a list, so callers should also bound their input chunk size.
    """
    def __init__(self):
        self.buffer = bytearray()

    def reset(self):
        """Call after the transport's incomplete-frame deadline expires."""
        self.buffer.clear()

    def feed(self, data):
        frames = []
        for byte in data:
            self.buffer.append(byte)
            while self.buffer:
                pos = self.buffer.find(MAGIC)
                if pos < 0:
                    self.buffer[:] = b"H" if self.buffer[-1:] == b"H" else b""
                    break
                del self.buffer[:pos]
                if len(self.buffer) < 8:
                    break
                version, kind, seq, size = HEADER.unpack(self.buffer[2:8])
                if version != 1 or size > MAX_PAYLOAD:
                    del self.buffer[0]
                    continue
                total = 10 + size
                if len(self.buffer) < total:
                    break
                expected = struct.unpack("<H", self.buffer[total-2:total])[0]
                if crc16(self.buffer[2:total-2]) != expected:
                    del self.buffer[0]
                    continue
                frames.append(Frame(kind, seq, bytes(self.buffer[8:total-2])))
                del self.buffer[:total]
        return frames

class ProtocolTests(unittest.TestCase):
    def setUp(self):
        self.packet = encode(1, 65535, struct.pack("<h", -1234))
        self.frame = Frame(1, 65535, struct.pack("<h", -1234))

    def test_known_crc(self):
        self.assertEqual(crc16(b"123456789"), 0x29B1)

    def test_every_split(self):
        for pos in range(len(self.packet)+1):
            d = Decoder()
            self.assertEqual(d.feed(self.packet[:pos]) + d.feed(self.packet[pos:]), [self.frame])

    def test_coalescing_noise_and_signed_value(self):
        d = Decoder()
        self.assertEqual(d.feed(b"noiseH" + self.packet * 3), [self.frame] * 3)
        self.assertEqual(temperature(self.frame), -12.34)

    def test_crc_recovery(self):
        bad = bytearray(self.packet)
        bad[-1] ^= 1
        self.assertEqual(Decoder().feed(bad + self.packet), [self.frame])

    def test_invalid_headers(self):
        for version, size in [(2, 2), (1, 257)]:
            bad = MAGIC + HEADER.pack(version, 1, 0, size)
            self.assertEqual(Decoder().feed(bad + self.packet), [self.frame])

    def test_limits_and_wrapping(self):
        packet = encode(2, (65535 + 1) & 0xFFFF, b"x"*256)
        self.assertEqual(Decoder().feed(packet), [Frame(2, 0, b"x"*256)])
        with self.assertRaises(ValueError):
            encode(1, 0, b"x"*257)
        with self.assertRaises(ValueError):
            temperature(Frame(1, 0, b""))

    def test_partial_timeout_and_noise_bound(self):
        d = Decoder()
        self.assertEqual(d.feed(self.packet[:8]), [])
        d.reset()
        self.assertEqual(d.feed(self.packet), [self.frame])
        self.assertEqual(d.feed(b"H"*10000), [])
        self.assertLessEqual(len(d.buffer), 266)

if __name__ == "__main__":
    unittest.main(verbosity=2)
