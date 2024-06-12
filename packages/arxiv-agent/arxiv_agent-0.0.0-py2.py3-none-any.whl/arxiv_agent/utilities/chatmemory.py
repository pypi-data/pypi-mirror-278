from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.messages import BaseMessage, AIMessage
from langchain_core.chat_history import BaseChatMessageHistory

from langchain_core.pydantic_v1 import BaseModel, Field
from typing import List


class InMemoryHistory(BaseChatMessageHistory, BaseModel):
    """In memory implementation of chat message history."""

    messages: List[BaseMessage] = Field(default_factory=list)

    def get_length(self) -> int:
        """Get the length of the chathistory"""
        return len(self.messages)

    def add_messages(self, messages: List[BaseMessage]) -> None:
        """Add a list of messages to the store"""
        self.messages.extend(messages)

    def delete_messages(self, indices: List[int]) -> None:
        """Delete messages from the store"""
    # indices should be a list or index in reverse order 
        for idx in indices:
            self.messages.pop(idx)

    def modify_summary(self, summary: BaseMessage) -> None:
        """modify the chathistory by the current summary"""
        self.messages[0] = summary

    def insert_memory_at_beginning(self, summary: BaseMessage) -> None:
        """insert a summary at the beginnng of the current history"""
        self.messages.insert(0, summary)

    def initialize_summary(self) -> None:
        """insert the summary into the chat history"""
        self.messages.insert(0, AIMessage(content=''))

    def get_message(self, i) -> BaseMessage:
        """check the i-th message in the history"""
        return self.messages[i]

    def modify_history(self, index: int, message: BaseMessage) -> None:
        "modify a piece of message"
        self.messages[index] = message

    def get_last_round(self) -> None:
        "get the AI and tool output from last round"
        return self.messages[-2:]

    def clear(self) -> None:
        self.messages = []

