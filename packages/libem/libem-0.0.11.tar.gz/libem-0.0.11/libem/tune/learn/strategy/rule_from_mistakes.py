import libem
from libem.core import model
import libem.core.util as libem_util
from libem.core.struct import Prompt

from libem.tune.learn import prompt, parameter
from libem.tune.learn.function import predict

import pprint as pp


def run(dataset, metric) -> tuple[float, Prompt.Rule, Prompt.Experience]:
    preds, truths, mistakes, successes = predict(dataset)
    metric_func = libem_util.get_func(metric)
    score = metric_func(preds, truths)

    libem.info("Tool: learn - metric:", metric, "score:", score)

    # if lots of mistakes, learn from rules
    rule, experience = Prompt.Rule(), Prompt.Experience()
    if score < 0.25:
        rule = rule_from_success(mistakes)
    else:
        experience = experience_from_mistake(mistakes)
    return score, rule, experience


def rule_from_success(successes: list) -> Prompt.Rule:
    libem.info("Successes: ", pp.pformat(successes))
    message = model.call(
        prompt=Prompt.join(
            prompt.recap_success(successes=successes),
            prompt.gen_rules(),
        ),
        model=parameter.model(),
        temperature=parameter.temperature(),
        seed=libem.LIBEM_SEED,
        tools=[],
    )
    libem.info("Learned: ", message)
    rules = message.split("\n")
    return Prompt.Rule(rules)


def experience_from_mistake(mistakes: list) -> Prompt.Experience:
    libem.info("Mistakes: ", pp.pformat(mistakes))
    message = model.call(
        prompt=Prompt.join(
            prompt.recap_mistake(mistakes=mistakes),
            prompt.gen_rules(),
        ),
        model=parameter.model(),
        temperature=parameter.temperature(),
        seed=libem.LIBEM_SEED,
        tools=[],
    )
    libem.info("Learned: ", message)
    mistakes = message.split("\n")
    return Prompt.Experience(mistakes)
