# Agentic Antivirus

Applicazione desktop (PySide6) con due funzionalita principali:

- chat agente locale (tools);
- classificatore malware su file PE basato su feature EMBER e modello TensorFlow.

## Stack tecnico

- Python
- PySide6 (GUI)
- TensorFlow + NumPy (modello di classificazione)
- EMBER feature extractor (`ember` da GitHub Elastic)
- LangChain + Ollama (assistant locale)

## Struttura essenziale

```text
agentic-antivirus/
├── src/main/python/
│   ├── app.py
│   ├── controller/
│   ├── model/
│   │   ├── assistant.py
│   │   ├── feature_extractor.py
│   │   ├── ml_model.py
│   │   └── dataset.py
│   └── view/
└── requirements.txt
```

## Prerequisiti

1. Python con versione compatibile con TensorFlow.
2. Ollama installato e in esecuzione.
3. Modello chat disponibile in Ollama: `qwen3-vl:latest` (default in `model/assistant.py`).

## Download repository

```bash
git clone https://github.com/everest1993/agentic-antivirus.git
```

## Installazione requirements

Dalla cartella che contiene la repository clonata:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Scarica il modello LLM locale:

```bash
ollama pull qwen3-vl:latest
```

## Avvio applicazione

Dalla stessa cartella usata sopra:

```bash
python agentic-antivirus/src/main/python/app.py
```

La finestra si apre con dimensione iniziale `800x400`.

## Comportamento del modello malware

All'avvio, `home_controller.Controller` crea il modello con `build_model()`:

- se trova `saved_models/malware_detector.keras` lo carica;
- altrimenti prova a fare training usando i parquet in `src/main/python/model/parquet/` e poi salva il modello.

La predizione e implementata in:

```python
Controller.classify_file(file_path=None, threshold=0.5)
```

Output:
- `Potenziale malware (score=...)` se score >= soglia;
- `File ok (score=...)` altrimenti.

## Miglioramenti previsti

- esporre la scansione malware direttamente dalla GUI;
- gestire la chat in thread separato per evitare freeze UI;
- aggiungere tool reali all'assistente (es. scan file esplicito da prompt).
- sostituire il modello ML con uno più performante
