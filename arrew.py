#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import re
from os.path import exists


def rule_to_regex(rule):
    regex = r'^'

    for i in range(0, len(rule)):
        if rule[i].islower():
            regex += '(?P<%s_%d>.+)' % (rule[i], i)
        else:
            regex += re.escape(rule[i])

    regex += '$'

    return re.compile(regex)


def parse_rules(rules):
    parsed_rules = {}

    for name in rules:
        rule = list(map(str.strip, rules[name].split("->")))
        parsed_rules[name] = {"hypotheses": list(
            map(rule_to_regex, rule[:-1])), "conclusion": rule[-1]}

    return parsed_rules


def calc_env(code):
    env = {"axioms": {}, "rules": {}, "theorems": {}}
    types = {"a": "axioms", "r": "rules", "t": "theorems"}

    code = filter(lambda x: x, code.split("\n"))
    code = filter(lambda x: x, map(
        lambda line: line.split("#")[0], code))  # strip comments

    for line in code:
        spl = list(filter(lambda x: x, map(str.strip, line.split(":"))))

        if len(spl) != 2:
            raise Exception("Invalid syntax: %s" % line)

        [name, expr] = spl

        if name[0] in types:
            ty = types[name[0]]
        else:
            raise Exception("Invalid variable name: %s" % name)

        env[ty][name] = expr

    env["rules"] = parse_rules(env["rules"])

    return env


def unify_matches(matches):
    unified = {}
    keys = list(map(lambda x: [x] + [x.split('_')[0]], list(matches.keys())))

    for [key, group] in keys:
        if group not in unified:
            unified[group] = matches[key]
        elif unified[group] != matches[key]:
            raise Exception("Mismatch for variable '%s', expected '%s' but got '%s'" % (
                group, unified[group], matches[key]))

    return unified


def apply_rule(
    env,
    rule,
    axioms,
    name,
):
    all_matches = {}
    rule = env["rules"][rule]
    hypotheses = rule["hypotheses"]

    # Match every axiom (parameter) with the rule's hypotheses

    for axiom in axioms:
        if axiom not in env["axioms"] and axiom not in env["theorems"]:
            raise Exception("Invalid axiom/theorem: '%s'" % axiom)

        if len(hypotheses) == 0:
            raise Exception(
                "Mismatch between number of hypotheses and rule arguments: '%s'" % name
            )

        axiom = (
            env["axioms"][axiom] if axiom in env["axioms"] else env["theorems"][axiom]
        )
        (hypothesis, hypotheses) = (hypotheses[0], hypotheses[1:])

        matches = hypothesis.search(axiom)
        if matches == None:
            continue

        matches = matches.groupdict()

        if len(matches) == 0:
            raise Exception(
                "Rule does not match the hypothesis: '%s' ('%s')" % (
                    name, axiom)
            )

        matches = unify_matches(matches)

        for key in matches:
            if not key.islower():  # lowercase are variables
                continue

            if key in all_matches and all_matches[key] != matches[key]:
                raise Exception(
                    "Rule value mismatch. In '%s', for variable '%s' expected '%s' but got '%s'"
                    % (name, key, all_matches[key], matches[key])
                )

            all_matches[key] = matches[key]

    if len(hypotheses) != 0:
        raise Exception(
            "Mismatch between number of hypotheses and rule arguments: '%s'" % name
        )

    axiom = rule["conclusion"]

    # Perform replacement
    for variable in all_matches:
        replacement = all_matches[variable]
        axiom = axiom.replace(variable, replacement)

    return axiom


if len(sys.argv) != 2:
    exit("Usage: python %s <filename.arw>" % sys.argv[0])

if not exists(sys.argv[1]):
    exit("Filename %s not found." % sys.argv[0])

with open(sys.argv[1]) as f:
    code = f.read()

try:
    env = calc_env(code)

    for name in env["theorems"]:
        axioms = env["theorems"][name].split(" ")
        (rule, axioms) = (axioms[0], axioms[1:])
        env["theorems"][name] = apply_rule(env, rule, axioms, name)
except Exception as e:
    exit(e)

for name in env["theorems"]:
    print("%s : %s" % (name, env["theorems"][name]))
