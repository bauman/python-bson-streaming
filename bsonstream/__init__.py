from bson import InvalidBSON, BSON, codec_options
import sys
import struct


class BSONInput(object):
    """
    credit to @mpobrien (https://raw.github.com/mongodb/mongo-hadoop/master/streaming/language_support/python/pymongo_hadoop/input.py)
    """
    
    """Custom file class for decoding streaming BSON,
    based upon the Dumbo & "typedbytes" modules at
    https://github.com/klbostee/dumbo &
    https://github.com/klbostee/typedbytes
    """

    def __init__(self, fh=sys.stdin,
                 unicode_errors: str = 'strict',
                 fast_string_prematch: bytes = b"",
                 decode: bool = True):
        self.fh = fh
        self.unicode_errors = unicode_errors
        if not isinstance(fast_string_prematch, bytes):
            raise ValueError("fast_string_prematch must be a bytes object")
        self.fast_string_prematch=fast_string_prematch
        self.eof = False
        self.decode = decode
        self.codec = codec_options.CodecOptions(tz_aware=True)
        
    def _read(self):
        try:
            size_bits = self.fh.read(4)
            size = struct.unpack("<i", size_bits)[0] - 4  # BSON size byte includes itself
            data = size_bits + self.fh.read(size)
            if len(data) != size + 4:
                raise struct.error("Unable to read expected BSON Chunk; " +
                                   "EOF, underful buffer or invalid object size.")
            eoo = 0x00
            if data[size + 4 - 1] != eoo:
                raise InvalidBSON("Bad EOO in BSON Data")
            if self.fast_string_prematch in data:
                if self.decode:
                    try:
                        return BSON(data).decode(self.codec)
                    except TypeError:
                        return BSON(data).decode()
                else:
                    return data
        except struct.error as e:
            self.eof = True
            raise StopIteration(e)

    def read(self):
        try:
            return self._read()
        except StopIteration as e:
            #print >> sys.stderr, "Iteration Failure: %s" % e
            return None

    def _reads(self):
        r = self._read
        while 1:
            try:
                data = r()
                if data:
                    yield data
            except StopIteration:
                break

    def close(self):
        self.fh.close()

    __iter__ = reads = _reads


class KeyValueBSONInput(BSONInput):
    def read(self):
        try:
            doc = self._read()
        except StopIteration as e:
            # print >> sys.stderr, "Key/Value Input iteration failed/stopped: %s" % e
            return None
        return doc

    def reads(self):
        it = self._reads()
        n = it.__next__
        while 1:
            try:
                doc = n()
                yield doc
            except StopIteration:
                break

    __iter__ = reads
