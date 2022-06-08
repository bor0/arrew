# The Arrew theorem prover

Arrew (ARrow REWriter) is a computer program that allows formal mathematical systems to be expressed, along with the derivation of theorems.

The syntax for specifying axioms is as follows:

```
a<name> : <term>
```

The syntax for specifying rules is as follows:

```
r<name> : <expr> -> <expr> -> ... -> <expr>
```

Lowercase characters in a rule expression are considered a variable, and will be substituted within the expressions.

All expressions but the last are considered the hypothesis (arguments to be passed when used in a theorem), and the last one is the conclusion.

The syntax for specifying theorems is as follows:

```
t<name> : <ruleN> <x=X;y=Y;...> <arg1> <arg2> ... <argn>
```

In this case, the rule `<ruleN>` will be applied to the corresponding arguments. Substitution (`x` with `X`; `y` with `Y`...) will be performed in both the rule's provided arguments and the theorem's hypotheses, and they will be matched/unified. If unification is successful, the final argument in the rule `argn` will be produced as a result.

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
# t1 will be equal to `MII` since the expression `Mx` captures `MI` (note `x` is a variable). The expression `x` will be substituted with the expression `I`
t2 : r2 x=II t1
# Similarly, t2 will be equal to `MIIII` following the previous reasoning
t3 : r3 x=M,y=I t2
# Since `MIIII` is captured by the rule's `xIIIy` set `x` to `M` and `y` to `I`. Then, `xUy` becomes `MUI`
```

See [Peano's axioms](./peano.arw) for a more detailed example; to derive the theorems, run `python3 arrew.py peano.arw`.

## Development

Install `pre-commit` and configure it once you clone this repo:

```
$ pip3 install pre-commit
$ pre-commit install
```
