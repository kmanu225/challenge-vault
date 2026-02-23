# Kyber: ML-PKE (Without Optimization)

This document outlines the key generation, encryption, and decryption algorithms for the Kyber-based Multi-Level Public Key Encryption (ML-PKE) scheme, **without any implementation-level optimizations**.

## Notation

- $n$: Degree of polynomials
- $q$: Modulus
- $k$: Security parameter
- $\chi$: Noise distribution
- $\mathcal{R}_q = \mathbb{Z}_q[X]/(X^n + 1)$

Vectors and matrices of polynomials are denoted in bold (e.g., $\mathbf{a}$, $\mathbf{s}$).

## 1. Key Generation

**Input**: Security parameter $k$
**Output**: Public key $(\mathbf{A}, \mathbf{t})$, Secret key $\mathbf{s}$

### Steps

1. Sample $\mathbf{A} \leftarrow \mathcal{R}_q^{k \times k}$ uniformly at random.
2. Sample secret $\mathbf{s} \leftarrow \mathcal{R}_q^{k}$ generated via noise distribution.
3. Sample error $\mathbf{e} \leftarrow \mathcal{R}_q^{k}$ generated via noise distribution.
4. Compute:

```math
\mathbf{t} = \mathbf{A} \cdot \mathbf{s} + \mathbf{e} \mod q
```

5. Output:
   - Public key: $(\mathbf{A}, \mathbf{t})$
   - Secret key: $\mathbf{s}$

## 2. Encryption

**Input**: Public key $(\mathbf{A}, \mathbf{t})$, Message $\mu \in \{0,1\}^n$  
**Output**: Ciphertext $(\mathbf{u}, \mathbf{v})$

### Steps

1. Sample ephemeral secret $\mathbf{r} \leftarrow \chi^k$.
2. Sample errors $\mathbf{e}_1,e_2 \leftarrow \chi$.
3. Encode message $\mu$ into polynomial $m \in \mathcal{R}_q$.
4. Compute:

```math
\mathbf{u} = \mathbf{A}^T \cdot \mathbf{r} + \mathbf{e}_1 \mod q
```

```math
\mathbf{v} = \mathbf{t}^T \cdot \mathbf{r} + e_2 + m \cdot \left\lfloor \frac{q}{2} \right\rfloor \mod q
```

5. Output ciphertext $(\mathbf{u}, \mathbf{v})$

## 3. Decryption

**Input**: Secret key $\mathbf{s}$, Ciphertext $(\mathbf{u}, \mathbf{v})$  
**Output**: Recovered message $\mu$

### Symmetric Modular Reduction

To ensure decryption is accurate, we use **symmetric modular reduction** :

- $\text{SymmetricMod}_q(x) = x - q \cdot \left\lfloor \frac{x}{q} + \frac{1}{2} \right\rfloor$
- This maps values into the symmetric range $\left[ -\frac{q}{2}, \frac{q}{2} \right]$

### Rounding Function

To recover message bits from decrypted polynomial coefficients, we use:

```math
\text{Round}_q(x) = 
\begin{cases}
0, & \text{if } \text{SymmetricMod}_q(x) \in \left[ -\frac{q}{4}, \frac{q}{4} \right] \\
1, & \text{otherwise}
\end{cases}
```

This rounds to the nearest message bit (0 or 1) depending on whether the coefficient is closer to $0$ or $\frac{q}{2}$. We generalize the round function to polynomials by applying it to their coefficients.

### Steps for decription

1. Compute $m' = \mathbf{v} - \mathbf{u}^T \cdot \mathbf{s} \mod q$
2. Apply symmetric modular reduction to all coefficients of $m'_i \gets \text{SymmetricMod}_q(m'_i)$
3. Recover bits using rounding $\mu_i = \text{Round}_q(m'_i)$
4. Output $\mu \in \{0,1\}^n$
