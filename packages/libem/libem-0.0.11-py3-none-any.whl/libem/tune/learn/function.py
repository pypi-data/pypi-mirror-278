import typing

import libem
import libem.core.util as libem_util
from libem.tune.learn import prompt, parameter

from libem.tune.learn import strategy as strategy_lib

schema = {}


def func(*args, **kwargs):
    return learn(*args, **kwargs)


def learn(dataset: list | typing.Iterable,
          metric: str = "libem.core.eval.f1",
          strategy=parameter.strategy()):
    match strategy:
        case "random_shots":
            return strategy_lib.random_shots.run(dataset, metric)
        case "similar_shots":
            return strategy_lib.similar_shots.run(dataset, metric)
        case "rule-from-mistake":
            return strategy_lib.rule_from_mistakes.run(dataset, metric)
        case "attentive-retrain":
            return strategy_lib.attentive_retrain.run(dataset, metric)
        case _:
            raise ValueError(f"Invalid strategy: {strategy}")


def predict(dataset) -> tuple[list, list, list, list]:
    preds, truths = [], []
    mistakes, successes = [], []

    for i, record in enumerate(dataset):
        left, right, truth = record["left"], record["right"], record["label"]

        pred = libem.match(left, right)
        libem.info("Tool: learn - record:", i, "pred:", pred, "true:", truth)

        preds.append(1 if pred.lower() == "yes" else 0)
        truths.append(truth)

        truth = "yes" if truth == 1 else "no"
        outcome = {
            "entity 1": left,
            "entity 2": right,
            "your answer": pred,
            "true answer": truth,
        }

        if pred == truth:
            successes.append(outcome)
        else:
            mistakes.append(outcome)
    return preds, truths, mistakes, successes


def check(dataset, metric: str = "libem.core.eval.f1") -> tuple[float, list]:
    preds, truths, mistakes, successes = predict(dataset)
    metric_func = libem_util.get_func(metric)
    score = metric_func(preds, truths)

    libem.info("Tool: check - metric:", metric, "score:", score)
    return score, mistakes
