import time
import os
from contextlib import suppress
import sqlite3
from epp_event_log_reader import read_test_events

from .db_writer import create_db, add_column_to_table, write
from .event_log_entry_extra_data import EventLogEntryExtraData
from .util import time_it


def logs_to_db(resultsPath, extra_fn=[]):
    start = time.monotonic()

    with time_it('parse files'):
        entries = read_test_events(resultsPath, entryclass=EventLogEntryExtraData)

    for fn in extra_fn:
        fn(entries)

    with time_it('save'):
        dbPath = os.path.join(resultsPath, 'results.db')
        print(f'SQLite DB path: {dbPath}')

        with suppress(FileNotFoundError):
            os.remove(dbPath)

        conn = sqlite3.connect(dbPath)
        create_db(conn)
        cur = conn.cursor()

        extraColumns = set()
        for entry in entries:
            for c in entry.data:
                extraColumns.add(c)
        for c in extraColumns:
            add_column_to_table(cur, 'logs', c)

        write(entries, cur, startDbId=0)

        conn.commit()

    print(f'The total execution took {time.monotonic() - start:.1f} seconds')
