from typing import Iterable, Mapping
from collections import Counter
import numpy as np
from editdistance import eval as ed

# def edit_distance(s1, s2, cost = lambda x, y: 1):
#   m = len(s1)
#   n = len(s2)
#   dp = [[0] * (n + 1) for _ in range(m + 1)]

#   # Fill the first row and first column
#   for i in range(m + 1):
#     dp[i][0] = i
#   for j in range(n + 1):
#     dp[0][j] = j

#   # Fill the matrix
#   for i in range(1, m + 1):
#     for j in range(1, n + 1):
#       c = 0 if s1[i-1] == s2[j-1] else cost(s1[i - 1], s2[j - 1])
#       dp[i][j] = min(
#         dp[i-1][j] + 1, # Deletion
#         dp[i][j-1] + 1, # Insertion
#         dp[i-1][j-1] + c
#       )

#   return dp[-1][-1]

def normalized_ed(a: str, b: str):
  """Edit distance normalized by the length of the longest string"""
  return ed(a, b) / max(len(a), len(b))

def sim(a: str, b: str, alpha = 10):
  ned = normalized_ed(a, b)
  return np.exp(-alpha * ned)

def Psim(p: str, Vp: Iterable[str], alpha = 10) -> Counter[str]:
  """Computes `Psim^p (w)` over all `w in Vp`
  - `p`: possibly out-of-vocabulary word to test
  - `Vp`: vocabulary to test against
  """
  Psim = Counter[str]({ w: sim(p, w, alpha) for w in Vp })
  total = sum(Psim.values())
  for w in Psim:
    Psim[w] /= total # type: ignore

  return Psim

def generalize_distrib(w: str, P: Mapping[str, Counter[str]], *, alpha = 10, k = 25):
  """Generalizes `P(w)` given `P`, by finding similar words to `w` in the vocabulary of `P`
  - `w`: word to generalize
  - `P`: existing distribution to generalize
  - `alpha`: scaling factor for similarity
  - `k`: number of similar words to consider
  """
  Vp = list(P.keys())
  Psim_w = Psim(w, Vp, alpha)
  posterior = Counter[str]()

  for p, Psim_pw in Psim_w.most_common(k):
    for l, Pocr_lp in P[p].items():
      posterior[l] += Psim_pw * Pocr_lp

  total = sum(posterior.values())
  for l in posterior:
    posterior[l] /= total # type: ignore

  return posterior