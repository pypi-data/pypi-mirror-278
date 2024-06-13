from datetime import datetime, timedelta


class ThroughputTimer:
    def __init__(self):
        self.start_time = None
        self.total_processed = 0

    def start(self):
        self.start_time = datetime.now()
        self.total_processed = 0
        return self

    def stats(self, remaining_item_count):
        stats = []
        if self.start_time is not None and self.total_processed > 0:
            elapsed = (datetime.now() - self.start_time).total_seconds()
            if elapsed >= 1:
                per_second = round(self.total_processed / elapsed)
                stats.append('Items/sec: {0}'.format(per_second))
                if remaining_item_count > 0:
                    delta = timedelta(seconds=round(elapsed * (remaining_item_count / self.total_processed)))
                    estimated = str(delta).split('.')[0]
                    stats.append('ETA: {0}'.format(estimated))

        return ', '.join(stats)

    def processed(self):
        self.total_processed += 1
