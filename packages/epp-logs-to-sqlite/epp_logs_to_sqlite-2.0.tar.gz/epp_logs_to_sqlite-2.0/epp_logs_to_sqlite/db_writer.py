def create_db(conn):
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE logs (
            id number NOT NULL,
            time text NOT NULL,
            description text NOT NULL,
            logId text NULL,
            info text NULL,
            groupName text NOT NULL,
            groupUserId number NOT NULL,
            timeSeconds number NOT NULL

        );"""
    )

    cursor.execute("""CREATE UNIQUE INDEX idx_logs ON logs (id);""")


def add_column_to_table(cursor, table, columName):
    cursor.execute(f'ALTER TABLE {table} ADD COLUMN {columName} text NULL;')


def insert_rows(cursor, table, columns, values):
    cursor.execute(
        'insert into {} ({}) values ({})'.format(table, ', '.join(columns), ', '.join('?' for c in columns)),
        tuple(values),
    )


def write(logEntries, cursor, startDbId=1):
    rowsNames = 'id time description logId info groupName groupUserId timeSeconds'.split(' ')
    for idx, logEntry in enumerate(logEntries):
        rowsValues = [
            startDbId + idx,
            str(logEntry.time),
            logEntry.getDescription(),
            logEntry.id,
            logEntry.info,
            logEntry.groupName,
            logEntry.groupUserId,
            logEntry.time.total_seconds(),
        ]

        extra = [(k, v) for k, v in logEntry.data.items()]

        insert_rows(
            cursor,
            'logs',
            rowsNames + [e[0] for e in extra],
            rowsValues + [e[1] for e in extra],
        )
