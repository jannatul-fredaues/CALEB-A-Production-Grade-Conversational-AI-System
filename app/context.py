# context.py

MAX_TURNS = 6  # user+assistant pairs

def trim_conversation(conversation: list) -> list:
    if not conversation:
        return conversation

    system = conversation[0]
    messages = conversation[1:]

    max_messages = MAX_TURNS * 2
    if len(messages) <= max_messages:
        return conversation

    return [system] + messages[-max_messages:]
