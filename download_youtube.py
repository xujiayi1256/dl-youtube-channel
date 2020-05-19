from __future__ import unicode_literals

import csv
import html
import ssl

import youtube_dl
from retrying import retry

import config

ssl._create_default_https_context = ssl._create_unverified_context


def my_hook(d):
    if d['status'] == 'finished':
        # print('Done downloading, now converting ...')
        print(d)


@retry(stop_max_attempt_number=5, wait_fixed=2000)
def download(link):
    if config.use_proxy:
        ydl_opts = {'nocheckcertificate': True, 'proxy': config.proxies['https'], 'outtmpl': config.video_output_dir}
    else:
        ydl_opts = {'nocheckcertificate': True, 'outtmpl': config.video_output_dir}

    # ydl_opts = {'nocheckcertificate': True, 'proxy': config.proxies['https'], 'outtmpl': config.video_output_dir,
    #             'progress_hooks': [my_hook]}

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([link])
        print('========== Done! ==========')


def write_csv(title, link):
    with open(config.downloaded_csv_name, 'a', newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([title, link])


def main():
    data = []
    with open(config.output_csv_name, 'r') as f:
        result = csv.reader(f)
        for line in result:
            title = html.unescape(line[0])
            video_link = line[1]
            print('Title: ' + title)
            print('Link: ' + video_link)
            data.append(line)
            try:
                download(video_link)
            except:
                break
            else:
                write_csv(title, video_link)
            print()
    # print(data)


if __name__ == '__main__':
    main()
