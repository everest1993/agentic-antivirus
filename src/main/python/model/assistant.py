from langchain_ollama import ChatOllama
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage


# CHAT_MODEL = "qwen3-vl:latest"
CHAT_MODEL = "llama3.1:latest"


class Assistant:
    # modificare con RAG o con comportamenti consigliati per prevenire infezioni del PC
    SYSTEM_PROMPT = """
    Rispondi SOLO a domande su malware. Non inventare.
    Se l'utente chiede informazioni che non conosci rispondi con:
    'Non sono in grado di aiutarti o risponderti.'.

    Default: NON usare tools.
    Usa un tool SOLO se l’utente chiede esplicitamente quell’azione e fornisce i dati necessari.
    Se i dati necessari mancano, chiedi all’utente di fornirli (senza chiamare tools).

    Contesto:
    {context}
    """

    def __init__(self):
        self.tools = []  # da definire (scan)

        # chat model servito da Ollama
        self.llm = ChatOllama(model=CHAT_MODEL, temperature=0).bind_tools(self.tools)
        self.messages = [SystemMessage(content=self.SYSTEM_PROMPT.format(context="Nessun contesto aggiuntivo."))]


    def chat(self, user_message: str) -> str:
        text = (user_message or "").strip()

        if not text:
            return ""

        self.messages.append(HumanMessage(content=text))
        ai_response = self.llm.invoke(self.messages)

        response_text = ai_response.content

        if isinstance(response_text, list):
            response_text = " ".join(
                part.get("text", "") for part in response_text if isinstance(part, dict)
            ).strip()
            
        response_text = str(response_text).strip()

        self.messages.append(AIMessage(content=response_text))
        return response_text or "Non sono in grado di aiutarti o risponderti."