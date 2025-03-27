from statsd import StatsClient

STATSD_HOST = 'localhost'
STATSD_PORT = 8125

statsd_client = StatsClient(STATSD_HOST, STATSD_PORT)