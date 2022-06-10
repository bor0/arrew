# The Arrew theorem prover

Arrew (ARrow REWriter) is a computer program that allows expressing formal systems and deriving theorems.

## Syntax

Every statement in an Arrew code is of the form:

```
r<name> : <expr> [-> <expr> -> ... -> <expr>]
t<name> : <ruleN> [x=X;y=Y;...] [arg1] [arg2] [...] [argn]
```

The syntax for `<name>` and `<expr>` is any string of characters except `':'` and `' '` (whitespace). Square brackets represent optional values.

Lowercase characters in a rule expression are considered a variable and will be used for substitution within the expressions.

## Semantics

The syntax `r<name>` specifies a rule, and `t<name>` specifies a theorem.

In a rule, all expressions but the last are considered the hypothesis (arguments to be passed when used in a theorem), and the last is the conclusion.

For theorems, the rule `<ruleN>` will be applied to the corresponding arguments. Substitution (`x` with `X`; `y` with `Y`...) will be performed in both the rule's hypotheses and the theorem's provided argument, and they will be matched/unified. If unification is successful, the final argument in the rule `argn` will be the result.

Arrew will print all derived theorems except those whose name ends in a `!`.

## Example

As an example, consider a simple formal system:

```
rMI : MI
thMI! : ra1

r1 : xI -> xIU
r2 : Mx -> Mxx
r3 : xIIIy -> xUy
```

The rule `rMI` specifies the axiom `MI` (converted into theorem `thMI!`). The remaining three rules allow transforming this rule to derive new theorems. Consider the following theorems:

```
t1 : r2 x=I thMI!
# t1 will be equal to `MII` since the expression `Mx` captures `MI` (note `x` is a variable). `x` is substituted with `I`
t2 : r2 x=II t1
# Similarly, t2 will be equal to `MIIII` following the previous reasoning
t3 : r3 x=M,y=I t2
# Since `MIIII` is captured by the rule's `xIIIy` set `x` to `M` and `y` to `I`. Then, `xUy` becomes `MUI`
```

See [Peano's axioms](./examples/peano.arw) for a more detailed example; to derive the theorems, run `python3 arrew.py examples/peano.arw`.

## Development

Install `pre-commit` and configure it once you clone this repo:

```
$ pip3 install pre-commit
$ pre-commit install
```
