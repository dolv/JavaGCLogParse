from pprint import pformat
from datetime import datetime
import re

gcLinePatterns={
    "Full_GC": re.compile('\[Full GC.*\]'),
    "GC_pause": re.compile('\[GC pause.*\]'),
    "concurrent_root_region_scan_end": re.compile('\[GC concurrent-root-region-scan-end.*\]'),
    "concurrent_mark_end": re.compile('\[GC concurrent-mark-end,.*\]'),
    "concurrent_cleanup_end": re.compile('\[GC concurrent-cleanup-end,.*\]'),
    "cleanup": re.compile('\[GC cleanup.*\]'),
    "remark": re.compile('\[GC remark.*\]'),
    "ref_proc": re.compile('\[GC ref-proc.*\]'),
    "undefined": re.compile('.*')
}

class GCLogLine:
    message = ""
    timefield = None
    record_type = None

    def __init__(self, line='', timeformat='%Y-%m-%dT%H:%M:%S.%f%z'):
        self.timeformat = timeformat
        self.timefield = self._get_timefield(line)
        self.message = ' '.join(line.split(' ')[2:])
        self.record_type = self._get_recordtype()

    def __str__(self):
        return "{} {} {}".format(self.record_type, self.timefield.strftime(self.timeformat), self.message)

    def _get_timefield(self, line):
        return datetime.strptime(line.split(' ')[0][:-1], self.timeformat).replace(tzinfo=None)

    def _get_recordtype(self):
        for type,pattern in gcLinePatterns.items():
            if pattern.match(self.message) is not None:
                return type


class Watcher:
    timeframe = 1
    timeformat = None
    events = []

    counters = {
        "Full_GC_free_below_20": 0,
        "Full_GC_time": float(0),
        "Full_GC_time_percent": float(0),
        "All_GC_events_time_total": float(0)
    }

    def __init__(self, timeframe_minutes=5, timeformat='%Y-%m-%dT%H:%M:%S.%f%z'):
        self.timeframe = timeframe_minutes
        self.timeformat = timeformat

    def add_line(self, event):
        # now = datetime.now()
        now = datetime.strptime('2017-03-01T17:08:27.086-0500','%Y-%m-%dT%H:%M:%S.%f%z').replace(tzinfo=None)
        if self.events and self.events[0] and self.events[0].timefield:
            initial_time = self.events[0].timefield
        else:
            initial_time = event.timefield

        time_delta = now - initial_time
        time_difference = divmod(time_delta.days * 86400 + time_delta.seconds, 60)

        if time_difference[0] >= 5 and self.events:
            gc_event_duration = self._get_GC_time(self.events[0].message)
            self.counters['All_GC_events_time_total'] -= gc_event_duration
            if self.events[0].record_type == "Full GC":
                self.counters['Full_GC_time'] -= gc_event_duration
                if self._full_gc_freed_mem_below(self.events[0].message, 0.2):
                    self.counters['Full_GC_free_below_20'] -= 1

            self.events.pop(0)

        self.events.append(event)

        gc_event_duration = self._get_GC_time(event.message)
        self.counters['All_GC_events_time_total'] += gc_event_duration
        if event.record_type == "Full_GC":
            self.counters['Full_GC_time'] += gc_event_duration
            if self._full_gc_freed_mem_below(event.message, 0.2):
                self.counters['Full_GC_free_below_20'] += 1

        self._update_counters()


    def _full_gc_freed_mem_below(self, message, percent=0.2):
        result =  False
        mem_info_pattern = re.compile('.*->(\d+)M\((\d+)M')
        mem_info_match = mem_info_pattern.match(message)
        used_mem = int(mem_info_match.group(1))
        total_mem =  int(mem_info_match.group(2))
        if (total_mem - used_mem)/total_mem < percent: result = True
        return result

    def _get_GC_time(self, message):
        timespent_pattern = re.compile('.* (\d+\.\d+) sec')
        timespent_match = timespent_pattern.match(message)
        return float(timespent_match.group(1))

    def _update_counters(self):
        self.counters['Full_GC_time_percent'] = self.counters['Full_GC_time'] / self.counters['All_GC_events_time_total']

    def __str__(self):
        output = {}
        output['timeframe'] = self.timeframe
        output['timeformat'] = self.timeformat
        output['events'] = []
        for line in self.events:
            output['events'].append(str(line))
        return pformat(output, width=160)