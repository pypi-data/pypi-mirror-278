from nio import (MatrixRoom, ReactionEvent, RedactedEvent,
                 RedactionEvent, RoomMessageAudio,
                 RoomMessageEmote, RoomMessageFile,
                 RoomMessageFormatted, RoomMessageImage,
                 RoomMessageNotice, RoomMessageText,
                 RoomMessage, InviteMemberEvent,
                 RoomMessageVideo, StickerEvent)

from .types.command import Command
from .context import Context
from .module import Module
from .match import Match
from .utils import info

from inspect import isclass
import importlib
import os

class Listener:

    def __init__(self, bot) -> None:
        self._bot = bot
        self._registry = list()
        self._startup_registry = list()
        self._commands = list()

    def mount_module(self, module: str) -> None:
        """
        Mount module by module name (without .py):
            {modules_dir}.{filename}
        Example:
            modules.help
        """
        mod_file = importlib.import_module(module)
        for it in dir(mod_file):
            obj = getattr(mod_file, it)
            if isclass(obj) and issubclass(obj, Module) and obj != Module:
                info(f"Setup {obj.__name__} module")
                obj(self._bot, self)

    def mount_modules(self, dirpath: str) -> None:
        """
        Mount all modules in dir

        Parameters:
        -------------
        dirpath: str - Path to modules directory.
        """
        dirname = os.path.basename(dirpath)
        for filename in os.listdir(dirpath):
            if filename.endswith(".py"):
                self.mount_module(f"{dirname}.{filename[:-3]}")

    async def startup(self) -> None:
        for action in self._startup_registry:
            for room_id in self._bot.async_client.rooms:
                await action(room_id)

    async def start_polling(self) -> None:
        await self._bot.connect(self)

    def _reg_command(self, prefix: str, aliases: list[str]) -> None:
        self._commands.append(Command(prefix, aliases))

    def _reg_event(self, func, event) -> None:
        self._registry.append([func, event])

    def _get_command_prefix(self, **kwargs) -> str:
        if not 'prefix' in kwargs.keys():
            return self._bot.config.prefix
        else:
            return kwargs['prefix']

    def _get_command_name(self, prefix: str, body: str) -> str:
        return body.split(" ")[0].replace(prefix, "")

    def get_commands(self) -> list:
        return self._commands.copy()

    def on_custom_event(self, event):

        def wrapper(func) -> None:
            if [func, event] in self._registry:
                func()
            else:
                self._reg_event(func, event)

        return wrapper

    def on_message(self, func) -> None:
        """
        on_message event listener

        func params:
        --------------
        room: MatrixRoom
        event: RoomMessage
        """
        async def wrapper(room: MatrixRoom, event: RoomMessage) -> None:
            if isinstance(event, (RoomMessageImage, RoomMessageAudio, RoomMessageVideo, RoomMessageFile)):
                await func(Context.from_media(self._bot, room, event))
            elif isinstance(event, (RoomMessageText, RoomMessageNotice, RoomMessageEmote, RoomMessageFormatted)):
                await func(Context.from_text(self._bot, room, event)) 
        self._reg_event(wrapper, RoomMessage)

    def on_member_join(self, func) -> None:
        """
        on_member_join event listener

        func params:
        --------------
        room: MatrixRoom
        event: InviteMemberEvent
        """
        async def wrapper(room: MatrixRoom, event: InviteMemberEvent) -> None:
            if event.membership == 'join':
                await func(room, event)
        self._reg_event(wrapper, InviteMemberEvent)

    def on_member_leave(self, func) -> None:
        """
        on_member_leave event listener

        func params:
        --------------
        room: MatrixRoom
        event: InviteMemberEvent
        """
        async def wrapper(room: MatrixRoom, event: InviteMemberEvent) -> None:
            if event.membership == 'leave':
                await func(room, event)
        self._reg_event(wrapper, InviteMemberEvent)

    def on_command(self, **kwargs):
        """
        Custom on_command event listener

        listener params:
        ------------------
        aliases: list[str] - list of command aliases
        prefix: str, optional - custom command prefix (empty - use standart bot prefix)

        func params:
        ------------------
        ctx: mxbt.Context
        """
        def wrapper(func):
            prefix = self._get_command_prefix(**kwargs) 
            self._reg_command(prefix, kwargs['aliases'])

            async def command_func(room, event: RoomMessageText) -> None:
                if not event.body.startswith(prefix):
                    return

                match = Match(room, event, self._bot)
                name = self._get_command_name(prefix, event.body)
                if name in kwargs['aliases']:
                    if self._bot.config.selfbot:
                        if not match.is_from_self():
                            return
                    else:
                        if match.is_from_self():
                            return
                    await func(Context.from_command(self._bot, room, event, prefix, kwargs['aliases']))
            self._reg_event(command_func, RoomMessageText)
            return command_func
        return wrapper

    def on_redaction(self, func) -> None:
        """
        on_redaction event listener

        func params:
        --------------
        room: MatrixRoom
        event: Event
            redacted event
        """
        async def wrapper(room: MatrixRoom, event: RedactionEvent) -> None:
            e = await self._bot.async_client.room_get_event(
                room.room_id, event.redacts
            )
            await func(room, e.event)

        self._reg_event(wrapper, RedactionEvent)

    def on_redact_reaction(self, func) -> None:
        """
        on_redact_reaction event listener

        func params:
        --------------
        room: MatrixRoom
        event: ReactionEvent
        """
        async def wrapper(room: MatrixRoom, event: RedactionEvent) -> None:
            e = await self._bot.async_client.room_get_event(room.room_id, event.redacts)
            redacted: RedactedEvent = e.event
            if redacted.type == 'm.reaction':
                await func(room, redacted)

        self._reg_event(wrapper, RedactionEvent)

    def on_reaction(self, func) -> None:
        """
        on_reaction event listener

        func params:
        --------------
        room: MatrixRoom
        event: ReactionEvent
        key: str
            Reaction emoji
        """
        async def wrapper(room: MatrixRoom, event: ReactionEvent) -> None:
            await func(room, event, event.key)

        self._reg_event(wrapper, ReactionEvent)

    def on_sticker(self, func) -> None:
        """
        on_sticker event listener

        func params:
        --------------
        room: MatrixRoom
        event: StickerEvent 
        url: str
            Sticker image url
        """
        async def wrapper(room: MatrixRoom, event: StickerEvent) -> None:
            await func(room, event, event.url)

        self._reg_event(wrapper, StickerEvent)

    def on_startup(self, func) -> None:
        if func in self._startup_registry:
            func()
        else:
            self._startup_registry.append(func)


