from dataclasses import dataclass, field
from typing import List, Optional

from nio import AsyncClient, RoomGetStateEventResponse

@dataclass
class Emote:
    name: str
    url: str

@dataclass
class EmotesPack:
    name: str=""
    emotes: List[Emote]=field(
        default_factory=lambda: list()
    )

    @classmethod
    def from_dict(cls, pack_name: str, data: dict) -> "EmotesPack":
        emotes = list()
        for name, value in data.items():
            emotes.append(Emote(name, value['url']))
        return cls(pack_name, emotes)

@dataclass
class RoomEmotes:
    room_id: str=""
    packs: List[EmotesPack]=field(
        default_factory=lambda: list()
    )

    @classmethod
    async def from_dict(cls, client: AsyncClient, room_id: str, packs: dict) -> "RoomEmotes":
        loaded_packs = list()
        for pack in packs.keys():
            result = await client.room_get_state_event(
                room_id, 'im.ponies.room_emotes', pack
            )
            if isinstance(result, RoomGetStateEventResponse):
                loaded_packs.append(
                    EmotesPack.from_dict(
                        pack,result.content['images']
                    )
                )

        return cls(room_id, loaded_packs)

@dataclass
class Emotes:
    user_emotes: Optional[EmotesPack]=None
    rooms_emotes: List[RoomEmotes]=field(
        default_factory=lambda: list()
    )

    def load_user_emotes(self, data: dict) -> None:
        self.user_emotes = EmotesPack.from_dict("", data['images'])

    async def load_rooms_emotes(self, client: AsyncClient, data: dict) -> None:
        for room_id, packs in data['rooms'].items():
            room_emotes = await RoomEmotes.from_dict(
                client, room_id, packs
            )
            self.rooms_emotes.append(room_emotes)
    
    def find_user_emote(self, name: str) -> Optional[Emote]:
        if not self.user_emotes: return 
        for emote in self.user_emotes.emotes:
            if emote.name == name:
                return emote

    def find_rooms_emote(self, name: str) -> Optional[Emote]:
        for room_emotes in self.rooms_emotes:
            for pack in room_emotes.packs:
                for emote in pack.emotes:
                    if emote.name == name:
                        return emote

    def find(self, name: str) -> Optional[Emote]:
         return self.find_user_emote(name) or self.find_rooms_emote(name)

    def get_all(self) -> list[Emote]:
        emotes = list()
        if self.user_emotes:
            for emote in self.user_emotes.emotes:
                emotes.append(emote)
        for room_emotes in self.rooms_emotes:
            for pack in room_emotes.packs:
                for emote in pack.emotes:
                    emotes.append(emote)
        return emotes

    def get_all_names(self) -> list[str]:
        emotes = self.get_all()
        return [emote.name for emote in emotes]

    def get_all_urls(self) -> list[str]:
        emotes = self.get_all()
        return [emote.url for emote in emotes]

