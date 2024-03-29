import csv
import itertools
import os
from collections import defaultdict

from tcv.calculation.powersystemdatamodel.model import LoadResult
from tcv.calculation.powersystemdatamodel.model import NodeResult, Transformer3WResult
from tcv.calculation.powersystemdatamodel.model import Transformer2WResult


class TimeSeriesResult:
    node_results: dict = defaultdict(list)
    load_results: dict = defaultdict(list)
    transformer_2w_results: dict = defaultdict(list)
    transformer_3w_results: dict = defaultdict(list)

    def __new__(cls, *args, **kwargs):
        obj = super().__new__(cls)

        obj.node_results = defaultdict(list)
        obj.load_results = defaultdict(list)
        obj.transformer_2w_results = defaultdict(list)
        obj.transformer_3w_results = defaultdict(list)

        return obj

    def __init__(self, base_directory: str, delimiter: str = ','):
        node_result_file = os.path.join(base_directory, "node_res.csv")
        load_result_file = os.path.join(base_directory, "load_res.csv")
        transformer_2w_result_file = os.path.join(base_directory, "transformer_2_w_res.csv")
        transformer_3w_result_file = os.path.join(base_directory, "transformer_3_w_res.csv")

        # Handling the node results
        with open(node_result_file, mode='r') as node_result_lines:
            for dct in csv.DictReader(node_result_lines, delimiter=delimiter):
                node_result = NodeResult.from_dict(dct)
                self.node_results[node_result.time].append(node_result)

        # Handling the load results
        with open(load_result_file, mode='r') as load_result_lines:
            for dct in csv.DictReader(load_result_lines, delimiter=delimiter):
                load_result = LoadResult.from_dict(dct)
                self.load_results[load_result.time].append(load_result)

        # Handling the two winding transformer results
        if os.path.exists(transformer_2w_result_file):
            with open(transformer_2w_result_file, mode='r') as transformer_2w_lines:
                for dct in csv.DictReader(transformer_2w_lines, delimiter=delimiter):
                    transformer_result = Transformer2WResult.from_dict(dct)
                    self.transformer_2w_results[transformer_result.time].append(transformer_result)

        # Handling the transformer three winding results
        if os.path.exists(transformer_3w_result_file):
            with open(transformer_3w_result_file, mode='r') as transformer_3w_lines:
                for dct in csv.DictReader(transformer_3w_lines, delimiter=delimiter):
                    transformer_result = Transformer3WResult.from_dict(dct)
                    self.transformer_3w_results[transformer_result.time].append(transformer_result)

    def __str__(self):
        return "TimeSeriesResult{node_results=%i,load_results=%i,transformer_2w_results=%i,transformer_3w_results=%i}" % (
            len(list(itertools.chain(*self.node_results.values()))),
            len(list(itertools.chain(*self.load_results.values()))),
            len(list(itertools.chain(*self.transformer_2w_results.values()))),
            len(list(itertools.chain(*self.transformer_3w_results.values()))))

    def join(self, that):
        """
        Join the other results into this one

        :param that: The other result to incorporate
        """
        for time_step, result in that.node_results:
            self.node_results[time_step].append(result)
        for time_step, result in that.load_results:
            self.load_results[time_step].append(result)
        for time_step, result in that.transformer_2w_results:
            self.transformer_2w_results[time_step].append(result)
        for time_step, result in that.transformer_3w_results:
            self.transformer_3w_results[time_step].append(result)
