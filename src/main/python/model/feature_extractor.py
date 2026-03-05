from pathlib import Path

import numpy as np

from model.ember_features import PEFeatureExtractor


def extract_ember_features(file_path):
    """
    Funzione per estrarre le feature EMBER da un file passato come percorso
    """
    path = Path(file_path).expanduser().resolve()

    extractor = PEFeatureExtractor()

    file_data = path.read_bytes()
    features = extractor.feature_vector(file_data)

    return np.asarray(features, dtype=np.float32)