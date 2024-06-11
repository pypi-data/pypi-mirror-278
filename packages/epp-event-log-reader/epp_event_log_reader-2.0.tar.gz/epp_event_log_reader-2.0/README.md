A library to parse .event files from Eggplant Performance test results.

### read a single event log
```python
from epp_event_log_reader import EventLogReader
elr = EventLogReader(r'<path to a .event file>')

while elr.read(logEntry := EventLogEntry(), 0):
    print(logEntry.getShortText())

```

### read the event logs of a whole test
```python
from epp_event_log_reader import read_test_events

for logEntry in read_test_events(r'<path to the directory of the results of a test>'):
    print(logEntry.getShortText())
```
