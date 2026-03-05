"""
Assistente LLM con utilizzo tools
"""
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from langchain_core.tools import tool
from PySide6.QtCore import QMetaObject, Qt, Q_RETURN_ARG
from typing import Optional


CHAT_MODEL = "qwen3-vl:latest"


class Assistant:
    SYSTEM_PROMPT = """
    Sei un assistente specializzato SOLO in sicurezza informatica.
    Rispondi esclusivamente a domande su cybersecurity (malware, phishing, hardening,
    vulnerabilità, incident response, privacy e protezione dei sistemi).
    Se la richiesta NON riguarda la sicurezza informatica, rispondi SOLO con:
    'Posso aiutarti solo su temi di sicurezza informatica.'.

    Regole operative (OBBLIGATORIE):
    1) Se l'utente chiede di scansionare/analizzare/verificare un file:
    - DEVI chiamare il tool `classify_file`.
    - Se l'utente NON fornisce un percorso file esplicito, chiama `classify_file` con `path` mancante o None.
    - Non chiedere all’utente di incollare il path.

    2) Per richieste in ambito cybersecurity che NON richiedono una scansione:
    - NON usare tool.
    - Rispondi in modo pratico e conciso, con best practice pertinenti.
    - Se non sei sicuro, rispondi: 'Non sono in grado di aiutarti o risponderti.'.

    Contesto:
    {context}
    """


    def __init__(self, controller):
        self.controller = controller

        @tool(description="Classifica la sicurezza di un file locale.")
        def classify_file(path: Optional[str] = None):
            if not path: # se il path non arriva dal prompt viene aperto il file picker
                path = QMetaObject.invokeMethod( # esegue il metodo nel main thread
                    self.controller,
                    "select_file",
                    Qt.BlockingQueuedConnection,
                    Q_RETURN_ARG(str),
                )

            if not path:
                return "Nessun file selezionato."
            
            resolved, probability, _, risk_label = self.controller.classify_file(path)
            return f"Esito scansione per '{resolved}': {risk_label} (score={probability:.4f})."


        self.tools_list = [classify_file] # lista (richiesta da bind_tools)
        # mappa per lookup del nome
        self.tools = {tool_item.name: tool_item for tool_item in self.tools_list}
        self.llm = ChatOllama(model=CHAT_MODEL, temperature=0).bind_tools(self.tools_list)
        # prompt di sistema e storico turni user/assistant/tool
        self.messages = [SystemMessage(content=self.SYSTEM_PROMPT.format(context=""))]


    def _invoke_model(self):
        """
        Invoca il modello e normalizza il testo della risposta
        """
        ai_response = self.llm.invoke(self.messages)

        if ai_response is None:
            return None, ""

        text = getattr(ai_response, "content", "").strip()
        
        return ai_response, text


    def _append_tool_outputs(self, ai_response):
        """
        Esegue le tool-call richieste dal modello e inserisce i risultati nello storico
        """
        for call in getattr(ai_response, "tool_calls", []):
            tool_name = call.get("name", "")
            tool_args = call.get("args", {})
            tool_call_id = call.get("id", "")
            selected_tool = self.tools.get(tool_name)

            if selected_tool is None:
                return f"Tool '{tool_name}' non disponibile."
            else:
                try:
                    output = selected_tool.invoke(tool_args)
                except Exception as exc:
                    output = f"Errore tool '{tool_name}': {exc}"

            self.messages.append(
                ToolMessage(
                    content=str(output),
                    tool_call_id=tool_call_id or f"missing-{tool_name or 'tool'}",
                )
            )


    def chat(self, user_message):
        text = user_message.strip()

        # risposta diretta oppure richiesta tool
        self.messages.append(HumanMessage(content=text))
        ai_response, response_text = self._invoke_model()

        if ai_response is None:
            return "Non sono in grado di aiutarti."

        self.messages.append(ai_response)

        if not getattr(ai_response, "tool_calls", None):
            return response_text

        # se ci sono tool-call: append output tool invoke modello per la risposta finale
        self._append_tool_outputs(ai_response)
        final_response, final_text = self._invoke_model()

        if final_response is None:
            return "Non sono in grado di aiutarti."

        self.messages.append(final_response)

        return final_text