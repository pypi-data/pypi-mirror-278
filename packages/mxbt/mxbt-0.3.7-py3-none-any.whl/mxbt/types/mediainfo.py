from dataclasses import dataclass

@dataclass
class MediaInfo:

    filename: str
    caption: str | None
    url: str
    external_url: str | None
    width: int
    height: int 
    mimetype: str
    size: int

    @classmethod
    def from_json(cls, data: dict):
        if not 'info' in data.keys():
            return None
        return cls(
            data['filename'] if 'filename' in data.keys() else data['body'],
            data['body'] if 'filename' in data.keys() else None,
            data['url'],
            data['external_url'] if 'external_url' in data.keys() else None,
            data['info']['w'],
            data['info']['h'],
            data['info']['mimetype'],
            data['info']['size']
        )


