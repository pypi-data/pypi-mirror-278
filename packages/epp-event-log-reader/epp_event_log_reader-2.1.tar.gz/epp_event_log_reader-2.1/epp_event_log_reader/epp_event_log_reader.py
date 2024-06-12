import struct

from .event_log_entry import EventLogEntry


class EventLogReader:
    A = 1
    B = 2

    def __init__(self, path=None):
        self.inError = 0
        self.processingWarnings = 0
        self.warnings = []
        self.errors = []
        self.path = path
        self.eventCount = 0
        if path is not None:
            self.open(path)
        else:
            self.file = None

    def open(self, path):
        self.file = open(path, 'rb')
        self.inError = 0
        self.processingWarnings = 0

        if struct.unpack('!H', self.file.read(2))[0] == 0xFF02:
            self.version = EventLogReader.B
        else:
            self.version = EventLogReader.A
            self.file.seek(0)

    def close(self):
        if self.file is not None:
            self.file.close()

    def printContents(self, out, vu):
        logEntry = EventLogEntry()
        while self.read(logEntry, 0):
            out.write(logEntry.getText())
            out.write('\n')
        if self.error():
            out.write('Error(s): ' + str(self.errors) + '\n')

    def error(self):
        return self.inError

    def getProcessingWarningsCount(self):
        return self.processingWarnings

    def getProcessingWarnings(self):
        return self.warnings

    def getProcessingErrors(self):
        return self.errors

    #  Return true if more to read
    def read(self, entry, timeOffset=0):
        self.eventCount += 1
        #  read and check tag
        s = self.file.read(1)
        if len(s) == 0:
            self.eof = 1
            return 0
        else:
            entry.tag = struct.unpack('b', s)[0]

        if entry.tag < EventLogEntry.NULL_EVENT or entry.tag >= EventLogEntry.MAX_TAG:
            self.inError = 1
            self.errors.append('invalid entry :: tag=' + str(entry.tag) + ' @ event:' + str(self.eventCount))
            return 0

        #  read and check time
        s = self.file.read(4)
        if len(s) < 4:
            self.eof = True
            return 0
        else:
            entry.time = struct.unpack('!I', s)[0]

        if entry.time < 0:
            self.inError = True
            self.errors.append('invalid time: ' + entry.time + ' @ event:' + self.eventCount)
        else:
            entry.time += timeOffset

        #  read and check id
        eid = []
        while 1:
            s = self.file.read(1)
            if len(s) == 0:
                self.eof = True
                return 0
            else:
                char = struct.unpack('c', s)[0]
            if char == b'\x00':
                break
            else:
                eid.append(char)

        eid = b''.join(eid).decode('ascii')

        entry.id = ''.join(eid)

        info = []
        while 1:
            s = self.file.read(1)
            if len(s) == 0:
                self.eof = True
                return 0
            else:
                char = struct.unpack('c', s)[0]
            if char == b'\x00':
                break
            else:
                info.append(char)

        entry.info = b''.join(info).decode('utf-8')

        if self.version == EventLogReader.B:
            struct.unpack('!I', self.file.read(4))[0]

        return 1
