from typing import Mapping, Iterable, Sequence
from collections import Counter
from dataclasses import dataclass
import ocr_map as om

def sample(distribution: Counter):
  import random
  return random.choices(list(distribution.keys()), weights=distribution.values())[0] # type: ignore

@dataclass
class Prior:

  Pocr: Mapping[str, Counter[str]]

  @classmethod
  def fit(cls, samples: Iterable[om.Sample]) -> 'Prior':
    """Fit the OCR simulator to a set of samples"""
    return Prior(om.Pocr(samples))
  
  @property
  def labels(self) -> set[str]:
    """Set of labels in the training samples"""
    return set(self.Pocr.keys())
  
  def distrib(self, label: str, *, alpha: int = 10, k: int = 25) -> Counter[str]:
    """Generalize the trained distribution to any `label`"""
    return om.generalize_distrib(label, self.Pocr, alpha=alpha, k=k)

  def simulate(self, word: str, *, alpha: int = 10, k: int = 25) -> str:
    """Simulate OCR noise for any given word
    - `alpha`: scaling factor for similarity (higher `alpha`s make the results closer to the original `word`)
    - `k`: number of similar words to consider
    """
    return sample(self.distrib(word, alpha=alpha, k=k))

@dataclass
class Posterior:
  Pl: Counter[str]
  Pocr_post: Mapping[str, Counter[str]]

  @classmethod
  def fit_prior(cls, Pocr: Mapping[str, Counter[str]], labels: Iterable[str]) -> 'Posterior':
    """Fit the model to a set of samples"""
    Pl = om.Pl(labels)
    Pocr_post = om.Pocr_posterior(Pocr, Pl)
    return Posterior(Pl, Pocr_post)

  def distrib(self, ocrpred: str, *, alpha: int = 10, k: int = 25) -> Counter[str]:
    """Generalize the trained posterior distribution to any `ocrpred`"""
    return om.generalize_distrib(ocrpred, self.Pocr_post, alpha=alpha, k=k)
  
  def denoise(self, ocrpred: str, *, alpha: int = 10, k: int = 25) -> str:
    """Denoise any OCR prediction `ocrpred`"""
    return sample(self.distrib(ocrpred, alpha=alpha, k=k))
  
@dataclass
class Model:

  prior_model: Prior
  post_model: Posterior


  @classmethod
  def fit(cls, samples: Sequence[om.Sample]) -> 'Model':
    """Fit the model to a set of samples"""
    prior = Prior.fit(samples)
    post = Posterior.fit_prior(prior.Pocr, (l for l, _ in samples))
    return Model(prior, post)
  
  def denoise(self, ocrpred: str, *, alpha: int = 10, k: int = 25) -> str:
    """Denoise any OCR prediction `ocrpred`"""
    return self.post_model.denoise(ocrpred, alpha=alpha, k=k)
  
  def simulate(self, word: str, *, alpha: int = 10, k: int = 25) -> str:
    """Simulate OCR noise for any given word
    - `alpha`: scaling factor for similarity (higher `alpha`s make the results closer to the original `word`)
    - `k`: number of similar words to consider
    """
    return self.prior_model.simulate(word, alpha=alpha, k=k)
  
  def posterior(self, ocrpred: str, *, alpha: int = 10, k: int = 25) -> Counter[str]:
    """Generalize the trained posterior distribution to any `ocrpred`"""
    return self.post_model.distrib(ocrpred, alpha=alpha, k=k)
  
  def prior(self, word: str, *, alpha: int = 10, k: int = 25) -> Counter[str]:
    """Generalize the trained distribution to any `word`"""
    return self.prior_model.distrib(word, alpha=alpha, k=k)
  
  @property
  def labels(self) -> set[str]:
    """Vocabulary of labels in the training samples"""
    return self.prior_model.labels
  
  @property
  def ocrpreds(self) -> set[str]:
    """Vocabulary of ocr preds in the training samples"""
    return set(self.post_model.Pocr_post.keys())
  
  @property
  def Pocr(self) -> Mapping[str, Counter[str]]:
    """Prior distribution"""
    return self.prior_model.Pocr
  
  @property
  def Pl(self) -> Counter[str]:
    """Label distribution"""
    return self.post_model.Pl
  
  @property
  def Pocr_post(self) -> Mapping[str, Counter[str]]:
    """Posterior distribution"""
    return self.post_model.Pocr_post