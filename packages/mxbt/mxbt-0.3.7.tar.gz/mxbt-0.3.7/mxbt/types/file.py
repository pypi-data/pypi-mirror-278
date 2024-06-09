from nio import AsyncClient, UploadError
from enum import Enum
from PIL import Image
from io import BytesIO
import aiofiles.os
import mimetypes
import filetype
import aiofiles
import os

from ..utils import error

class FileType(Enum):
    Image = 0
    Video = 1
    Other = 2

class File:

    def __init__(self, path: str, caption: str="") -> None:
        self.path = path
        self.filename = os.path.basename(self.path)
        self.caption = caption
        self.mime_type = self.guess_mimetype()

        if filetype.is_image(path):
            self.filetype = FileType.Image
        elif filetype.is_video(path):
            self.filetype = FileType.Video
        else:
            self.filetype = FileType.Other

    def is_image(self) -> bool:
        return self.filetype == FileType.Image

    def is_video(self) -> bool:
        return self.filetype == FileType.Video

    def is_regular_file(self) -> bool:
        return self.filetype == FileType.Other

    def guess_mimetype(self) -> str | None:
        return mimetypes.guess_type(self.path)[0]

    async def upload(self, async_client) -> dict | None:
        """
        Upload file to Matrix server, returns base dict with file content

        Parameters:
        -------------
        async_client: nio.AsyncClient - Async Matrix client for uploading file
        """
        if self.filetype == FileType.Image:
            return await self.__upload_image(async_client)
        elif self.filetype == FileType.Video:
            return await self.__upload_video(async_client)
        elif self.filetype == FileType.Other:
            return await self.__upload_regular_file(async_client)

    async def __upload_to_server(self, async_client, file_stat) -> tuple:
        async with aiofiles.open(self.path, "r+b") as file:
            resp, maybe_keys = await async_client.upload(
                file,
                content_type=self.mime_type,
                filename=self.filename,
                filesize=file_stat.st_size)
        return resp, maybe_keys

    async def __upload_regular_file(self, async_client) -> dict | None:
        file_stat = await aiofiles.os.stat(self.path)
        resp, _ = await self.__upload_to_server(async_client, file_stat)
        if isinstance(resp, UploadError):
            error(f"Failed Upload Response: {resp}")
            return

        return {
            "body" : self.caption,
            "filename" : self.filename,
            "format": "org.matrix.custom.html",
            "formatted_body" : self.caption,
            "info" : {
                "mimetype" : self.mime_type,
                "size" : file_stat.st_size
            },
            "msgtype" : "m.file",
            "url" : resp.content_uri
        }

    async def __upload_image(self, async_client) -> dict | None:
        image = Image.open(self.path)
        (width, height) = image.size

        file_stat = await aiofiles.os.stat(self.path)
        resp, _ = await self.__upload_to_server(async_client, file_stat)
        if isinstance(resp, UploadError):
            error(f"Failed Upload Response: {resp}")
            return

        return {
            "body": self.caption,
            "filename" : self.filename,
            "format": "org.matrix.custom.html",
            "formatted_body" : self.caption,
            "info": {
                "size": file_stat.st_size,
                "mimetype": self.mime_type,
                "thumbnail_info": None,
                "w": width,
                "h": height,
                "thumbnail_url": None
            },
            "msgtype": "m.image",
            "url": resp.content_uri
        }

    async def __upload_video(self, async_client) -> dict | None:
        file_stat = await aiofiles.os.stat(self.path)
        resp, _ = await self.__upload_to_server(async_client, file_stat)
        if isinstance(resp, UploadError):
            error(f"Failed Upload Response: {resp}")
            return

        return {
            "body": self.caption,
            "filename" : self.filename,
            "format": "org.matrix.custom.html",
            "formatted_body" : self.caption,
            "info": {
                "size": file_stat.st_size,
                "mimetype": self.mime_type,
                "thumbnail_info": None,
                "w" : 360, # TODO: Grep real width and height
                "h" : 640
            },
            "msgtype": "m.video",
            "url": resp.content_uri
        }

