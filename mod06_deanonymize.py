import pandas as pd

def load_data(anonymized_path, auxiliary_path):
    """
    Load anonymized and auxiliary datasets.
    """
    anon = pd.read_csv(anonymized_path)
    aux = pd.read_csv(auxiliary_path)
    return anon, aux


def link_records(anon_df, aux_df):
    """
    Attempt to link anonymized records to auxiliary records
    using exact matching on quasi-identifiers.

    Returns a DataFrame with columns:
      anon_id, matched_name
    containing ONLY uniquely matched records.
    """
    keys = ["age", "gender", "zip3"]

    aux_complete = aux_df.dropna(subset=keys)
    unique_aux = aux_complete[
        ~aux_complete.duplicated(subset=keys, keep=False)
    ]

    matches = anon_df.dropna(subset=keys).merge(
        unique_aux[keys + ["name"]],
        on=keys,
        how="inner",
        validate="many_to_one"
    )

    return matches[["anon_id", "name"]].rename(
        columns={"name": "matched_name"}
    )
    raise NotImplementedError


def deanonymization_rate(matches_df, anon_df):
    """
    Compute the fraction of anonymized records
    that were uniquely re-identified.
    """
    if anon_df.empty:
        return 0.0

    return len(matches_df) / len(anon_df)
    raise NotImplementedError
