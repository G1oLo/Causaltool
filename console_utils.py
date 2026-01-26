import asyncio
from typing import AsyncGenerator, Optional, List
from autogen_agentchat.messages import TextMessage

# Coda globale a cui il consumer della Console è in ascolto
message_queue: Optional[asyncio.Queue] = None

# Buffer per il riassunto e per la conversazione
summary_buffer: List[TextMessage] = []
conversation_buffer: List[TextMessage] = []

buffer_mode: bool = True  # Default: i messaggi vengono bufferizzati


def set_queue(q: asyncio.Queue):
    global message_queue
    message_queue = q


async def queue_to_stream(q: asyncio.Queue) -> AsyncGenerator[TextMessage, None]:
    while True:
        msg = await q.get()
        yield msg
        q.task_done()


async def send(msg: TextMessage, buffer_type: str = "conversation"):
    if message_queue is None:
        raise RuntimeError(
            "message_queue non è impostata. Chiama set_queue() prima di usare send()."
        )

    payload = msg.model_dump()
    # Modifica per la spaziatura: aggiungi \n alla fine del contenuto.
    payload["content"] = f"{msg.content.strip()}\n"
    formatted_msg = TextMessage(**payload)

    if buffer_mode:
        if buffer_type == "summary":
            summary_buffer.append(formatted_msg)
        else:
            conversation_buffer.append(formatted_msg)
    else:
        await message_queue.put(formatted_msg)


def set_buffer_mode(enabled: bool):
    global buffer_mode
    buffer_mode = enabled


async def _flush_internal_buffer(internal_buffer: List[TextMessage]):
    """Funzione helper per inviare messaggi da un buffer specifico alla coda e pulirlo."""
    if message_queue is None:
        raise RuntimeError("message_queue non è impostata al momento del flush.")

    for m in internal_buffer:
        await message_queue.put(m)
    internal_buffer.clear()


async def flush_summary_buffer():
    """Invia tutti i messaggi dal summary_buffer alla coda e pulisce il buffer."""
    await _flush_internal_buffer(summary_buffer)


async def flush_conversation_buffer_log():
    """Invia tutti i messaggi dal conversation_buffer alla coda e pulisce il buffer."""
    await _flush_internal_buffer(conversation_buffer)


async def flush_buffer(
    buffer_type: str,
):  # Funzione aggiornata che sostituisce la vecchia flush_buffer
    if message_queue is None:
        raise RuntimeError("message_queue non è impostata.")

    current_buffer = summary_buffer if buffer_type == "summary" else conversation_buffer

    for msg_to_send in list(
        current_buffer
    ):  # Itera su una copia se modifichi durante l'iterazione (qui clear())
        await message_queue.put(msg_to_send)
    current_buffer.clear()


async def flush_conversation_buffer():
    """Svuota specificamente il conversation_buffer sulla coda dei messaggi."""
    await flush_buffer("conversation")  # Usa la logica centralizzata di flush_buffer
