"""
Attentive Shots

1. Training pass: Identify and record errors from the first training pass,
   labeling these as "mistakes."
2. Chain of thought retraining: Apply a chain-of-thought prompting to retrain
   Libem on just the mistakes, marking successfully resolved instances as "corrected."
3. Few-shot prompting: Use the corrected examples to enhance the few-shot learning prompts,
   improving model training and generalization.
"""

import libem
from libem.core import model
import libem.core.util as libem_util
from libem.core.struct import Prompt

from libem.tune.learn import prompt, parameter
from libem.tune.learn import predict

import pprint as pp


def run(dataset, metric):
    preds, truths, mistakes, successes = predict(dataset)
    metric_func = libem_util.get_func(metric)
    score = metric_func(preds, truths)

    libem.info("Tool: learn - metric:", metric, "score:", score)
    print(mistakes)

    # return the shots

