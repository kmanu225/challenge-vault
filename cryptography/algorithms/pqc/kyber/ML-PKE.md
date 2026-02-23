# Kyber: ML-PKE (With Ciphertext Compression and Matrix Optimization)

This document outlines the **optimized Key Generation, Encryption, and Decryption** algorithms for the **Kyber-based Multi-Level Public Key Encryption (ML-PKE)** scheme. This version includes:

- **Matrix $\mathbf{A}$ generation from a 256-bit seed**
- **Ciphertext compression and decompression**

## Notation

- $n$: Degree of polynomials  
- $q$: Modulus  
- $k$: Security parameter  
- $\chi$: Noise distribution  
- $\mathcal{R}_q = \mathbb{Z}_q[X]/(X^n + 1)$  
- $d_u$, $d_v$: Compression bit-widths for $\mathbf{u}$ and $\mathbf{v}$ respectively  
- $\texttt{G}$: Public matrix generation function (e.g., XOF like SHAKE128)

Vectors and matrices of polynomials are denoted in bold (e.g., $\mathbf{a}$, $\mathbf{s}$).

## 1. Key Generation

**Input**: Security parameter $k$  
**Output**: Public key $(\rho, \mathbf{t})$, Secret key $\mathbf{s}$

### ✦ Optimization: Generate $\mathbf{A}$ from Seed $\rho$

Instead of storing the full matrix $\mathbf{A}$, we use a **public seed** $\rho \in \{0,1\}^{256}$ and generate $\mathbf{A}$ deterministically with a cryptographic hash function:

```math
\mathbf{A} = G(\rho)
```

1. Sample random 256-bit seed $\rho \in \{0,1\}^{256}$  
2. Compute matrix $\mathbf{A} = G(\rho)$ deterministically from $\rho$  
3. Sample secret vector $\mathbf{s} \leftarrow \chi^k$  
4. Sample error vector $\mathbf{e} \leftarrow \chi^k$  
5. Compute:

```math
   \mathbf{t} = \mathbf{A} \cdot \mathbf{s} + \mathbf{e} \mod q
```

6. Output:

   - Public key: $(\rho, \mathbf{t})$
   - Secret key: $\mathbf{s}$

## 2. Encryption

**Input**: Public key $(\rho, \mathbf{t})$, message $\mu \in \{0,1\}^n$  
**Output**: Compressed ciphertext $(\hat{\mathbf{u}}, \hat{\mathbf{v}})$

1. Recompute $\mathbf{A} = G(\rho)$ using the public seed  
2. Sample ephemeral secret $\mathbf{r} \leftarrow \chi^k$  
3. Sample error vectors $\mathbf{e}_1 \leftarrow \chi^k$, $e_2 \leftarrow \chi$  
4. Encode message $\mu$ into polynomial $m \in \mathcal{R}_q$  
5. Compute:

```math
   \mathbf{u} = \mathbf{A}^T \cdot \mathbf{r} + \mathbf{e}_1 \mod q
```

```math
   \mathbf{v} = \mathbf{t}^T \cdot \mathbf{r} + e_2 + m \cdot \left\lfloor \frac{q}{2} \right\rfloor \mod q
```

6. **Compress ciphertext**:
   - For $x$ in $\mathbf{u}$:  

```math
     \hat{x} = \text{Compress}_q(x, d_u) = \left\lfloor \frac{x \cdot 2^{d_u}}{q} \right\rfloor
```

- For $x$ in $\mathbf{v}$:  

```math
     \hat{x} = \text{Compress}_q(x, d_v) = \left\lfloor \frac{x \cdot 2^{d_v}}{q} \right\rfloor
```

7. Output: $(\hat{\mathbf{u}}, \hat{\mathbf{v}})$

## 3. Decryption

**Input**: Secret key $\mathbf{s}$, compressed ciphertext $(\hat{\mathbf{u}}, \hat{\mathbf{v}})$  
**Output**: Message $\mu \in \{0,1\}^n$

### Decompression

- For $x$ in $\hat{\mathbf{u}}$:  

```math
  x \gets \text{Decompress}_q(x, d_u) = \left\lfloor \frac{q \cdot x}{2^{d_u}} \right\rfloor
```

- For $x$ in $\hat{\mathbf{v}}$:  

```math
  x \gets \text{Decompress}_q(x, d_v) = \left\lfloor \frac{q \cdot x}{2^{d_v}} \right\rfloor
```

### Symmetric Modular Reduction

Used to map coefficients to a centered range:

```math
\text{SymmetricMod}_q(x) = x - q \cdot \left\lfloor \frac{x}{q} + \frac{1}{2} \right\rfloor
```

### Rounding Function

```math
\text{Round}_q(x) = 
\begin{cases}
0, & \text{if } \text{SymmetricMod}_q(x) \in \left[ -\frac{q}{4}, \frac{q}{4} \right] \\
1, & \text{otherwise}
\end{cases}
```

1. Decompress $\hat{\mathbf{u}}$ and $\hat{\mathbf{v}}$ into $\mathbf{u}$ and $\mathbf{v}$  
2. Compute:

```math
   m' = \mathbf{v} - \mathbf{u}^T \cdot \mathbf{s} \mod q
```

3. For each coefficient $m'_i$:
   - Apply symmetric reduction: $m'_i \gets \text{SymmetricMod}_q(m'_i)$  
   - Recover bit: $\mu_i = \text{Round}_q(m'_i)$  
4. Output: $\mu = (\mu_0, \mu_1, \dots, \mu_{n-1})$

### ⚠️ Note on Decompression Accuracy

Decompression is inherently lossy: the original polynomial coefficients are quantized into fewer bits during compression, and exact reconstruction is not guaranteed after decompression.
However, Kyber’s parameters are chosen such that:

- The decompressed values are statistically close enough to the originals.
- The decryption and rounding operations are highly likely to still recover the correct message bits.
- The failure probability is negligible under chosen parameters (e.g., less than $2^{-100}$).

As a result, decryption succeeds with overwhelming probability in practice — even though it's not information-theoretically perfect.
