"""
Modulo da eseguire per effettuare il training del modello di classificazione
"""
from model.ml_model import MODEL, train_and_save_model


def main():
    train_and_save_model()
    print(f"Modello salvato in: {MODEL}")


if __name__ == "__main__":
    main()