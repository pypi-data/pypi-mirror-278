import re
from contextlib import contextmanager
import time


def parse_value(logEntries, fieldName, infoRegexp, tag=None, logId=None):
    def entryFilter(entry):
        if tag is not None and entry.tag != tag:
            return False
        if logId is not None and entry.id != logId:
            return False
        return True

    for logEntry in filter(entryFilter, logEntries):
        if m := re.search(infoRegexp, logEntry.dumpData(), re.DOTALL | re.MULTILINE):
            logEntry.addFileld(fieldName, m.group(1))


@contextmanager
def time_it(msg, *args, **kwds):
    start = time.monotonic()
    print(f'{msg} - Start')
    try:
        yield None
    finally:
        print(f'{msg} - Took {time.monotonic() - start:.1f}\n')
