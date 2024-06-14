from typing import Union

import techgram
from techgram import raw


class GroupCallsNotFound(Exception):
    def __init__(self, er: str):
        super().__init__(er)


class DiscardGroupCall:
    async def discard_group_call(
        self: "techgram.Client",
        chat_id: Union[int, str]
    ) -> "techgram.raw.base.Updates":
        """ Discard group call
        """
        call = await self.get_group_call(chat_id)

        if call.call is None:
            raise GroupCallsNotFound('Chat Without a Voice Chats')

        return await self.invoke(
            raw.functions.phone.DiscardGroupCall(
                call=call.call
            )
        )
