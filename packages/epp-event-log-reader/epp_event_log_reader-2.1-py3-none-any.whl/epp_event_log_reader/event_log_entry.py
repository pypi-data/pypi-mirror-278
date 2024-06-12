

class EventLogEntry:
    NULL_EVENT = 0
    CONNECT = 1
    END_ACTIVITY = 2
    ERROR = 3
    WARNING = 4
    TIMEOUT = 5
    START_TRANSACTION = 6
    END_TRANSACTION = 7
    SYNC = 8
    FAIL_TRANSACTION = 9
    EXIT = 10
    START = 11
    END = 12
    MESSAGE = 13
    START_ACTIVITY = 14
    PASS = 15
    FAIL = 16
    START_TIMING = 17
    END_TIMING = 18
    FAIL_TIMING = 19
    SUSPEND_TRANSACTION = 20
    RESUME_TRANSACTION = 21
    CURRENT_SCRIPT = 22
    METRIC = 23
    START_REQUEST = 24
    END_REQUEST = 25
    RECORD_TRANSACTION = 26
    #  Make sure that the following exceeds the highest event number by one
    MAX_TAG = 27

    dataSeparator = '\t'

    descriptions = [
        'None',
        'Connect',
        'End activity',
        'Error',
        'Warning',
        'Timeout',
        'Start transaction',
        'End transaction',
        'Sync',
        'Fail transaction',
        'Exit',
        'Start',
        'End',
        'Message',
        'Start activity',
        'Pass',
        'Fail',
        'Start timing',
        'End timing',
        'Fail timing',
        'Suspend transaction',
        'Resume transaction',
        'Current script',
        'Metric',
        'Start Request',
        'End Request',
        'Transaction',
    ]

    def getDescription(self):
        return EventLogEntry.descriptions[self.tag]

    def formatVUId(self, injector=None, engine=None, group=None, vu=0):
        return '%s.%s.%s.%04d' % (injector, engine, group, vu)

    def __init__(self):
        self.tag = EventLogEntry.NULL_EVENT
        self.time = -1
        self.id = ''
        self.info = ''

    def dumpData(self, injector=None, engine=None, group=None, vu=0):
        return (
            self.formatVUId(injector, engine, group, vu)
            + EventLogEntry.dataSeparator
            + str(self.time)
            + EventLogEntry.dataSeparator
            + self.getDescription()
            + EventLogEntry.dataSeparator
            + self.id
            + EventLogEntry.dataSeparator
            + self.info
        )

    def getText(self):
        return (
            self.formatVUId()
            + ', '
            + str(self.time)
            + EventLogEntry.dataSeparator
            + self.getDescription()
            + EventLogEntry.dataSeparator
            + self.id
            + EventLogEntry.dataSeparator
            + self.info
        )

    def getShortText(self):
        return self.getDescription() + EventLogEntry.dataSeparator + self.id + EventLogEntry.dataSeparator + self.info


class EventLogEntryNode(EventLogEntry):
    def __init__(self):
        super().__init__()
        self._parent = None
        self.children = []

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, value):
        self._parent = value

    def addChild(self, child):
        self.children.append(child)
        child.parent = self
