# Agentic Antivirus

Applicazione desktop (PySide6) con due funzionalita principali:

- chat agente locale (tools);
- classificatore malware di file basato su feature EMBER e modello TensorFlow.

## Stato del progetto

Questo progetto e un prototipo sperimentale di antivirus.
Non e un prodotto finale affidabile o completo e non garantisce protezione reale del sistema.
Non sostituisce un antivirus/EDR di produzione.

## Stack tecnico

- Python
- PySide6 (GUI)
- TensorFlow + NumPy (modello di classificazione)
- EMBER feature extractor locale (modulo vendorizzato da `elastic/ember`)
- LangChain + Ollama (assistant locale)

## Prerequisiti

1. Python con versione compatibile con TensorFlow.
2. Ollama installato e in esecuzione.
3. Modello chat disponibile in Ollama: `qwen3-vl:latest` (default in `model/assistant.py`).

## Download repository

```bash
git clone https://github.com/everest1993/agentic-antivirus.git
cd agentic-antivirus
```

## Installazione requirements

Dalla root del progetto:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Scaricare il modello LLM locale:

```bash
ollama pull qwen3-vl:latest
```

## Training modello malware (prima dell'avvio)

Il modello di classificazione deve essere trainato **prima** di avviare la GUI.
Il training **non** scarica automaticamente i parquet.

Scaricare manualmente il dataset EMBER v2 da:
`https://www.kaggle.com/datasets/dhoogla/ember-2018-v2-features`

Posizionare i file parquet in:
`src/main/python/model/parquet/`

- `train_ember_2018_v2_features.parquet`
- `test_ember_2018_v2_features.parquet`

Eseguire:

```bash
python src/main/python/train_model.py
```

Questo comando usa i parquet in `src/main/python/model/parquet/` e salva il modello in `saved_models/malware_detector.keras`.

## Avvio applicazione

Dalla stessa root del progetto:

```bash
python src/main/python/app.py
```

La finestra si apre con dimensione iniziale `800x400`.

## Comportamento del modello malware

All'avvio, `HomeController` carica il modello con `build_model()`:

- se trova `saved_models/malware_detector.keras` lo carica;
- se non lo trova, solleva errore: prima va eseguito il training manuale.

La predizione e implementata in:

```python
HomeController.classify_file(file_path=None)
```

Output:
- `Pericoloso` se score >= 0.65;
- `Dubbio` se 0.50 <= score < 0.65;
- `Sicuro` se score < 0.50.

## Miglioramenti e sviluppi futuri

- Migliorare il modello di classificazione.
- Introdurre una gestione completa dei file sospetti: quarantena, ripristino e rimozione definitiva.
- Aggiungere un flusso HITL (Human-in-the-Loop) per la revisione manuale dei casi con score vicino alla soglia.
- Estendere la scansione da singolo file a directory (anche ricorsive).