class FileUrl:

    def __init__(self, url: str, filename: str="image.png", caption: str="", inline: bool=True) -> None:
        self.url = url
        self.filename = filename
        self.caption = caption
        self.inline = inline
        self.mime_type = ""
        self.size = 0

        self.filetype = FileType.Other

    def is_mxc(self) -> bool:
        return self.url.startswith('mxc://')

    async def read(self, async_client: AsyncClient) -> tuple[bytes, str, int]:
        """
        Read external file by self.url and return file bytes, mimetype and size
        """
        url = self.url
        if self.is_mxc():
            url = await async_client.mxc_to_http(self.url)
            if url is None: return bytes(), str(), int()
        session = async_client.client_session

        result: bytes = bytes()
        mimetype: str = ""
        size: int = 0
        if session:
            async with session.get(url) as response:
                if response.status == 200:
                    result = await response.content.read()
                    mimetype = response.content_type
                    if response.content_length:
                        size = response.content_length
        return result, mimetype, size

    async def upload_to_server(self, file: bytes, async_client: AsyncClient) -> str | None:
        resp, _ = await async_client.upload(
            BytesIO(file),
            content_type=self.mime_type,
            filename=self.filename,
            filesize=self.size
        )
        if isinstance(resp, UploadError):
            error(f"Failed Upload Response: {resp}")
            return None
        return resp.content_uri

    async def get_urls(self, file: bytes, async_client: AsyncClient) -> tuple[str | None, str | None]:
        """
        Get and return mxc:// file url and external file url if exists
        """
        url = ""
        external_url = None
        if self.is_mxc():
            url = self.url
        else:
            external_url = self.url
            url = await self.upload_to_server(file, async_client)
        return url, external_url

    async def to_image(self, file: bytes, async_client: AsyncClient) -> dict | None:
        image = Image.open(BytesIO(file))
        width, height = image.size

        url, external_url = await self.get_urls(file, async_client)
        
        data = {
            "body": self.caption,
            "filename" : self.filename,
            "format": "org.matrix.custom.html",
            "formatted_body" : self.caption,
            "info": {
                "size": self.size,
                "mimetype": self.mime_type,
                "thumbnail_info": None,
                "w": width,
                "h": height,
                "thumbnail_url": None
            },
            "msgtype": "m.image",
            "url": url
        }

        if external_url:
            data['external_url'] = external_url

        return data

    async def to_video(self, file: bytes, async_client: AsyncClient) -> dict | None:
        url, external_url = await self.get_urls(file, async_client)

        data = {
            "body": self.caption,
            "filename" : self.filename,
            "format": "org.matrix.custom.html",
            "formatted_body" : self.caption,
            "info": {
                "size": self.size,
                "mimetype": self.mime_type,
                "thumbnail_info": None,
                "w": 360, # TODO: Grep real width and height
                "h" : 640
            },
            "msgtype": "m.video",
            "url": url
        }

        if external_url:
            data['external_url'] = external_url

        return data

    async def to_regular(self, file: bytes, async_client: AsyncClient) -> dict | None:
        url, external_url = await self.get_urls(file, async_client)

        data = {
            "body" : self.caption,
            "filename" : self.filename,
            "format": "org.matrix.custom.html",
            "formatted_body" : self.caption,
            "info" : {
                "mimetype" : self.mime_type,
                "size" : self.size,
            },
            "msgtype" : "m.file",
            "url" : url 
        }

        if external_url:
            data['external_url'] = external_url

        return data

    def guess_type(self, file: bytes) -> None:
        if filetype.is_image(file):
            self.filetype = FileType.Image
        elif filetype.is_video(file):
            self.filetype = FileType.Video
        else:
            self.filetype = FileType.Other

    async def to_file(self, async_client: AsyncClient) -> dict | None:
        """
        Return full content dict for this file with automatically generated content type
        """
        file, self.mime_type, self.size = await self.read(async_client)
        self.guess_type(file) 

        if self.filetype == FileType.Image:
            return await self.to_image(file, async_client)
        elif self.filetype == FileType.Video:
            return await self.to_video(file, async_client)
        elif self.filetype == FileType.Other:
            return await self.to_regular(file, async_client)

    def to_html(self) -> str:
        if self.filetype == FileType.Image:
            return self.__image_to_html()
        else:
            return self.filename 
    
    def __image_to_html(self) -> str:
        return f'<img alt="{self.filename}" title="{self.filename}" height="32" src="{self.url}" data-mx-emoticon/>'

