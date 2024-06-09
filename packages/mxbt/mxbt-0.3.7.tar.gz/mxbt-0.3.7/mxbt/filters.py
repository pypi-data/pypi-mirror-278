from enum import Enum
from typing import Callable
from nio import MatrixRoom

from .types.msgtype import MsgType
from .context import Context
from .match import Match

class BaseFilter:

    @staticmethod
    def __find_context(args) -> Context | None:
        for arg in args:
            if isinstance(arg, Context):
                return arg
    
    @staticmethod
    def __find_context_body(args) -> tuple | None:
        for index, arg in enumerate(args):
            if isinstance(arg, MatrixRoom):
                return args[index:]

    def filter(self):
        def wrapper(func):
            async def command_func(*args) -> None:
                ctx = BaseFilter.__find_context(args)
                if ctx:
                    await self.action(ctx.room, ctx.event,func,*args)
                else:
                    body = BaseFilter.__find_context_body(args)
                    if not body: return
                    room, event = body
                    await self.action(room, event,func,*args)
            return command_func
        return wrapper

    async def action(self, room: MatrixRoom, event, func, *args):
        await func(*args)

class IncludeExcludeFilter(BaseFilter):
    
    def __init__(
            self,
            checker: Callable,
            include: list[str] | None=None,
            exclude: list[str] | None=None,
            ) -> None:
        """
        Params:
            include: list[str] | None -> list of included items 
            exclude: list[str] | None -> list of excluded items
        """
        self.checker = checker
        self.include = include
        self.exclude = exclude

    async def action(self, room: MatrixRoom, event, func, *args) -> None:
        if self.include:
            if not self.checker(room.room_id, self.include):
                return
        
        if self.exclude:
            if self.checker(room.room_id, self.exclude):
                return

        await func(*args)

class RoomsFilter(IncludeExcludeFilter):

    def __init__(self, 
                 include: list[str] | None=None,
                 exclude: list[str] | None=None) -> None:
        """
        Params:
            include: list[str] | None -> list of included rooms 
            exclude: list[str] | None -> list of excluded rooms
        """
        super().__init__(
            Match.is_from_rooms,
            include,
            exclude
        )

class UserFilter(IncludeExcludeFilter):

    def __init__(self, 
                 include: list[str] | None=None,
                 exclude: list[str] | None=None) -> None:
        """
        Params:
            include: list[str] | None -> list of included users 
            exclude: list[str] | None -> list of excluded users
        """
        super().__init__(
            Match.is_from_users,
            include,
            exclude
        )

class SenderFilter(BaseFilter):

    def __init__(self, 
                 can_ban: bool | None=None,
                 can_kick: bool | None=None,
                 can_invite: bool | None=None,
                 can_delete: bool | None=None,
                 power_level: int | None=None) -> None:
        """
        Params:
            can_ban: bool | None -> Can sender ban other users or not 
            can_kick: bool | None -> Can sender kick other users or not 
            can_invite: bool | None -> Can sender invite other users or not 
            can_delete: bool | None -> Can sender delete events or not 
            power_level: int | None -> Has sender power level or not 
        """
        self.can_ban = can_ban
        self.can_kick = can_kick
        self.can_invite = can_invite
        self.can_delete = can_delete
        self.power_level = power_level

    async def action(self, room: MatrixRoom, event, func, *args):
        items = {
            Match.can_ban : self.can_ban,
            Match.can_kick : self.can_kick,
            Match.can_invite : self.can_invite,
            Match.can_delete_events : self.can_delete
        }

        result = False
        for method, value in items.items():
            if value is None: continue
            else:
                if value and method(room, event.sender):
                    result = True
                elif not value and not method(room, event.sender):
                    result = True
                else:
                    return
        
        if not self.power_level is None:
            if Match.has_power_level(
                room, event.sender,
                self.power_level):
                result = True
            else: return

        if result: await func(*args)

class MessageFilter(BaseFilter):

    def __init__(self, 
                 has_text: list[str] | None=None,
                 msgtype: list[str | MsgType] | None=None) -> None:
        """
        Params:
            has_text: list[str] | None -> List of text which needs to be in message
            msgtype: list[str | MsgType] | None -> List of accepted message types
        """
        self.has_text = has_text
        self.msgtype = msgtype
        
        if self.msgtype:
            self.__msgtype_values = list()
            for value in self.msgtype:
                if isinstance(value, Enum):
                    self.__msgtype_values.append(value.value)
                else:
                    self.__msgtype_values.append(value)

    async def action(self, room: MatrixRoom, event, func, *args):
        if self.has_text:
            if not Match.has_text(event.body, self.has_text):
                return

        if self.msgtype:
            if not event.source['content']['msgtype'] in self.__msgtype_values:
                return

        await func(*args)

