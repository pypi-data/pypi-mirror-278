from comicbot_api.version1.comic_bot_api_client_v1 import ComicBotAPIClientV1Builder
from pprint import pprint
from timeit import default_timer as timer


def main():
    builder = ComicBotAPIClientV1Builder()
    client = builder.build()
    start_time = timer()
    pprint(client.get_releases_for_week(week_num=3, formats=["hardcover", "tradepaperback"]))
    end_time = timer()
    print(end_time - start_time)


if __name__ == '__main__':
    main()
