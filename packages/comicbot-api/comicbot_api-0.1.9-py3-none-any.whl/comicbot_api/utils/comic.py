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
        self.link_suffix = kwargs.pop('link_suffix', "")
        print(self.link_suffix)
        self.title = kwargs.pop('title', "")
        self.base_url = kwargs.pop('base_url', "")
        print(self.base_url)
        if 'base_url' in kwargs or 'link_suffix' in kwargs:
            self.url = self.base_url + self.link_suffix
        else:
            self.url = kwargs.pop('url', '')
        self.image_url = ""

    def get_link(self) -> str:
        return self.base_url + self.link_suffix

    def __repr__(self):
        return pprint.pformat(dataclasses.asdict(self))
