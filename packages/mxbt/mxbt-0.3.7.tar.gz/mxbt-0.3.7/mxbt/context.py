from nio import (MatrixRoom, Event, RoomMessage, RoomMessageAudio,
                 RoomMessageEmote, RoomMessageFile,
                 RoomMessageFormatted, RoomMessageImage,
                 RoomMessageNotice, RoomMessageText,
                 RoomMessageVideo)
from dataclasses import dataclass, field
from typing import List, Optional

from .types.mediainfo import MediaInfo
from .types.command import Command
from .types.file import File, FileUrl
from .bot import Bot

@dataclass
class Context:
    """
    Event context class

    Parameters:
    -------------
    bot: mxbt.Bot
        Bot object for sending events
    room: nio.MatrixRoom
        Event room object
    event: nio.Event
        Event object
    sender: str
        User id of event author
    event_id: str
        Id of received event
    body: str
        Body of received event
    command: Optional[mxbt.Command]
        Command object with args, prefix and aliases
    relates_to: Optional[str]
        event id of replied message
    mentions: list[str], optional
        List of all mentioned users in event
    media_info: Optional[mxbt.MediaInfo] 
        Dict with media file info
    """
    bot: Bot 
    room: MatrixRoom
    room_id: str
    event: Event
    sender: str
    event_id: str
    body: str=str()
    command: Optional[Command]=None
    relates_to: Optional[str]=None
    mentions: List[str]=field(
        default_factory=lambda: list()
    )
    media_info: Optional[MediaInfo]=None

    async def _pack_result(self, result) -> Optional["Context"]:
        if result is None: return None 
        room_id, event = result

        if isinstance(event, RoomMessageText):
            return Context.from_text(self.bot, room_id, event)
        else:
            return Context.from_media(self.bot, room_id, event)

    async def send(self, body: str | File | FileUrl,
                   use_html: bool=False,
                   mentions: list[str]=list(),
                   emotes: list[str]=list()) -> Optional["Context"]:
        """
        Send text or file to context room

        Parameters:
        -------------
        body: str | mxbt.types.File
            Text of message or File object to send
        use_html: bool, optional
            Use html formatting or not
        """
        result = await self.bot.send(
            self.room_id,
            body,
            use_html,
            mentions,
            emotes
        )
        return await self._pack_result(result)

    async def reply(self, body: str | File | FileUrl,
                    use_html: bool=False,
                    mentions: list[str]=list(),
                    emotes: list[str]=list()) -> Optional["Context"]:
        """
        Reply context message with text or file

        Parameters:
        -------------
        body: str | mxbt.types.File
            Text of message or File object to send
        use_html: bool, optional
            Use html formatting or not
        """
        result = await self.bot.reply(
            self.room_id,
            body,
            self.event_id,
            use_html,
            mentions,
            emotes
        )
        return await self._pack_result(result) 

    async def edit(self, body: str | File | FileUrl,
                   use_html: bool=False,
                   mentions: list[str]=list(),
                   emotes: list[str]=list()) -> Optional["Context"]:
        """
        Edit context message with text or file

        Parameters:
        -------------
        body: str | mxbt.types.File
            Text of message or File object to send
        use_html: bool, optional
            Use html formatting or not
        """
        result = await self.bot.edit(
            self.room_id,
            body,
            self.event_id,
            use_html,
            mentions,
            emotes
        )
        return await self._pack_result(result)

    async def delete(self, reason: str | None=None):
        """
        Delete context event

        Parameters:
        -------------
        reason: str | None - optional
            Reason, why message is deleted
        """
        return await self.bot.delete(
            self.room.room_id,
            self.event.event_id,
            reason
        )
    
    async def react(self, body: str) -> Optional[Event]:
        """
        Send reaction to context message.

        Parameters:
        --------------
        body : str
            Reaction emoji.
        """
        return await self.bot.send_reaction(
            self.room.room_id,
            self.event.event_id,
            body
        )

    async def ban(self, reason: str | None=None):
        """
        Ban sender of this event

        Parameters:
        -------------
        reason: str | None - optional
            Reason, why sender is banned
        """
        return await self.bot.ban(
            self.room.room_id,
            self.sender,
            reason
        )

    async def kick(self, reason: str | None=None):
        """
        Kick sender of this event

        Parameters:
        -------------
        reason: str | None - optional
            Reason, why sender is kicked
        """
        return await self.bot.kick(
            self.room.room_id,
            self.sender,
            reason
        )

    async def typing(self, state: bool=True, timeout: int=30000):
        """
        Send typing notice to context room

        Parameters:
            typing_state (bool): A flag representing whether the user started
                or stopped typing.
            timeout (int): For how long should the new typing notice be
                valid for in milliseconds.
        """
        return await self.bot.typing(
            self.room_id, state, timeout
        )

    @staticmethod
    def __parse_command(message: RoomMessageText, prefix: str, aliases: list) -> Command:
        command = Command(prefix, aliases)
        args = message.body.split(" ")
        args = args[1:] if len(args) > 1 else list()
        command.args = args
        command.substring = ' '.join(args)
        return command

    @staticmethod
    def __parse_mentions(message: RoomMessageText | RoomMessageNotice | RoomMessageEmote | RoomMessageFormatted) -> list:
        mentions = list()
        content = message.source['content']
        if 'm.mentions' in content.keys():
            if 'user_ids' in content['m.mentions'].keys():
                mentions = content['m.mentions']['user_ids']
        return mentions

    @staticmethod
    def __parse_relations(message: RoomMessage) -> Optional[str]:
        content = message.source['content']
        if 'm.relates_to' in content.keys():
            if 'm.in_reply_to' in content['m.relates_to'].keys():
                return content['m.relates_to']['m.in_reply_to']['event_id']

    @staticmethod
    def from_command(bot: Bot, room: MatrixRoom, message: RoomMessageText, prefix: str, aliases: list) -> "Context":
        command = Context.__parse_command(message, prefix, aliases)
        relates_to = Context.__parse_relations(message)
        mentions = Context.__parse_mentions(message)
        return Context(
            bot=bot,
            room=room, 
            room_id=room.room_id,
            event=message,
            sender=message.sender,
            event_id=message.event_id,
            body=message.body,
            command=command,
            relates_to=relates_to,
            mentions=mentions
        )

    @classmethod
    def from_text(cls, bot: Bot, room: MatrixRoom, message: RoomMessageText | RoomMessageNotice | RoomMessageEmote | RoomMessageFormatted) -> "Context":
        relates_to = Context.__parse_relations(message)
        mentions = cls.__parse_mentions(message)
        return cls(
            bot=bot,
            room=room,
            room_id=room.room_id,
            event=message,
            sender=message.sender,
            event_id=message.event_id,
            body=message.body,
            relates_to=relates_to,
            mentions=mentions
        )

    @classmethod
    def from_media(cls, bot: Bot,
                   room: MatrixRoom,
                   message: RoomMessageImage | RoomMessageVideo | RoomMessageFile | RoomMessageAudio) -> "Context":
        relates_to = Context.__parse_relations(message)
        return cls(
            bot=bot,
            room=room,
            room_id=room.room_id,
            event=message,
            sender=message.sender,
            event_id=message.event_id,
            body=message.body,
            relates_to=relates_to,
            media_info=MediaInfo.from_json(message.source['content'])
        )


