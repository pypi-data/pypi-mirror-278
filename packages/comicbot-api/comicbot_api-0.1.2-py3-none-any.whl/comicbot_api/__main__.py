from comicbot_api.version1.comic_bot_api_client_v1 import ComicBotAPIClientV1Builder
from pprint import pprint


def main():
    builder = ComicBotAPIClientV1Builder()
    client = builder.build()
    pprint(client.get_releases_for_week(week_num=3, formats=["hardcover"], publishers=["marvel"]))


if __name__ == '__main__':
    main()
