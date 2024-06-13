# Felicien

Felicien is you companion to retrieve timeseries from a TSDB, to transform it in various format and to push it to a TSDB. Supported TSDB are Prometheus compatible (Prometheus, VictoriaMetrics, ...).

## Installation

Felicien is available on PyPI:

```sh
$ python -m pip install felicien
```

Felicien officially supports Python 3.11+.

## Usage

Felicien helps you to connect to a TSDB, and to play with timeseries.

```python
>>> from felicien import FeliConnector
>>> tsdb = FeliConnector(url="https://my.victoriametrics.instance", tsdb="victoriametrics")
>>> tsdb
FeliConnector([victoriametrics]{https://my.victoriametrics.instance})

>>> ts_scalar = tsdb.get_timeserie(metric='vm_cache_entries{job=~"victoriametrics", instance=~"victoriametrics:8428", type="storage/hour_metric_ids"}')
>>> ts_scalar
FeliTS(vm_cache_entries{instance:"victoriametrics:8428", job:"victoriametrics", type:"storage/hour_metric_ids"}, 1 datapoints)
>>> ts_scalar.as_prometheus()
{'metric': {'__name__': 'vm_cache_entries',
  'instance': 'victoriametrics:8428',
  'job': 'victoriametrics',
  'type': 'storage/hour_metric_ids'},
 'values': [17805.0],
 'timestamps': [1713606731000]}

>>> ts_vector = tsdb.get_timeserie(metric='vm_cache_entries{job=~"victoriametrics", instance=~"victoriametrics:8428", type="storage/hour_metric_ids"}[1h]')
>>> ts_vector
FeliTS(vm_cache_entries{job:"victoriametrics", type:"storage/hour_metric_ids", instance:"victoriametrics:8428"}, 60 datapoints)
>>> ts_vector.frequency
Timedelta('0 days 00:01:00')
>>> ts_vector.data.describe()
count       60.000000
mean     17768.150000
std          5.580915
min      17766.000000
25%      17766.000000
50%      17766.000000
75%      17767.000000
max      17805.000000
dtype: float64
>>> ts_vector.trim_by_size(boundary=10, keep="left")
2024-04-20 09:03:40.177000046    17766.0
2024-04-20 09:04:40.177000046    17766.0
2024-04-20 09:05:40.177000046    17766.0
2024-04-20 09:06:40.177000046    17766.0
2024-04-20 09:07:40.177000046    17766.0
2024-04-20 09:08:40.177000046    17766.0
2024-04-20 09:09:40.177000046    17766.0
2024-04-20 09:10:40.177000046    17766.0
2024-04-20 09:11:40.177000046    17766.0
2024-04-20 09:12:40.177000046    17766.0
dtype: float64
```

## Main features

- Connect to a TSDB, and check connectivity
- Get a timeserie and store it in a Pandas Series
- Estimate frequency of a timeserie
- Trim a timeserie by date or by size
- Transform the timeserie in a pandas.DataFrame
- Delete a timeserie in a TSDB
- Import a timeserie into a TSDB
- Normalize a timeserie on its frequency

## License

[MIT](LICENSE)
