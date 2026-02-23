# ------------------------
# The code implements the LLL (Lenstra-Lenstra-Lovász) algorithm, which is used for lattice basis reduction.
# The LLL algorithm reduces a given lattice basis into a "shorter" and "nearly orthogonal" basis.
# ------------------------


import numpy as np
import olll  # This seems to be an external library for LLL-based reductions.


def update_schmidt(B, B_star, k):
    """
    Updates the Schmidt orthogonalization of the first k vectors in the basis.

    Args:
        B (np.array): The lattice basis matrix (each row is a vector).
        B_star (np.array): The orthogonalized basis vectors.
        k (int): The index up to which the basis is orthogonalized.

    Returns:
        np.array: The updated B_star matrix.
    """
    for j in range(k + 1):
        B_star[j] = B[j]
        for i in range(j):
            # Subtract the projection of B[j] onto the previously orthogonalized vectors.
            B_star[j] -= (B[j] @ B_star[i]) / (B_star[i] @ B_star[i]) * B_star[i]
        B_star[j] = B_star[j]
    return B_star


def lovasz_condition(B, B_star, k, delta=3 / 4):
    """
    Checks if the Lovász condition is satisfied for the given k-th vector.

    Args:
        B (np.array): The lattice basis matrix.
        B_star (np.array): The orthogonalized basis matrix.
        k (int): The index of the vector to check.
        delta (float, optional): The constant used in the condition (default is 3/4).

    Returns:
        bool: True if the Lovász condition is satisfied, False otherwise.
    """
    mu = B[k] @ B_star[k - 1] / (B_star[k - 1] @ B_star[k - 1])
    return (
        np.linalg.norm(B_star[k]) ** 2
        >= (delta - mu**2) * np.linalg.norm(B_star[k - 1]) ** 2
    )


def swap(B, k):
    """
    Swaps the k-th and (k-1)-th vectors in the basis.

    Args:
        B (np.array): The lattice basis matrix.
        k (int): The index of the vector to swap with its previous vector.

    Returns:
        np.array: The updated lattice basis matrix after the swap.
    """
    B_k = list(B[k][:])
    B[k] = B[k - 1][:]
    B[k - 1] = B_k
    return B


def lll_alg(B):
    """
    Performs the LLL lattice basis reduction algorithm on the given basis.

    Args:
        B (np.array): The lattice basis matrix.

    Returns:
        np.array: The reduced lattice basis matrix.
    """
    n = B.shape[0]  # The number of vectors in the basis.
    B_star = np.zeros(B.shape, dtype=float)
    B_star = update_schmidt(B, B_star, 0)  # Initial Schmidt orthogonalization.

    k = 1
    while k < n:
        # Try to reduce the k-th vector by using previous ones.
        for j in range(k - 1, -1, -1):
            mu = abs(B[k] @ B_star[j] / (B_star[j] @ B_star[j]))
            if mu > 1 / 2:
                B[k] -= (
                    round(mu) * B[j]
                )  # Update B[k] by subtracting a multiple of B[j]
                B_star = update_schmidt(B, B_star, k)

        # Check if the Lovász condition is satisfied.
        if lovasz_condition(B, B_star, k):
            k += 1
        else:
            # Swap B[k] and B[k-1] if the condition isn't satisfied.
            B = swap(B, k)
            B_star = update_schmidt(B, B_star, k)
            k = max(k - 1, 1)  # Decrease k if needed.

    return B


if __name__ == "__main__":
    # Example lattice basis
    B = np.array(
        [
            [1, 1, 1],
            [-1, 0, 2],
            [3, 5, 6],
        ]
    )

    # Apply LLL algorithm and print the result
    print("Reduced Basis using LLL:")
    print(lll_alg(B).T)

    # Applying external LLL reduction from 'olll' library (assuming it works similarly)
    print("Reduced Basis using olll:")
    print(np.array(olll.reduction(B, 0.75)).T)
