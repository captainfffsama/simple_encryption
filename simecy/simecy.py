import base64
import tempfile
import os

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC



class decrypt:
    def __init__(self,file_path:str, password:str = "imsohandsome"):
        """用于代码中的上下文管理器,会在临时文件中生成一个临时文件,然后将解密的内容写到其中,返回临时文件的路径.上下文管理结束之后删除解密得到的临时文件

        Args:
            file_path: 需要解密的文件
            password: 解密所使用的密码

        Example:
            假设需要解密的是kp2d_cfg.yamlbytes,密码是imsohandsome

            >>> from simecy import decrypt
            >>> import yaml
            >>> with decrypt("./kp2d_cfg.yamlbytes","imsohandsome") as d:
            >>>    # do your work ,for example:
            >>>        with open(d,"r") as fr:
            >>>            yaml_content=yaml.load(fr,Loader=yaml.FullLoader)
            >>> ...
        """
        self.file_path = file_path
        self.pw=password
        self.final_file_path=""

    def __enter__(self):
        if os.path.splitext(self.file_path)[-1][-5:] == "bytes":
            _, self.final_file_path = tempfile.mkstemp(
                suffix=os.path.splitext(self.file_path)[-1][:-5])
            decode(self.file_path, self.pw,self.final_file_path)
        else:
            print("WARNING:{} file is not end with bytes,noneed to be decrypt!".format(
                self.file_path))
            self.final_file_path= self.file_path
        return self.final_file_path

    def __exit__(self, exc_type, exc_val, exc_tb):
        if os.path.splitext(self.file_path)[-1][-5:] == "bytes" and os.path.exists(self.final_file_path):
            os.remove(self.final_file_path)  # type: ignore


def decode(file_path, password,save_path = ""):
    """解密文件

    Args:
        file_path: str
            需要解密的文件的路径,文件名需是 bytes 结尾
        password: str
            解密所需的密码
        save_path: str
            解密之后文件的保持位置,默认是和加密文件同一目录,将加密文件名中bytes去掉
    """
    assert file_path.endswith(
        'bytes'), "ERROR: {} must end with bytes".format(file_path)
    with open(file_path, "rb") as fr:
        token = fr.read()

    SALT = b'\n"\x98\x02\xf6\xee\xef$\xbc(\x02\xcd\x17\xb3X\xd2'
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32,
                     salt=SALT, iterations=390000)

    kkey = kdf.derive(password.encode(encoding='utf-8'))
    key = base64.urlsafe_b64encode(kkey)
    f = Fernet(key)
    content_str = f.decrypt(token)
    # try:
    #     print("content is: \n", content_str.decode(encoding='utf-8'))
    # except:
    #     pass
    if save_path=="":
        save_path = file_path[:-5]
    with open(save_path, "wb") as fw:
        fw.write(content_str)


def encode(file_path,password,save_path=""):
    """加密文件

    Args:
        file_path: str
            需要加密的文件的路径,文件名需是 bytes 结尾
        password: str
            加密所需的密码
        save_path: str
            加密之后文件的保持位置,默认是和未加密文件同一目录,在其名字之后加上bytes
    """
    if save_path=="":
        if not file_path.endswith("bytes"):
            save_path = file_path+"bytes"
        else:
            print("WARNING: {} is exist,will not encode {}".format(save_path, file_path))
            return 0
    with open(file_path, "rb") as fr:
        content = fr.read()
    SALT = b'\n"\x98\x02\xf6\xee\xef$\xbc(\x02\xcd\x17\xb3X\xd2'
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32,
                     salt=SALT, iterations=390000)
    kkey = kdf.derive(password.encode(encoding='utf-8'))
    key = base64.urlsafe_b64encode(kkey)
    f = Fernet(key)
    if isinstance(content, str):
        content = content.encode(encoding='utf-8')
    token: bytes = f.encrypt(content)
    # print(token)

    with open(save_path, "wb") as fw:
        fw.write(token)

