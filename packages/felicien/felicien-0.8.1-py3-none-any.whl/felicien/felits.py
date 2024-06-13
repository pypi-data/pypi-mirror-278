#!/usr/bin/env python
# -*- coding: utf8 -*-

import pandas as pd
import itertools
import datetime as dt
import matplotlib.pyplot as plt
import json


# Smallest frequency should be seen at least 10% of the Serie to be considered
# as the Serie frequency
MIN_FREQUENCY_REPRESENTATION = 0.1


class FeliTS:
    """A Timeserie of a Prometheus metric

    This is a metric representation as returned by the Prometheus API. It
    includes the metric definition, and the data as a pandas Series.
    see official documentation:
    https://prometheus.io/docs/prometheus/latest/querying/api/#expression-query-result-formats

    Attributes:

    - name: A string with the name of the metric

    - labels: A dict of labels of the metric

    - data: A pandas.Series with the timeserie
    """

    def __init__(
        self,
        from_prom: dict = None,
        name: str = None,
        labels: dict = {},
        values: pd.Series = None,
    ) -> None:
        """Initializes the instance based on the data from Prometheus API

        Args:
            from_prom (dict, optional): Query result data from Prometheus API.

            name (str, optional): Name of the metric

            labels (dict, optional): Labels of the metric

            values (pandas Series, optional): Values and their timestamp of
              the timeserie as the Index

        Raises:
            AttributeError if the metric has no __name__

            AttributeError if the metric has no value (or values)

            ValueError if the value list is empty

            ValueError if a item of the value list hasn't the right format:
            [timestamp, metric_value]

            AttributeError if neither an output from Prometheus API nor raw
            data are passed to the constructor
        """
        if from_prom is not None:
            # Construct from Prometheus API output
            self.name = from_prom.get("metric", {}).get("__name__", "")
            if self.name == "":
                raise AttributeError("missing metric __name__")

            self.labels = dict()
            for label, value in from_prom.get("metric", {}).items():
                if label != "__name__":
                    self.labels[label] = value

            _data = list()
            _index = list()
            if from_prom.get("value") is not None:
                if (
                    not isinstance(from_prom.get("value"), list)
                    or len(from_prom.get("value", [])) != 2
                ):
                    raise ValueError(
                        f"metric value is not right {from_prom.get('value')}. "
                        f"It should be an array with a timestamp and a value."
                    )
                _index.append(from_prom.get("value", [])[0])
                _data.append(float(from_prom.get("value", [])[1]))
            elif from_prom.get("values") is not None:
                for value in from_prom.get("values", []):
                    if not isinstance(value, list) or len(value) != 2:
                        raise ValueError(
                            f"metric value is not as expected {value}"
                        )
                    _index.append(value[0])
                    _data.append(float(value[1]))
            else:
                raise AttributeError("missing metric value(s)")

            if len(_data) == 0 or len(_index) == 0:
                raise ValueError("metric value can't be empty")

            self.data = pd.Series(
                data=_data, index=pd.to_datetime(_index, unit="s")
            )

        elif name is not None:
            # Construct from raw data
            self.name = name
            if self.name == "":
                raise AttributeError("missing metric __name__")

            self.labels = labels

            if values is None:
                raise AttributeError("missing metric value(s)")
            if values.size == 0:
                raise ValueError("metric value can't be empty")
            self.data = values

        else:
            # Construct from nothing
            raise AttributeError("missing data to construct FeliTS")

    def __repr__(self) -> str:
        return (
            f"FeliTS({self.name}{{{self.labels_string}}}, "
            f"{self.size} datapoints)"
        )

    @property
    def labels_string(self) -> str:
        """The labels as a string, as Prometheus would represent it

        Returns:
            str: all the labels as a key-value list, separated with commas
        """
        _labels = list()
        if hasattr(self, "labels") and self.labels is not None:
            for k, v in self.labels.items():
                _labels.append(f'{k}="{v}"')

        return ", ".join(_labels)

    @property
    def frequency(self) -> dt.timedelta:
        """Expose the main frequency in the timeseries. In case there are
            multiple frequencies, the most frequent is returned.

        Returns:
            dt.timedelta: the duration between 2 data points
                or None for single value serie
        """
        if self.data.size <= 1:
            return dt.timedelta()

        # round the timestamp to the second, then calculate time delta between
        # every 2 points, then count all the different deltas, and count
        # results
        frequencies = (
            self.data.index.floor("s").diff().value_counts()  # type: ignore
        )

        if frequencies.size == 1:
            # only one frequency: return it
            return frequencies.idxmax()
        elif frequencies.size > 1:
            # multiple frequencies: return the lowest one that is occuring
            # more than 10% of the time
            for i in range(frequencies.size):
                if (frequencies / self.data.size).sort_index().iloc[
                    i
                ] > MIN_FREQUENCY_REPRESENTATION:
                    return frequencies.sort_index()[i:].idxmax()

        # all other cases seem wrong
        return dt.timedelta()

    @property
    def size(self) -> int:
        """Expose the size to the timeseries

        Returns:
            int: Size of the timeseries
        """
        return self.data.size

    def as_prometheus(self, timestamp_format: str = "s") -> str:
        """Object representation based on Prometheus API format

        Args:
            timestamp_format (str, optional): Format of the timestamps. Could
                be 's' for seconds or 'ms' for milliseconds.
                Defaults to 's'.

        Returns:
            str: JSON representation of the object, as you could push it
                to Prometheus
        """
        return json.dumps(self.as_dict(timestamp_format=timestamp_format))

    def as_dict(self, timestamp_format: str = "s") -> dict:
        """Object representation as a Dictionary

        Args:
            timestamp_format (str, optional): Format of the timestamps. Could
                be 's' for seconds or 'ms' for milliseconds.
                Defaults to 's'.

        Returns:
            dict: representation of the object

        Raises:
            ValueError if the timestamp_format argument is not "s" or "ms"
        """
        result = dict()

        if timestamp_format == "s":
            timestamp_factor = 1
        elif timestamp_format == "ms":
            timestamp_factor = 1000
        else:
            raise ValueError("timestamp_format should be 's' or 'ms'")

        result["metric"] = {"__name__": self.name}

        for k, v in self.labels.items():
            result["metric"][k] = v

        result["values"] = self.data.to_list()  # type: ignore
        result["timestamps"] = (
            (
                pd.Series(data=self.data.index) - dt.datetime(1970, 1, 1)
            )  # type: ignore
            .dt.total_seconds()
            .apply(lambda x: x * timestamp_factor)
            .astype(int)
            .to_list()
        )

        return result

    def as_dataframe(self, name: str = "") -> pd.DataFrame:
        """self.data representation as a pandas.DataFrame

        Args:
            name (str, optional): Name of the column for the Serie in the
                resulting DataFrame. Defaults to self.name.

        Returns:
            pandas.DataFrame: The self.data, as a pandas.DataFrame
        """
        colname = self.name if name == "" else name
        return self.data.to_frame(name=colname)

    def trim_by_date(
        self,
        boundary: dt.datetime = None,
        keep: str = "right",
        inplace: bool = False,
    ) -> pd.Series:
        """Trim the timeseries by date

        Args:
            boundary (dt.datetime, optional): Limit on which triming the
                timeserie. Defaults to None.
            keep (str, optional): Which part of the timeseries to keep.
                Defaults to right.
            inplace (bool, optional): Control if the trim should be applied
                to the current object, or just get the trimmed timeserie.
                Defaults to False.

        Returns:
            pd.Series: The trimmed timeseries

        Raises:
            ValueError if the keep argument is not "left" or "right"
        """
        if keep == "right":
            criteria = self.data.index < boundary
        elif keep == "left":
            criteria = self.data.index > boundary
        else:
            raise ValueError("keep should be 'left' or 'right'")

        if inplace:
            self.data = self.data[~(criteria)]
            return self.data

        return self.data[~(criteria)]

    def trim_by_size(
        self,
        boundary: int = 0,
        keep: str = "right",
        inplace: bool = False,
    ) -> pd.Series:
        """Trim the timeseries by size

        Args:
            boundary (int, optional): Size of the trimmed timeserie. If the
                boundary is 0, keep the whole timeserie.
                Defaults to 0.
            keep (str, optional): Which part of the timeseries to keep.
                Defaults to right.
            inplace (bool, optional): Control if the trim should be applied
                to the current object, or just get the trimmed timeserie.
                Defaults to False.

        Returns:
            pd.Series: The trimmed timeseries

        Raises:
            ValueError if the keep argument is not "left" or "right"
        """
        if boundary > self.data.size or boundary == 0:
            return self.data
        if keep == "right":
            if inplace:
                self.data = self.data[-boundary:]
            return self.data[-boundary:]
        elif keep == "left":
            if inplace:
                self.data = self.data[:boundary]
            return self.data[:boundary]
        else:
            raise ValueError("keep should be 'left' or 'right'")

    def plot(self) -> None:
        """Plot a timeserie"""
        plt.plot(
            self.data.index.to_list(),
            self.data.to_list(),
            label=self.name,
            linestyle="solid",
        )
        plt.xticks(rotation=60, fontsize=10)
        plt.title(f"{self.name}{{{self.labels_string}}}")
        plt.show()
        plt.close()

    def normalize(self, inplace: bool = False) -> pd.Series:
        """Normalize the timeserie, filling missing points with NaN values
        but making sure the index respect the frequency.

        Important: points not aligned on the frequency will be dropped, while
            missing points on frequency will be added as NaN

        Args:
            inplace (bool, optional): Control if the trim should be applied
                to the current object, or just get the trimmed timeserie.
                Defaults to False.

        Returns:
            pd.Series: The normalized timeserie

        Raises:
            ValueError if the timeserie has no frequency (such as single point
                timeserie)

        """
        if self.frequency == dt.timedelta():
            raise ValueError("Can't determine frequency")

        if inplace:
            self.data = self.data.asfreq(freq=self.frequency)
            return self.data

        return self.data.asfreq(freq=self.frequency)

    def longest_continuous_segment(self, position: str = "last") -> pd.Series:
        """Extract the longest continuous segment, which is the longest
            segment of the timeserie respecting the frequency, without any
            missing point

            DEPRECATED: use `continuous_segment` function instead

        Args:
            position (str, optional): Which longest segment to return, in case
                multiple segment exist
                Defaults to last.

        Returns:
            pd.Series: the extract of the timeserie

        Raises:
            ValueError if the position argument is not "first" or "last"
        """
        # validate arguments
        if position not in ["first", "last"]:
            raise ValueError(
                f"position argument must be 'first' or 'last', not {position}"
            )

        return self.continuous_segment(position=position, longest=True)

    def continuous_segment(
        self, position: str = "last", longest: bool = False
    ) -> pd.Series:
        """Extract continuous segment from the timeserie respecting the
            frequency, without any missing point. This segment can be the
            longest, or any length, but it has to be eother the first segment
            or the last from the timeserie.

        Args:
            position (str, optional): Which longest segment to return, in case
                multiple segment exist
                Defaults to last.
            longest (bool, optional): Should the segment be the longest
                Defaults to False.

        Returns:
            pd.Series: the extract of the timeserie

        Raises:
            ValueError if the position argument is not "first" or "last"
        """
        # validate arguments
        if position not in ["first", "last"]:
            raise ValueError(
                f"position argument must be 'first' or 'last', not {position}"
            )

        # case of series with maximum 2 points
        if self.size <= 2:
            return self.data

        # create an array stating if two points are separated by
        # exactly 1 frequency
        segments = self.data.index.diff() == self.frequency  # type: ignore

        # estimate the size of the longest segment matching the frequency
        longest_length = max(
            len(list(y)) if is_freq else 0
            for (is_freq, y) in itertools.groupby(segments)
        )

        # finding the position of the longest segment (first or last)
        start_position = 0
        end_position = 0
        cursor = 0
        for is_freq, segment in itertools.groupby(segments):
            local_segment = list(segment)
            # case where the frequency matches and the length of
            # the segment is the longest
            if is_freq and (
                (longest and len(local_segment) == longest_length)
                or (not longest)
            ):
                start_position = cursor
                end_position = start_position + len(local_segment)

                # in case we found the first longest segment
                if position == "first":
                    break

            # move current cursor along the serie
            cursor += len(local_segment)

        return self.data.iloc[start_position - 1 : end_position]  # noqa E203
