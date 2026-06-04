import numpy as np
from scipy.linalg import expm
import math

# IP BOUNDARY: CORE MATHEMATICAL PRIMITIVES
# ZETA_ZEROS_T: Immutable constants from LMFDB for spectral filtering
ZETA_ZEROS_T = np.array([
    14.134725, 21.022040, 25.010858, 30.424876, 32.935062,
    37.586178, 40.918719, 43.327073, 48.005151, 49.773832,
    52.970321, 56.446248, 59.347044, 60.831779, 65.112544
])

def von_mangoldt(n: int) -> float:
    """
    Computes the Von Mangoldt function Lambda(n).
    Invariant: Lambda(p^k) = log(p) for primes p and k >= 1; 0 otherwise.
    Uses trial division up to sqrt(n).
    K(S) Contribution: Provides prime weighting for spectral embedding (delta_lambda_1: neutral).
    ARM64 Memory Bound: O(sqrt(n)) - trial division only, no sieve allocation.
    """
    if n <= 1:
        return 0.0
    
    # Trial division to find prime factors
    p = 0
    temp = n
    for i in range(2, int(math.isqrt(n)) + 1):
        if temp % i == 0:
            p = i
            break
    
    if p == 0:
        return math.log(n) # n itself is prime
        
    while temp % p == 0:
        temp //= p
        
    if temp == 1:
        return math.log(p) # n is a power of p
    return 0.0

def cartan_connection(u: np.ndarray, v: np.ndarray) -> np.ndarray:
    """
    Computes the continuous Cartan connection (parallel transport) from u to v.
    Replaces discrete Rodrigues rotations to guarantee det(R) = +1 in SO(d).
    Uses the Lie algebra generator (skew-symmetric tensor) and matrix exponential.
    """
    # Prevent divide by zero if zero vectors are passed
    norm_u = np.linalg.norm(u)
    norm_v = np.linalg.norm(v)
    if norm_u < 1e-12 or norm_v < 1e-12:
        return np.eye(len(u))

    u_hat = u / norm_u
    v_hat = v / norm_v
    
    # Skew-symmetric generator A = v_hat u_hat^T - u_hat v_hat^T
    # This matrix belongs to the Lie algebra so(d)
    A = np.outer(v_hat, u_hat) - np.outer(u_hat, v_hat)
    
    # Calculate matrix exponential to guarantee proper rotation
    # exp(A) is strictly orthogonal with det = +1
    R = expm(A)
    return R

def restriction_map(u: np.ndarray, v: np.ndarray, c: float) -> np.ndarray:
    """
    Computes the restriction map ρ_{uv} = c * R(u -> v)
    c must be bounded to [0, 1] representing coherence/agreement.
    """
    c = max(0.0, min(1.0, float(c)))
    R = cartan_connection(u, v)
    return c * R

class FiberSheafOps:
    @staticmethod
    def build_block_laplacian(edges: list, n_nodes: int, d: int) -> np.ndarray:
        """
        Builds the block sheaf Laplacian L_F = D - A.
        Edges should be a list of undirected tuples: (u_idx, v_idx, u_vec, v_vec, coherence_c).
        CRITICAL: L = D - A, NOT A^T A. Double-counting is prevented by treating edges as undirected.
        Result is symmetric PSD by construction.
        K(S) Contribution: Core spectral operator. lambda_1 of L_F is the spectral gap (delta_lambda_1: direct).
        ARM64 Memory Bound: O(n_nodes^2 * d^2) dense matrix. For n<=17 (AFE size), peak ~8KB.
        """
        size = n_nodes * d
        L = np.zeros((size, size))
        
        for u, v, u_vec, v_vec, c in edges:
            rho_uv = restriction_map(u_vec, v_vec, c)
            rho_vu = restriction_map(v_vec, u_vec, c)
            
            # Diagonal contribution (D)
            # D_uu += rho_vu^T rho_vu (approx c^2 I)
            u_start, u_end = u * d, (u + 1) * d
            v_start, v_end = v * d, (v + 1) * d
            
            L[u_start:u_end, u_start:u_end] += rho_vu.T @ rho_vu
            L[v_start:v_end, v_start:v_end] += rho_uv.T @ rho_uv
            
            # Off-diagonal contribution (A)
            # L_uv = - rho_uv^T rho_vu
            # L_vu = - rho_vu^T rho_uv
            L[u_start:u_end, v_start:v_end] -= rho_uv.T @ rho_vu
            L[v_start:v_end, u_start:u_end] -= rho_vu.T @ rho_uv
            
        return L
