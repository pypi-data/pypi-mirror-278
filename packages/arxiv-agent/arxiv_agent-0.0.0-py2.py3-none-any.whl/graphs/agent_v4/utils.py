from langchain_core.chat_history import BaseChatMessageHistory
from ...utilities.chatmemory import InMemoryHistory

store = {}
def get_by_session_id(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        print(f"Creating new store for session {session_id}")
        store[session_id] = InMemoryHistory()
    return store[session_id]