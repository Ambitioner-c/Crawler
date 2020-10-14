import requests
import time


def upload_image(cover_path):
    url = "http://127.0.0.1:8000/file/"
    headers ={

    }

    files = {'file': open(cover_path,'rb')}
    try:
        r = requests.post(url=url,files=files, headers=headers).content

        print(r.decode("utf8"))

    except Exception as e:
        print(e)


# with open('/home/cfl/qrcode.png', 'rb') as f:
#     data = f.read()
#     print(len(data))
start = time.time()
upload_image('/home/cfl/Downloads/qq-files/656359504/file_recv/recording10.wav')
end = time.time()
print(end - start)

