# The Arrew theorem prover

Arrew (ARrow REWriter) is a computer program that allows formal mathematical systems to be expressed, along with the derivation of theorems.

The syntax of specifying axioms is as follows:

```
a<name> : <term>
```

The syntax of specifying rules is as follows:

```
r<name> : <expr> -> <expr> -> ... -> <expr>
```

Any lowercase character in a rule expression is considered a variable and will be used to match and substitute within the subsequent expressions.

All expressions but the last are considered the hypothesis (arguments to be passed when used in a theorem), and the last one is considered the conclusion

The syntax of specifying theorems is as follows:

```
t<name> : <ruleN> <x=X;y=Y;...> <arg1> <arg2> ... <argn>
```

In this case, to `<ruleN>` will be applied the corresponding arguments. Substitution (`x` with `X`, `y` with `Y`...) will be done in both the rule's provided arguments and the theorem's hypotheses, and they will be matched/unified. If unification was successful, the final argument in the rule `argn` will be produced as a result.

As an example, consider a simple formal system:

```
a1 : MI

r1 : xI -> xIU
r2 : Mx -> Mxx
r3 : xIIIy -> xUy
```

We specify a single axiom (term) `MI` and three rules that allow transforming axioms to derive new theorems. Consider the following theorems:

```
t1 : r2 x=I a1
# t1 will be equal to `MII` since the expression `Mx` captures `MI` (note `x` is a variable). The expression `x` will be substituted with the expression `I`.
t2 : r2 x=II t1
# Similarly, t2 will be equal to `MIIII` following the previous reasoning
t3 : r3 x=M,y=I t2
# Since `MIIII` is captured by the rule's `xIIIy` set `x` to `M` and `y` to `I`. Then, `xUy` becomes `MUI`
```

Note that Arrew is a simple language: it doesn't directly support terms (so they have to be defined in terms of axioms). See [Peano's axioms](./peano.arw) as an example; to derive the theorems, run `python3 arrew.py peano.arw`.

## Development

Install `pre-commit` and configure it once you clone this repo:

```
$ pip3 install pre-commit
$ pre-commit install
```
