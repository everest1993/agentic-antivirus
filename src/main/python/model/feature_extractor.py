from pathlib import Path

import numpy as np


def extract_ember_features(file_path: str | Path, feature_version: int = 2):
    path = Path(file_path).expanduser().resolve()

    if not path.is_file():
        raise FileNotFoundError(f"File non trovato: {path}")

    try:
        from ember.features import PEFeatureExtractor

    except Exception as exc:
        raise ImportError(
            "Dipendenza mancante per estrarre feature EMBER. "
            "Installa il pacchetto 'ember' (e relative dipendenze)."
        ) from exc

    extractor = PEFeatureExtractor(feature_version=feature_version)
    file_data = path.read_bytes()
    features = extractor.feature_vector(file_data)

    return np.asarray(features, dtype=np.float32)