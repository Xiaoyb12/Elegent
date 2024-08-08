url='https://v3-webc.douyinvod.com/4e5c9aadec988f7ebb9f3c27d46ca3c5/6512eb7b/video/tos/cn/tos-cn-ve-15c001-alinc2/o8QRlxut9khVPNAKBZz6E5fW90hfgAIIg13CEA/?a=6383&ch=5&cr=3&dr=0&lr=all&cd=0%7C0%7C0%7C3&cv=1&br=2256&bt=2256&cs=0&ds=6&ft=inKH6wzxUUmfzXdDg0BD1YswHAX1tGPs3W49eFsWaS4D12nz&mime_type=video_mp4&qs=0&rc=MzNnaTM2O2UzN2dkODYzNkBpM2s3PDs6ZnJnbTMzNGkzM0BhMWBjLzM0NTQxLzFhYV8uYSNrNV9kcjRvbXFgLS1kLWFzcw%3D%3D&btag=e00008000&dy_q=1695735137&l=20230926213215FE3B54695BD85C209729'
import requests
res = requests.get(url)
open('1.mp4', 'wb').write(res.content)
