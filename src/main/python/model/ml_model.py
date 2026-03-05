"""
Modello MLP per classificazione binaria
"""
from pathlib import Path

import shutil
import matplotlib.pyplot as plt
import tensorflow as tf


BATCH_SIZE = 32
EPOCHS = 30
PROJECT_ROOT = Path(__file__).resolve().parents[4]
MODEL_DIR = PROJECT_ROOT / "saved_models"
MODEL = MODEL_DIR / "malware_detector.keras"


def _get_saved_model_path():
    """
    Verifica se il modello è già stato costruito e allenato
    """
    if MODEL.exists():
        return MODEL

    return None


def build_model():
    """
    Recupera il modello se già presente
    """
    saved_model = _get_saved_model_path()

    if saved_model is not None:
        return tf.keras.models.load_model(saved_model)
    else:
        raise FileNotFoundError(
            f"Modello non trovato in '{MODEL}'. "
            "Effettua il training eseguendo il modulo: "
            "python agentic-antivirus/src/main/python/train_model.py"
        )


def train_and_save_model(epochs: int = EPOCHS):
    """
    Esegue build e training del modello di classificazione
    """
    from model.dataset import get_input_shape, split_dataset # lazy import

    train_ds, val_ds, _, _ = split_dataset()
    train_ds = train_ds.batch(BATCH_SIZE).prefetch(tf.data.AUTOTUNE)
    val_ds = val_ds.batch(BATCH_SIZE).prefetch(tf.data.AUTOTUNE)

    # modello MLP sequenziale
    model = tf.keras.models.Sequential(
        [
            tf.keras.Input(shape=(get_input_shape(),)),
            tf.keras.layers.Dense(512, activation="relu"),
            tf.keras.layers.BatchNormalization(),
            tf.keras.layers.Dropout(0.3),
            tf.keras.layers.Dense(128, activation="relu"),
            tf.keras.layers.BatchNormalization(),
            tf.keras.layers.Dropout(0.3),
            tf.keras.layers.Dense(32, activation="relu"),
            tf.keras.layers.BatchNormalization(),
            tf.keras.layers.Dropout(0.3),
            tf.keras.layers.Dense(1, activation="sigmoid"),
        ]
    )

    model.compile(
        optimizer=tf.keras.optimizers.Adam(1e-3),
        loss="binary_crossentropy",
        metrics=[tf.keras.metrics.AUC(name="auc"), "precision", "recall"],
    )

    callbacks = [
        tf.keras.callbacks.EarlyStopping(
            monitor="val_loss",
            patience=5,
            restore_best_weights=True,
        ),
        tf.keras.callbacks.ReduceLROnPlateau(
            monitor="val_loss",
            factor=0.5,
            patience=3,
            min_lr=1e-6,
        ),
    ]

    history = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=epochs,
        callbacks=callbacks,
    )

    MODEL_DIR.mkdir(parents=True, exist_ok=True) # crea la cartella saved_models se non esiste
    model.save(MODEL) # salva il modello nella cartella
    show_metrics(history.history)

    return model


def show_metrics(training_history):
    """
    Mostra la qualità del training nelle varie epoche
    """
    metrics_to_plot = [
        ("loss", "Loss"),
        ("auc", "AUC"),
        ("precision", "Precision"),
        ("recall", "Recall"),
    ]

    available_metrics = [
        (key, label)
        for key, label in metrics_to_plot
        if key in training_history and f"val_{key}" in training_history
    ]

    if not available_metrics:
        return

    _, axes = plt.subplots(len(available_metrics), 1, figsize=(10, 4 * len(available_metrics)))
    if len(available_metrics) == 1:
        axes = [axes]

    for ax, (metric_key, metric_label) in zip(axes, available_metrics):
        ax.plot(training_history[metric_key], label=f"Train {metric_label}")
        ax.plot(training_history[f"val_{metric_key}"], label=f"Validation {metric_label}")
        ax.set_xlabel("Epochs")
        ax.set_ylabel(metric_label)
        ax.set_title(f"Training vs Validation {metric_label}")
        ax.legend()

    plt.tight_layout()
    plt.show()