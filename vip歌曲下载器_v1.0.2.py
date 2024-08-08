import asyncio
import hashlib
import json
import os.path
import re
import time
import tkinter as tk
from tkinter import ttk
import uuid

import aiofiles
import aiohttp

headers = {
    "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/89.0.4389.114 Mobile Safari/537.36 "
}

async def main(searchKeyWord, page='1'):
    # 异步上下文管理
    async with aiohttp.ClientSession() as session:
        url = 'https://complexsearch.kugou.com/v2/search/song'
        t = time.time()
        params = {
            'callback': 'callback123',
            # 页数
            'page': page,
            # 搜索值
            'keyword': searchKeyWord,
            'pagesize': '30',
            'bitrate': '0',
            'isfuzzy': '0',
            'inputtype': '0',
            'platform': 'WebFilter',
            'userid': '0',
            'clientver': '2000',
            'iscorrection': '1',
            'privilege_filter': '0',
            'token': '',
            'srcappid': '2919',
            'clienttime': str(t),
            'mid': str(t),
            'uuid': str(t),
            'dfid': '-'
        }
        # signature参数加密方法
        sign_params = ['NVPh5oo715z5DIWAeQlhMDsWXXQV4hwt', 'bitrate=0', 'callback=callback123',
                       'clienttime=' + str(t), 'clientver=2000', 'dfid=-', 'inputtype=0', 'iscorrection=1',
                       'isfuzzy=0',
                       'keyword=' + searchKeyWord, 'mid=' + str(t), 'page=' + page, 'pagesize=30',
                       'platform=WebFilter', 'privilege_filter=0', 'srcappid=2919', 'token=', 'userid=0',
                       'uuid=' + str(t), 'NVPh5oo715z5DIWAeQlhMDsWXXQV4hwt']
        # 'NVPh5oo715z5DIWAeQlhMDsWXXQV4hwt
        # appid=1014
        # clienttime=1693031684
        # clientver=1000
        # dfid=34cByg3lcMvC1KYEoZ0v8VHx
        # mid=4acac2816bcb3f9e670ddb5f44cbd717
        # srcappid=2919
        # uuid=1693031684068
        # {"userid":"586411488","plat":103,"m_type":0,"vip_type":0,"own_ads":{}}
        # NVPh5oo715z5DIWAeQlhMDsWXXQV4hwt
        sign_params = ''.join(sign_params)

        print(sign_params)
        signature = hashlib.md5(sign_params.encode(encoding='UTF-8')).hexdigest()

        params['signature'] = signature
        async with session.get(url=url, headers=headers, params=params) as resp:
            if resp.status == 200:
                resp_text = await resp.text()
                json_data = json.loads(resp_text[12:-2:])
                # 赋值判断数据获取状态
                status = json_data['status']
                song_list = []
                if status == 1:
                    for item in json_data['data']['lists']:
                        song_info = {'SongName': re.sub(r"[\/\\\:\*\?\"\<\>\|]", "_", item['SongName']),
                                     'AlbumID': item['AlbumID'],
                                     'FileHash': item['FileHash'], 'SQFileHash': item['SQFileHash'],
                                     'HQFileHash': item['HQFileHash'], 'MvHash': item['MvHash'],
                                     'Audioid': item['Audioid'],
                                     'SingerName': re.sub(r"[\/\\\:\*\?\"\<\>\|]", "_", item['SingerName'])}
                        song_list.append(song_info)
                else:
                    print(f'获取歌曲列表失败: {json_data["error_msg"]}')
                tasks = []
                if len(song_list) > 0:
                    print(f'获取歌曲列表成功，准备下载...')
                    for song in song_list:
                        task = asyncio.create_task(getSongPlayAddr(song))
                        tasks.append(task)
                await asyncio.wait(tasks)
            else:
                print('连接错误稍后重试')


async def getSongPlayAddr(song_info):
    mid = hashlib.md5(uuid.uuid4().urn.split(':')[2].encode(encoding='UTF-8')).hexdigest()
    async with aiohttp.ClientSession() as session:
        url = 'https://wwwapi.kugou.com/yy/index.php'
        params = {
            'r': 'play/getdata',
            'callback': 'jQuery191035601158181920933_1653052693184',
            'hash': song_info['FileHash'],
            'mid': mid,
            'platid': '4',
            'album_id': song_info['AlbumID'],
        }
        async with session.get(url=url, headers=headers, params=params) as resp:
            if resp.status == 200:
                resp_text = await resp.text()
                try:
                    json_data = json.loads(resp_text[42:-2:].replace('\\', '').encode('utf8').decode('unicode_escape'))
                    await saveMp3(json_data['data']['play_url'], song_info['SongName'], song_info['SingerName'])
                    print(json_data['data']['play_url'])
                except Exception as e:
                    pass
            else:
                print('请稍后再试')

async def saveMp3(url, song_name, singer_name):
    if not os.path.exists('music'):
        os.mkdir('music')
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url, headers=headers) as resp:
            async with aiofiles.open(f'music/{song_name}-{singer_name}.mp3', mode='wb') as f:
                await f.write(await resp.content.read())
                message = f'{song_name}--{singer_name}--下载完成\n'
                result_text.insert(tk.END, message)

def start_crawling():
    song_or_singer = entry.get()
    if song_or_singer:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main(song_or_singer))
    else:
        result_text.insert(tk.END, "请输入歌曲或歌手名称\n")

# GUI部分
root = tk.Tk()
root.title("歌曲爬取工具")

frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

label = ttk.Label(frame, text="输入歌曲或歌手：")
label.grid(row=0, column=0, sticky=tk.W, pady=5)

entry = ttk.Entry(frame, width=30)
entry.grid(row=0, column=1, pady=5)

btn = ttk.Button(frame, text="开始爬取", command=start_crawling)
btn.grid(row=1, column=0, columnspan=2, pady=10)

result_text = tk.Text(frame, width=40, height=10)
result_text.grid(row=2, column=0, columnspan=2, pady=5)

root.mainloop()