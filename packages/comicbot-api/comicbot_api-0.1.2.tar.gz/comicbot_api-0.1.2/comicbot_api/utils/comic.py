import dataclasses
import pprint
from dataclasses import dataclass


@dataclass(repr=False, init=False)
class Comic:
    link_suffix: str
    title: str
    base_url: str
    url: str
    image_url: str

    def __init__(self, **kwargs):
        self.link_suffix = kwargs['link_suffix']
        self.title = kwargs['title']
        self.base_url = kwargs['base_url']
        self.url = kwargs['base_url'] + kwargs['link_suffix']
        self.image_url = ""

    def get_link(self) -> str:
        return self.base_url + self.link_suffix

    def __repr__(self):
        return pprint.pformat(dataclasses.asdict(self))
