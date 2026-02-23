# [ECC (Elliptic Curve Cryptography)](https://csrc.nist.gov/projects/elliptic-curve-cryptography)

Elliptic Curve Cryptography (ECC) is an asymmetric cryptographic scheme that uses the mathematical structure of elliptic curves to create secure encryption systems. ECC is known for its high security with relatively small key sizes compared to traditional cryptographic schemes such as RSA. This makes it an efficient choice for modern cryptography, especially in environments with limited resources, such as mobile devices.

## Overview

ECC relies on elliptic curves are defined over finite fields, and cryptographic operations are performed on points that lie on the curve in a Cartesian plane. The difficulty of solving the **Elliptic Curve Discrete Logarithm Problem (ECDLP)** is the basis of ECC’s security, making it resistant to attacks that are efficient on other cryptographic schemes.

## Features of This Repository

This repository provides a simple, illustrative implementation of Elliptic Curve Cryptography using **Weierstrass curves**. It demonstrates several key concepts related to ECC:


### 1. **Weirstrass Elliptic Curves**

This repository includes an implementation of Weierstrass elliptic curves, which are defined by the equation:

$$
y^{2} = x^{3} + ax + b \quad \text{(Weierstrass reduced form)}
$$

where $a$ and $b$ are constants, and the curve is smooth and non-singular when the discriminant $4a3+27b2≠0$.

Key features of this implementation include:

- **Invariant Point at Infinity**: The elliptic curve is equipped with a special point at infinity, often denoted as OO. This point serves as the identity element for the group law of the curve, meaning that any point PP added to OO results in PP.

- **Point Addition**: The group addition law is implemented, which allows you to add two distinct points on the curve. The sum of two points PP and QQ is another point RR on the curve, calculated using the slope of the line connecting PP and QQ.

- **Scalar Multiplication (Multiple Addition)**: This operation allows for the multiplication of a point PP by an integer nn, which is equivalent to adding PP to itself nn times. This operation is essential in ECC for generating public and private keys.

### 2. **Illustration of Elliptic Curves**

This section includes graphical representations of elliptic curves, showing how the curve’s points behave and the geometric properties of these curves. By visualizing the curve, one can better understand how points on the curve are used in cryptographic operations.

### 3. **Elliptic Curve Discrete Logarithm Problem (ECDLP)**

ECDLP is the core problem that ECC is based on. The repository provides an explanation of the ECDLP, which is considered computationally hard to solve. This difficulty ensures the security of ECC systems. The example illustrates how finding the discrete logarithm of a point on an elliptic curve is infeasible even with large amounts of computational resources.

### 4. **Elliptic Curve Diffie-Hellman (ECDH)**

The ECDH protocol allows two parties to securely exchange cryptographic keys over an insecure communication channel. Using elliptic curve mathematics, the protocol ensures that only the intended parties can derive the shared secret. This repository demonstrates how the ECDH key exchange works and provides a hands-on example of how keys can be exchanged and a shared secret can be generated.



## References
- [KEM-Seculab](https://kem.gitbook.io/cybersecurity/cryptography/elliptic-curve-cryptography)
- [NIST: Elliptic Curve Cryptography](https://csrc.nist.gov/projects/elliptic-curve-cryptography)
- [RFC 6637: Elliptic Curve Diffie-Hellman (ECDH) and Elliptic Curve Digital Signature Algorithm (ECDSA)](https://tools.ietf.org/html/rfc6637)

