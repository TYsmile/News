import qiniu
from qiniu import Auth, put_data


access_key = "tOWNMqbbEAqgg8yKelIsl1e0CxDDUAY_mqih9PG9"
secret_key = "zXv4CkofUm_QlRGR0MmY9xVfFD5Mjl8CMciIdlTt"
bucket_name = "myhome"

def storage(data):
    try:
        q = Auth(access_key, secret_key)
        token = q.upload_token(bucket_name)
        ret, info = qiniu.put_data(token, None, data)
        print(ret, info)
    except Exception as e:
        raise e

    if info.status_code != 200:
        raise Exception("上传图片失败")

    return ret["key"]

if __name__ == '__main__':
    file = input("请输入文件路径")
    with open(file, 'rb') as f:
        storage(f.read())