__author__ = 'Rui'

if __name__ == '__main__':
    from redis import Redis
    from rq_scheduler import Scheduler
    from datetime import datetime
    import data_collector
    import settings.config as config

    scheduler = Scheduler(connection=Redis())
    scheduler.schedule(
        scheduled_time=datetime.now(), # Time for first execution, in UTC timezone
        func=data_collector.get_line_status,
        args=[config.ACTIVE_BACKEND],
        kwargs={},         # Keyword arguments passed into function when executed
        interval=10,                   # Time before the function is called again, in seconds
        repeat=None,
        result_ttl=0                      # Repeat this number of times (None means repeat forever)
    )

