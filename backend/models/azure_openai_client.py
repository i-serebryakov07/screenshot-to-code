import time
from typing import Awaitable, Callable, List
from openai import AsyncAzureOpenAI
from openai.types.chat import ChatCompletionMessageParam, ChatCompletionChunk
from llm import Completion


async def stream_azure_openai_response(
    messages: List[ChatCompletionMessageParam],
    api_key: str,
    endpoint: str,
    deployment: str,
    api_version: str,
    callback: Callable[[str], Awaitable[None]],
) -> Completion:
    """Stream completions from an Azure OpenAI deployment."""
    start_time = time.time()
    client = AsyncAzureOpenAI(
        api_key=api_key,
        azure_endpoint=endpoint,
        api_version=api_version,
    )

    params = {
        "model": deployment,
        "messages": messages,
        "temperature": 0,
        "stream": True,
        "timeout": 600,
    }

    stream = await client.chat.completions.create(**params)  # type: ignore
    full_response = ""
    async for chunk in stream:  # type: ignore
        assert isinstance(chunk, ChatCompletionChunk)
        if (
            chunk.choices
            and len(chunk.choices) > 0
            and chunk.choices[0].delta
            and chunk.choices[0].delta.content
        ):
            content = chunk.choices[0].delta.content or ""
            full_response += content
            await callback(content)

    await client.close()
    completion_time = time.time() - start_time
    return {"duration": completion_time, "code": full_response}
