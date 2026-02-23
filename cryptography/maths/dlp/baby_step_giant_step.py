from math import sqrt, ceil

def break_dlp(y, g, p):
    """
    This function solves the discrete logarithm problem using the Baby-Step Giant-Step algorithm.
    It finds an integer `l` such that `y = g^l mod p`.

    Args:
        y (int): The result of the discrete logarithm (the target value).
        g (int): The base of the discrete logarithm.
        p (int): The modulus for the discrete logarithm.

    Returns:
        int: The solution `l` to the equation `y = g^l mod p`.
    """
    # Calculate the square root of p and round up to the nearest integer
    m = ceil(sqrt(p))
    
    # Baby step: store all values of g^k mod p for k from 0 to m-1
    baby_steps = {pow(g, k, p): k for k in range(m)}
    print("Baby Steps: ", baby_steps)

    x = y
    j = 0
    # Calculate the inverse of g^m mod p
    inv_g_pow_m = pow(g, -m, p)
    print(f"Inverse modulo of g^m: {inv_g_pow_m}")

    all_x = [x]
    
    # Giant step: compute x * g^(-m) mod p iteratively
    while x not in baby_steps.keys():
        x = pow(x * inv_g_pow_m, 1, p)
        all_x.append(x)
        j += 1

    print("Giant Steps: ", all_x)

    # Calculate the solution to the discrete logarithm problem
    l = j * m + baby_steps[x]
    print(f"{g}^{l} = {pow(g, l, p)}[{p}]\n")
    return l


if __name__ == "__main__":
    p = 101  
    m = ceil(sqrt(p)) 
    g = 2  
    y = 48  
    
    # Perform the attack and get the solution l
    l = break_dlp(y, g, p)
