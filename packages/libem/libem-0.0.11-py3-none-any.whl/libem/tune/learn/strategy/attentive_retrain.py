import libem
from libem.core import model
import libem.core.util as libem_util
from libem.core.struct import Prompt

from libem.tune.learn import prompt, parameter
from libem.tune.learn.function import predict

import pprint as pp


def run(dataset, metric):
    preds, truths, mistakes, successes = predict(dataset)
    metric_func = libem_util.get_func(metric)
    score = metric_func(preds, truths)

    libem.info("Tool: learn - metric:", metric, "score:", score)
    print(mistakes)
