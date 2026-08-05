#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#
#  This file is part of Pyrogram.
#
#  Pyrogram is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pyrogram is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pyrogram.  If not, see <http://www.gnu.org/licenses/>.

from typing import Optional

from pyrogram import enums, raw, types
from ..object import Object


class KeyboardButton(Object):
    """One button of the reply keyboard.
    For simple text buttons String can be used instead of this object to specify text of the button.
    Optional fields are mutually exclusive.

    Parameters:
        text (``str``):
            Text of the button. If none of the optional fields are used, it will be sent as a message when
            the button is pressed.

        icon_custom_emoji_id (``str``, *optional*):
            Custom emoji icon displayed before the button text.

        style (:obj:`~pyrogram.enums.ButtonStyle`, *optional*):
            Style (background color) of the button. If omitted, an app-specific style is used.

        request_contact (``bool``, *optional*):
            If True, the user's phone number will be sent as a contact when the button is pressed.
            Available in private chats only.

        request_location (``bool``, *optional*):
            If True, the user's current location will be sent when the button is pressed.
            Available in private chats only.

        web_app (:obj:`~pyrogram.types.WebAppInfo`, *optional*):
            If specified, the described `Web App <https://core.telegram.org/bots/webapps>`_ will be launched when the
            button is pressed. The Web App will be able to send a “web_app_data” service message. Available in private
            chats only.

    """

    def __init__(
        self,
        text: str,
        icon_custom_emoji_id: Optional[str] = None,
        style: "enums.ButtonStyle" = enums.ButtonStyle.PRIMARY,
        *,
        request_contact: bool = None,
        request_location: bool = None,
        web_app: "types.WebAppInfo" = None
    ):
        super().__init__()

        self.text = str(text)
        self.request_contact = request_contact
        self.request_location = request_location
        self.web_app = web_app
        self.icon_custom_emoji_id = icon_custom_emoji_id
        self.style = style

    @staticmethod
    def read(b):
        raw_style: "raw.types.KeyboardButtonStyle" = b.style
        button_style = enums.ButtonStyle.DEFAULT
        icon_custom_emoji_id = None

        if raw_style is not None:
            if raw_style.bg_primary:
                button_style = enums.ButtonStyle.PRIMARY
            elif raw_style.bg_danger:
                button_style = enums.ButtonStyle.DANGER
            elif raw_style.bg_success:
                button_style = enums.ButtonStyle.SUCCESS
            if raw_style.icon:
                icon_custom_emoji_id = str(raw_style.icon)

        if isinstance(b, raw.types.KeyboardButton):
            if button_style == enums.ButtonStyle.DEFAULT and not icon_custom_emoji_id:
                return b.text
            return KeyboardButton(
                text=b.text,
                style=button_style,
                icon_custom_emoji_id=icon_custom_emoji_id
            )

        if isinstance(b, raw.types.KeyboardButtonRequestPhone):
            return KeyboardButton(
                text=b.text,
                request_contact=True,
                style=button_style,
                icon_custom_emoji_id=icon_custom_emoji_id
            )

        if isinstance(b, raw.types.KeyboardButtonRequestGeoLocation):
            return KeyboardButton(
                text=b.text,
                request_location=True,
                style=button_style,
                icon_custom_emoji_id=icon_custom_emoji_id
            )

        if isinstance(b, raw.types.KeyboardButtonSimpleWebView):
            return KeyboardButton(
                text=b.text,
                web_app=types.WebAppInfo(
                    url=b.url
                ),
                style=button_style,
                icon_custom_emoji_id=icon_custom_emoji_id
            )

    def write(self):
        raw_style = raw.types.KeyboardButtonStyle(
            bg_primary=self.style == enums.ButtonStyle.PRIMARY,
            bg_danger=self.style == enums.ButtonStyle.DANGER,
            bg_success=self.style == enums.ButtonStyle.SUCCESS,
            icon=int(self.icon_custom_emoji_id) if self.icon_custom_emoji_id else None
        )

        if self.request_contact:
            return raw.types.KeyboardButtonRequestPhone(text=self.text, style=raw_style)
        elif self.request_location:
            return raw.types.KeyboardButtonRequestGeoLocation(text=self.text, style=raw_style)
        elif self.web_app:
            return raw.types.KeyboardButtonSimpleWebView(text=self.text, url=self.web_app.url, style=raw_style)
        else:
            return raw.types.KeyboardButton(text=self.text, style=raw_style)
