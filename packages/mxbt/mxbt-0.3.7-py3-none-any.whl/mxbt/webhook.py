from typing import Optional
import aiohttp

class WebHook:

    def __init__(self, homeserver: str, access_token: str) -> None:
        self.homeserver = homeserver
        self.access_token = access_token

        self.base_url = "{homeserver}/_matrix/client/r0/rooms/{room_id}/send/m.room.message"

    async def send_text(self, room_id: str, body: str, msgtype: str="m.notice", webhook_data: dict=dict()) -> Optional[dict | list]:
        url = self.base_url.format(
            homeserver=self.homeserver,
            room_id=room_id,
        )

        data = {
            "body" : body,
            "format" : "org.matrix.custom.html",
            "formatted_body" : body,
            "msgtype" : msgtype,
            "webhook_data" : webhook_data 
        }

        headers = {
            'Authorization' : f'Bearer {self.access_token}',
            'Content-Type' : 'application/json'
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data, headers=headers) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    print(await response.text())


