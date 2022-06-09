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

## Mathematics

A formal system is defined by the tuple $F = (R_n, E, V, T)$ with the functions $s_r$ and $s_t$ where:

- $E$ is the set of valid expressions. E.g. $\texttt{A+B} \in E$.
- $V$ is the set of variables. E.g. $x \in V, y \in V, \ldots$
- $R_n$ is the set of rules of $n$-ary arguments, where the $n$-th argument represents a conclusion, and the others represent hypotheses. E.g. $\texttt{(Z)} \in R_1$ is used to express the idea of "zero". Another example: $\texttt{(x, Sx)} \in R_2$ expresses the idea of "successor".
- $T$ is the set of theorems.

Further, let $r \in R_n$, $v \subseteq V \times E$. Also, let $X[E/V]$ be the expression $X$ in which each occurrence of $V$ is replaced with $E$. The following function performs substitution on a rule's hypotheses and conclusion:

$$ s_r(r, v) = {
\begin{cases}
s_r(r_1[E/V], \ldots, r_n[E/V], v \setminus \{(V, E) \}),  & r = (r_1, \ldots, r_n) \land (V, E) \in v \\
r & v = \emptyset
\end{cases}}
$$

Let $h = (h_1, \ldots, h_{n-1})$ where $\forall i, h_i \in T$, that is, every hypothesis represents a theorem. The following function performs substitution on a theorem's hypotheses:

$$ s_t(h, v) = {
\begin{cases}
s_t(h_1[E/V], \ldots, h_{n-1}[E/V], v \setminus \{(V, E) \}),  & h = (h_1, \ldots, h_{n-1}) \land (V, E) \in v \\
h & v = \emptyset
\end{cases}}
$$

To produce a new theorem, consider applying the rule $r = (r_1, \ldots, r_n) \in R_n$, together with the set of substitutions $v \subseteq V \times E$ and a sequence of hypotheses $h = (h_1, \ldots, h_{n-1})$ where $\forall i, h_i \in T$. We say that $t = s_r((r_n),v) \in T$ (that is, $t$ is a theorem) if and only if:

$$
s_r((r_1, \ldots, r_{n-1}), v) = s_t(h, v) \land r = (r_1, \ldots, r_n) \land h = (h_1, \ldots, h_{n-1}) \land (V, E) \in v
$$

Corollary: By letting $n = 1$, we have:

$$
s_r((), v) = s_t((), v) \land (V, E) \in v
$$

That is, $\forall r, r \in R_1 \to r \in T$, i.e., all 1-ary rules are theorems.

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

See [Peano's axioms](./peano.arw) for a more detailed example; to derive the theorems, run `python3 arrew.py peano.arw`.

## Development

Install `pre-commit` and configure it once you clone this repo:

```
$ pip3 install pre-commit
$ pre-commit install
```
