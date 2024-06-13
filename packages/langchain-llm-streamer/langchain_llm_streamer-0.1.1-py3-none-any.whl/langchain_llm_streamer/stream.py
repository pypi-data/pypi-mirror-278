import asyncio


async def _stream_response(model, messages: list[str]) -> None:
    """
    Stream the response from the model to the console.

    Args:
        model: The language model instance.
        messages (list[str]): The list of messages to send to the model.
    """
    chunks = []
    async for chunk in model.astream(messages):
        chunks.append(chunk)
        print(chunk.content, end="", flush=True)


def stream_print(model, messages: list[str]) -> None:
    """
    Print the response from the model to the console.

    Args:
        model: The language model instance.
        messages (list[str]): The list of messages to send to the model.
    """
    asyncio.run(_stream_response(model, messages))
    print()
