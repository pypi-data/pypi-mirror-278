import datetime
import glob
import os
import logging

from .event_log_entry import EventLogEntry, EventLogEntryNode
from .epp_event_log_reader import EventLogReader

logger = logging.getLogger('epp_event_test_reader')

OPEN_SCOPE_TAGS = {
    EventLogEntry.START,
    EventLogEntry.START_ACTIVITY,
    EventLogEntry.CURRENT_SCRIPT,
    EventLogEntry.START_TRANSACTION,
}


CLOSE_SCOPE_TAGS = {
    EventLogEntry.END,
    EventLogEntry.END_ACTIVITY,
    EventLogEntry.END_TRANSACTION,
    EventLogEntry.FAIL_TRANSACTION,
}


def add_scope(logEntries):
    currentUser = None
    currentParent = None

    for logEntry in logEntries:
        if currentUser != (logEntry.groupName, logEntry.groupUserId):
            currentUser = (logEntry.groupName, logEntry.groupUserId)
            currentParent = logEntry
        else:
            while logEntry.tag == EventLogEntry.CURRENT_SCRIPT and currentParent.tag != EventLogEntry.START_ACTIVITY:
                currentParent = currentParent.parent

            currentParent.addChild(logEntry)

            if logEntry.tag in OPEN_SCOPE_TAGS:
                currentParent = logEntry
            elif logEntry.tag in CLOSE_SCOPE_TAGS:
                currentParent = currentParent.parent

    return logEntries


def read_events_file(fpath: str, entryclass=EventLogEntryNode) -> list[EventLogEntryNode]:
    groupName = fpath.split('\\')[-2]
    groupUserId = fpath.split('\\')[-1].replace('.event', '')

    events = []
    elr = EventLogReader(fpath)
    while elr.read(logEntry := entryclass(), 0):
        logEntry.time = datetime.timedelta(milliseconds=logEntry.time)
        logEntry.groupName = groupName
        logEntry.groupUserId = groupUserId
        events.append(logEntry)

    return events


def read_test_events(dirpath, entryclass=EventLogEntryNode) -> list[EventLogEntryNode]:
    entries = []

    def group_info(fpath):
        group, userId = fpath.split('\\')[-2:]
        return group, int(userId.replace('.event', ''))

    files = sorted(glob.glob(os.path.join(dirpath, r'**\*.event'), recursive=True), key=group_info)
    tfiles = len(files)

    for i, fpath in enumerate(files):
        group, userId = group_info(fpath)
        logger.info(f'{userId} of {group} ({i + 1}/{tfiles})')
        entries.extend(read_events_file(fpath, entryclass=entryclass))

    add_scope(entries)

    return entries
