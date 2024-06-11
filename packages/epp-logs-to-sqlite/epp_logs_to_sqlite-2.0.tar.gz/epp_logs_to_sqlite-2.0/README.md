# A tool to parse Eggplant Performance test logs into a SQLite database

It can either be used as a library or run as a script:

epp_logs_to_sqlite run as a script:
```bash
python epp_logs_to_sqlite -m '<path to epp test base directory>'
```

epp_logs_to_sqlite used as a library:
```python
from epp_logs_to_sqlite import parse_value, logs_to_db


def parse_username(entries):
    parse_value(
        entries,
        "username",
        r"username: (.*)",
        tag=EventLogEntry.MESSAGE,
    )


results = '<path to epp test base directory>'
logs_to_db(results, [parse_username])
```