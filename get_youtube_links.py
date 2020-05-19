import csv
import html
import json
import ssl
from urllib import request

import config

ssl._create_default_https_context = ssl._create_unverified_context

base_video_url = 'https://www.youtube.com/watch?v='
base_search_url = 'https://www.googleapis.com/youtube/v3/search?'


def get_channel_id(channel_name):
    url = 'https://www.googleapis.com/youtube/v3/channels?forUsername={}&key={}&part=id'.format(channel_name,
                                                                                                config.api_key)

    # user_agent = random.choice(config.USER_AGENTS)
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
    # print(user_agent)
    headers = {'user-agent': user_agent}

    if config.use_proxy:
        opener = request.build_opener(request.ProxyHandler(config.proxies))
        request.install_opener(opener)

    req = request.Request(url, headers=headers)
    inp = request.urlopen(req)

    resp = json.load(inp)
    return resp['items'][0]['id']


def get_links_from_channel(channel_id):
    video_links = []
    first_url = base_search_url + f'part=snippet&maxResults=50&order=date&key={config.api_key}&channelId={channel_id}'
    url = first_url
    while True:
        # user_agent = random.choice(USER_AGENTS)
        user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
        headers = {'user-agent': user_agent}
        if config.use_proxy:
            opener = request.build_opener(request.ProxyHandler(config.proxies))
            request.install_opener(opener)

        req = request.Request(url, headers=headers)
        inp = request.urlopen(req)

        resp = json.load(inp)
        items = resp['items']

        if items:
            next_page_token = resp['nextPageToken']
            for i in items:
                if i['id']['kind'] == "youtube#video":
                    title = i['snippet']['title']
                    title = html.unescape(title)
                    video_link = base_video_url + i['id']['videoId']
                    print(title)
                    print(video_link)
                    print()
                    video_links.append([title, video_link])
            url = first_url + f'&pageToken={next_page_token}'
        else:
            with open(config.output_csv_name, 'a', newline='', encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerows(video_links)
            break


if __name__ == '__main__':
    channel = get_channel_id(config.youtube_channel_name)
    # print(channel)
    get_links_from_channel(channel)
