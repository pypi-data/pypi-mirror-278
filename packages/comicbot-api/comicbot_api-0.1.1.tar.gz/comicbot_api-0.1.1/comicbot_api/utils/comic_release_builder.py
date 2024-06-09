from dataclasses import dataclass, field
from typing import List
from functools import reduce

PUBLISHERS = {
    'dc': 1,
    'marvel': 2,
    'dark-horse': 5,
    'image': 7,
    'dynamite': 12,
    'boom-studios': 13,
    'oni-press': 29,
}

FORMATS = {
    'single-issue': 1,
    'tradepaperback': 3,
    'hardcover': 4
}


def resolve_url_param_type(translation_dict, param_type, selected_params) -> str:
    if selected_params:
        return reduce(lambda param_string, param:
                      param_string + f'&{param_type}[]={translation_dict[param]}',
                      selected_params, '')
    return ''


def print_publisher_options():
    print(PUBLISHERS.keys())


def print_format_options():
    print(FORMATS.keys())


@dataclass
class ComicReleaseURLBuilder:
    date: str
    publishers: List = field(default_factory=lambda: [])
    formats: List = field(default_factory=lambda: [])
    base_url: str = None
    base_url_params: List = field(
        default_factory=lambda: ['view=text', 'list=releases', 'date_type=week'])

    def resolve_base_params(self):
        return '?' + '&'.join(self.base_url_params)

    def build(self) -> str:
        return self.base_url + self.resolve_base_params() + f'&date={self.date}' + \
            resolve_url_param_type(FORMATS, 'format', self.formats) + \
            resolve_url_param_type(PUBLISHERS, 'publisher', self.publishers)

    def with_url(self, url: str):
        self.base_url = url
        return self

    def with_publishers(self, *args):
        if len(args) == 0:
            return self
        for publisher in args:
            self.publishers.append(publisher)
        return self

    def with_formats(self, *args):
        if len(args) == 0:
            return self
        for issue_format in args:
            self.formats.append(issue_format)
        return self
