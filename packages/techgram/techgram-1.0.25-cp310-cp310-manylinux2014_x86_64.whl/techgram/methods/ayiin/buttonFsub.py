#  ===========================================================
#              Copyright (C) 2023-present AyiinXd
#  ===========================================================
#  ||                                                       ||
#  ||              _         _ _      __  __   _            ||
#  ||             / \  _   _(_|_)_ __ \ \/ /__| |           ||
#  ||            / _ \| | | | | | '_ \ \  // _` |           ||
#  ||           / ___ \ |_| | | | | | |/  \ (_| |           ||
#  ||          /_/   \_\__, |_|_|_| |_/_/\_\__,_|           ||
#  ||                  |___/                                ||
#  ||                                                       ||
#  ===========================================================
#   Appreciating the work of others is not detrimental to you
#  ===========================================================


import techgram
from techgram import errors, types


class ButtonFsub:
    async def fsub_button(self: 'techgram.Client', m: 'types.Message', starter: bool = False):
        keyboard = []
        temp = []
        new_keyboard = []
        if starter:
            new_keyboard.append(
                [
                    types.InlineKeyboardButton(
                        text="ᴛᴇɴᴛᴀɴɢ sᴀʏᴀ",
                        callback_data="tentang",
                    )
                ]
            )
        for x in self._fsub:
            try:
                info = await self.get_chat(int(x))
            except errors.ChannelInvalid:
                await m.reply(f'[ERROR] - Silahkan jadikan saya admin di {int(x)}')
                return
            except errors.ChatWriteForbidden:
                await m.reply(f'[ERROR] - Silahkan jadikan saya admin di {int(x)}')
                return
            except Exception as e:
                await m.reply(f'[ERROR] - Silahkan jadikan saya admin di {int(x)}')
                return
            text_btn = (
                'ɢʀᴏᴜᴘ' if info.type in [
                    techgram.enums.ChatType.GROUP,
                    techgram.enums.ChatType.SUPERGROUP
                ]
                else 'ᴄʜᴀɴɴᴇʟ' if info.type == techgram.enums.ChatType.CHANNEL
                else 'ᴊᴏɪɴ ᴅᴜʟᴜ'
            )
            if info.username:
                link = f'https://t.me/{info.username}'
            if info.invite_link:
                link = info.invite_link
            else:
                link = await self.export_chat_invite_link(x)
            keyboard.append(types.InlineKeyboardButton(text_btn, url=link))
        for i, board in enumerate(keyboard, start=1):
            temp.append(board)
            if i % 2 == 0:
                new_keyboard.append(temp)
                temp = []
            if i == len(keyboard):
                new_keyboard.append(temp)
        if starter:
            new_keyboard.append(
                [
                    types.InlineKeyboardButton(
                        text="ᴛᴜᴛᴜᴘ",
                        callback_data="tutup",
                    )
                ]
            )
        else:
            try:
                new_keyboard.append(
                    [
                        types.InlineKeyboardButton(
                            "ᴄᴏʙᴀ ʟᴀɢɪ",
                            url=f"https://t.me/{self.me.username}?start={m.command[1]}",
                        )
                    ]
                )
            except IndexError:
                pass
        return new_keyboard