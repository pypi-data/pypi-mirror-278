from typing import Iterable, Collection
import pandas as pd
from . import Sample

def parse_df(df: pd.DataFrame, vocab: Collection[str] | None = None) -> Iterable[Sample]:
  """Parses a dataframe with columns `lab, pred-0, prob-0, ..., pred-24, prob-24`
  - `vocab`: if provided, only samples with labels in `vocab` are yielded
  """
  for _, row in df.iterrows():
    label = row['lab']
    if vocab is None or label in vocab:
      top_preds = [(str(row[f'pred-{i}']), row[f'prob-{i}']) for i in range(25)]
      yield label, top_preds
