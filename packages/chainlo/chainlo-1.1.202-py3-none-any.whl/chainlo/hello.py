# This is a simple example of a chainlit app.

from chainlo import AskUserMessage, Message, on_chat_start

from typing import Dict, List, Optional

import chainlo.data as cl_data
from chainlo.step import StepDict


import chainlo as cl

import chainlo.data as cl_data
from chainlo.data.sql_alchemy import SQLAlchemyDataLayer


cl_data._data_layer = SQLAlchemyDataLayer(conninfo="postgresql+asyncpg://postgres:postgres@192.168.100.5:5432/chats")


@cl.oauth_callback
def auth_callback(provider_id: str, token: str, raw_user_data, default_app_user):
    if provider_id == "google":
        if "@chainlo.io" in raw_user_data["email"]:
            return default_app_user
    return None


@on_chat_start
async def main():
    res = await AskUserMessage(content="What is your name?", timeout=30).send()
    if res:
        await Message(
            content=f"Your name is: {res['output']}.\nChainlit installation is working!\nYou can now start building your own chainlit apps!",
        ).send()
