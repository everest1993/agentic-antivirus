import tensorflow as tf
import matplotlib.pyplot as plt

from pathlib import Path

BATCH_SIZE = 32
PROJECT_ROOT = Path(__file__).resolve().parents[4]
MODEL = PROJECT_ROOT / "saved_models" / "malware_detector.keras"
LEGACY_MODEL = PROJECT_ROOT.parent / "saved_models" / "malware_detector.keras"


def _get_saved_model_path():
    if MODEL.exists():
        return MODEL
    if LEGACY_MODEL.exists():
        return LEGACY_MODEL
    return None


def build_model():
    saved_model = _get_saved_model_path()
    if saved_model is not None:
        return tf.keras.models.load_model(saved_model)

    # build and fit
    from model.dataset import split_dataset, get_input_shape
    train_ds, val_ds, _, _ = split_dataset()

    train_ds = train_ds.batch(BATCH_SIZE).prefetch(tf.data.AUTOTUNE)
    val_ds = val_ds.batch(BATCH_SIZE).prefetch(tf.data.AUTOTUNE)

    # model
    model = tf.keras.models.Sequential([
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
        tf.keras.layers.Dense(1, activation="sigmoid")
    ])

    model.summary()

    model.compile(
        optimizer=tf.keras.optimizers.Adam(1e-3),
        loss="binary_crossentropy",
        metrics=[tf.keras.metrics.AUC(name="auc"), "precision", "recall"]
    )

    callbacks = [
        tf.keras.callbacks.EarlyStopping(
            monitor="val_loss",
            patience=5,
            restore_best_weights=True
        ),
        tf.keras.callbacks.ReduceLROnPlateau(
            monitor="val_loss",
            factor=0.5,
            patience=3,
            min_lr=1e-6
        )
    ]

    history = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=30,
        callbacks=callbacks
    )

    MODEL.parent.mkdir(parents=True, exist_ok=True)
    model.save(MODEL)

    show_metrics(history.history)

    return model


def show_metrics(training_history):
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