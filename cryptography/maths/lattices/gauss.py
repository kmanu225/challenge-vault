import numpy as np

def gauss_reduction(v1, v2):
    """
    Performs the Gauss Lattice Base Reduction algorithm to reduce two lattice vectors.

    The algorithm works by iteratively applying the following steps:
    1. If the norm of v2 is less than the norm of v1, swap v1 and v2.
    2. Compute m as the rounded value of the dot product of v1 and v2 divided by the squared norm of v1.
    3. If m is zero, return the reduced vectors v1 and v2.
    4. Otherwise, update v2 by subtracting m*v1 from it.

    Args:
        v1 (np.array): The first lattice vector.
        v2 (np.array): The second lattice vector.

    Returns:
        tuple: The reduced lattice vectors v1 and v2.
    """
    while True:
        # (a) If ||v2|| < ||v1||, swap v1, v2
        if np.linalg.norm(v2) < np.linalg.norm(v1):
            v1, v2 = v2, v1

        # (b) Compute m = ⌊ v1∙v2 / v1∙v1 ⌉
        dot_product = np.dot(v1, v2)
        norm_sq = np.dot(v1, v1)
        m = int(dot_product / norm_sq)
        print(f"m: {m}")

        # (c) If m = 0, return v1, v2
        if m == 0:
            return v1, v2

        # (d) v2 = v2 - m*v1
        v2 = v2 - m * v1

if __name__ == "__main__":
    v = (846835985, 9834798552)
    u = (87502093, 123094980)
    v1 = np.array(v)
    v2 = np.array(u)
    
    print(f"v1: {v1}, v2: {v2}")
    
    # Perform Gauss lattice reduction
    v1, v2 = gauss_reduction(v1, v2)
    
    print(f"v1: {v1}, v2: {v2}")
    
    # Compute and display the inner product of v1 and v2
    print(f"Inner product of v1 and v2: {np.dot(v1, v2)}")
