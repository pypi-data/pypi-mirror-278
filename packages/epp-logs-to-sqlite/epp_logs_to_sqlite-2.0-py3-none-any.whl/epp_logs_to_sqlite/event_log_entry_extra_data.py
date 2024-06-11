from epp_event_log_reader import EventLogEntryNode


class EventLogEntryExtraData(EventLogEntryNode):
    def __init__(self):
        super().__init__()
        self.data = {}

    def addFileld(self, name, value):
        self.data[name] = value
