import asyncio
from typing import TypedDict

from ninject import Context, Dependency, dependencies, inject

Greeting = Dependency[str, "Greeting"]
Recipient = Dependency[str, "Recipient"]


@dependencies
class MessageContent(TypedDict):
    greeting: Greeting
    recipient: Recipient


@inject
async def print_message(*, greeting: Greeting = inject.ed, recipient: Recipient = inject.ed):
    print(f"{greeting}, {recipient}!")


context = Context()


async def get_message() -> str:
    return "Hello"


async def get_recipient() -> str:
    return "World"


@context.provides(MessageContent)
async def provide_message_content() -> dict:
    greeting, recipient = await asyncio.gather(get_message(), get_recipient())
    return {"greeting": greeting, "recipient": recipient}


if __name__ == "__main__":
    with context:
        asyncio.run(print_message())
