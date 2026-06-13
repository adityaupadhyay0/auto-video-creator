# LaTeX Glossary

Pre-verified MathTex strings. Copy exactly — these render without error in Manim CE ≥0.18.

All strings use raw string syntax `r"..."`. Do not convert to f-strings.

---

## Calculus

```python
# Derivative (limit definition)
MathTex(r"f'(x) = \lim_{\Delta x \to 0} \frac{f(x + \Delta x) - f(x)}{\Delta x}")

# Derivative (Leibniz notation)
MathTex(r"\frac{dy}{dx}")
MathTex(r"\frac{d}{dx}\left[f(x)\right]")

# Power rule
MathTex(r"\frac{d}{dx}\left[x^n\right] = nx^{n-1}")

# Chain rule
MathTex(r"\frac{dy}{dx} = \frac{dy}{du} \cdot \frac{du}{dx}")

# Product rule
MathTex(r"(fg)' = f'g + fg'")

# Definite integral
MathTex(r"\int_a^b f(x)\, dx")

# Fundamental theorem
MathTex(r"\int_a^b f'(x)\, dx = f(b) - f(a)")

# Limit notation
MathTex(r"\lim_{x \to a} f(x) = L")
MathTex(r"\lim_{x \to \infty} f(x)")

# Partial derivative
MathTex(r"\frac{\partial f}{\partial x}")
```

---

## Algebra & Arithmetic

```python
# Quadratic formula
MathTex(r"x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}")

# Binomial expansion
MathTex(r"(a + b)^2 = a^2 + 2ab + b^2")

# Slope-intercept
MathTex(r"y = mx + b")

# Point-slope
MathTex(r"y - y_1 = m(x - x_1)")

# Pythagorean theorem
MathTex(r"a^2 + b^2 = c^2")

# Absolute value
MathTex(r"|x| = \begin{cases} x & x \geq 0 \\ -x & x < 0 \end{cases}")
```

---

## Linear Algebra

```python
# Matrix (2x2)
MathTex(r"\begin{pmatrix} a & b \\ c & d \end{pmatrix}")

# Determinant
MathTex(r"\det(A) = ad - bc")

# Dot product
MathTex(r"\vec{u} \cdot \vec{v} = |\vec{u}||\vec{v}|\cos\theta")

# Matrix multiplication hint
MathTex(r"(AB)_{ij} = \sum_k A_{ik} B_{kj}")
```

---

## Statistics & Probability

```python
# Mean
MathTex(r"\bar{x} = \frac{1}{n}\sum_{i=1}^{n} x_i")

# Standard deviation
MathTex(r"\sigma = \sqrt{\frac{1}{n}\sum_{i=1}^{n}(x_i - \bar{x})^2}")

# Normal distribution
MathTex(r"f(x) = \frac{1}{\sigma\sqrt{2\pi}} e^{-\frac{(x-\mu)^2}{2\sigma^2}}")

# Bayes' theorem
MathTex(r"P(A|B) = \frac{P(B|A)\,P(A)}{P(B)}")

# Binomial probability
MathTex(r"P(X=k) = \binom{n}{k} p^k (1-p)^{n-k}")
```

---

## Physics

```python
# Newton's second law
MathTex(r"F = ma")

# Kinematic equation
MathTex(r"v = v_0 + at")
MathTex(r"x = x_0 + v_0 t + \frac{1}{2}at^2")

# Einstein mass-energy
MathTex(r"E = mc^2")

# Wave equation
MathTex(r"v = f\lambda")

# Ohm's law
MathTex(r"V = IR")
```

---

## Common Symbols and Notation

```python
# Set membership
MathTex(r"x \in \mathbb{R}")

# For all / there exists
MathTex(r"\forall x \in \mathbb{R},\; f(x) \geq 0")
MathTex(r"\exists x : f(x) = 0")

# Implies / iff
MathTex(r"A \implies B")
MathTex(r"A \iff B")

# Summation
MathTex(r"\sum_{i=1}^{n} i = \frac{n(n+1)}{2}")

# Product notation
MathTex(r"\prod_{i=1}^{n} i = n!")

# Infinity
MathTex(r"\infty")
MathTex(r"[0, \infty)")

# Vectors
MathTex(r"\vec{v} = \langle v_1, v_2, v_3 \rangle")

# Greek letters (commonly used)
# α β γ δ ε ζ η θ ι κ λ μ ν ξ π ρ σ τ φ χ ψ ω
MathTex(r"\alpha, \beta, \gamma, \delta")
MathTex(r"\epsilon, \theta, \lambda, \mu")
MathTex(r"\pi, \sigma, \tau, \phi, \omega")
```

---

## Multi-Line Alignment (use for derivation steps)

```python
# Aligned environment for step-by-step derivations
MathTex(r"""
\begin{aligned}
f'(x) &= \lim_{\Delta x \to 0} \frac{f(x+\Delta x) - f(x)}{\Delta x} \\
      &= \lim_{\Delta x \to 0} \frac{(x+\Delta x)^2 - x^2}{\Delta x} \\
      &= \lim_{\Delta x \to 0} \frac{2x\Delta x + (\Delta x)^2}{\Delta x} \\
      &= \lim_{\Delta x \to 0} (2x + \Delta x) \\
      &= 2x
\end{aligned}
""", font_size=36)
```

Note: Multi-line MathTex can be large. Check occupancy and scale if needed:
```python
formula = MathTex(r"...", font_size=36)
if formula.height > 4.0:
    formula.scale_to_fit_height(3.5)
```
