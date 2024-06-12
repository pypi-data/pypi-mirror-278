from __future__ import annotations

from dataclasses import dataclass
import datetime
from .web_scraper import WebScraper
from comicbot_api.utils.comic_release_builder import ComicReleaseURLBuilder
from comicbot_api.utils.release_day import ReleaseDay
import loguru
from loguru import logger
import sys


@dataclass(init=False)
class ComicBotAPIClientV1:
    """
    Client interface for the Comic Bot API v1
    """
    _web_scraper: WebScraper
    _logger: loguru.Logger
    _logger_id: int = None
    _log_level: str = "INFO"
    _base_url: str = 'https://leagueofcomicgeeks.com'
    _api_endpoint: str = '/comic/get_comics'

    def __init__(self):
        self.reconfigure_logger(level=self._log_level)
        self._web_scraper = WebScraper(base_url=self._base_url)

    def get_releases_for_week(self, week_num: int, **kwargs):
        formats = kwargs.pop('formats', None)
        publishers = kwargs.pop('publishers', None)
        if formats is None:
            formats = []
        if publishers is None:
            publishers = []

        url_builder = ComicReleaseURLBuilder(ReleaseDay(week_num=week_num).release_date)
        url_builder.with_formats(*formats) \
            .with_publishers(*publishers) \
            .with_url(self._base_url + self._api_endpoint)
        url = url_builder.build()
        logger.trace(str.format("Requesting latest releases from {0}", url))
        return self._web_scraper.scrape_comics(url_builder.build())

    def get_latest_releases(self, **kwargs):
        return self.get_releases_for_week(week_num=datetime.date.today().isocalendar().week,
                                          **kwargs)

    def reconfigure_logger(self, sink=sys.stdout,
                           message="<green>{time}</green> - {level} - {message}", level="INFO"):
        if self.__getattribute__("_logger_id") is not None:
            logger.remove(self._logger_id)
        else:
            logger.remove()
        level = self._log_level.upper() or level
        self._logger_id = logger.add(sink, format=message, level=level)

    def set_web_scraper(self, web_scraper: WebScraper):
        self._web_scraper = web_scraper

    def set_log_level(self, log_level: str):
        self._log_level = log_level
        self.reconfigure_logger()

    def set_base_url(self, base_url: str):
        self._base_url = base_url

    def set_api_endpoint(self, api_endpoint: str):
        self._api_endpoint = api_endpoint


@dataclass(init=False)
class ComicBotAPIClientV1Builder:
    """
    Client Builder for Comic Bot API Client
    """
    comic_bot_client: ComicBotAPIClientV1

    def __init__(self):
        self.comic_bot_client = ComicBotAPIClientV1()

    def with_cache(self):
        logger.info("I dont do much yet...")
        return self

    def with_base_url(self, base_url: str):
        self.comic_bot_client.set_base_url(base_url)
        return self

    def with_api_endpoint(self, api_endpoint: str):
        self.comic_bot_client.set_api_endpoint(api_endpoint)
        return self

    def with_web_scraper(self, web_scraper):
        self.comic_bot_client.set_web_scraper(web_scraper)
        return self

    def with_log_level(self, log_level: str):
        self.comic_bot_client.set_log_level(log_level)
        return self

    def build(self) -> ComicBotAPIClientV1:
        return self.comic_bot_client
