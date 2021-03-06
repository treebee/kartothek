from functools import partial

import pytest

from kartothek.io.dask.delayed import (
    read_dataset_as_delayed,
    read_dataset_as_delayed_metapartitions,
    read_table_as_delayed,
)
from kartothek.io.testing.read import *  # noqa


@pytest.fixture(params=["dataframe", "metapartition", "table"])
def output_type(request):
    return request.param


def _load_dataframes(output_type, *args, **kwargs):
    if output_type == "dataframe":
        func = read_dataset_as_delayed
    elif output_type == "metapartition":
        func = read_dataset_as_delayed_metapartitions
    elif output_type == "table":
        if "tables" in kwargs:
            kwargs.pop("tables")
        func = partial(read_table_as_delayed, table="core")
    tasks = func(*args, **kwargs)
    result = [task.compute() for task in tasks]
    return result


@pytest.fixture()
def bound_load_dataframes(output_type):
    return partial(_load_dataframes, output_type)
