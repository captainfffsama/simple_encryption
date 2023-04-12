import tempfile
import os
from hashlib import blake2b

SALT = b'\n"\x98\x02\xf6\xee\xef$\xbc(\x02\xcd\x17\xb3X\xd2'
PDSALT =[13,17,41,49]

class decrypt:

    def __init__(self,
                 file_path: str,
                 password: str = "imsohandsome",
                 plaintext: bool = True):
        """用于代码中的上下文管理器,会在临时文件中生成一个临时文件,然后将解密的内容写到其中,返回临时文件的路径.上下文管理结束之后删除解密得到的临时文件

        Args:
            file_path: 需要解密的文件
            password: 解密所使用的密码
            plaintext: 指示是否是明文密码

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
        if plaintext:
            self.__pw = password
        else:
            self.__pw = _pddecrypt(password)
        self.final_file_path = ""

    def __enter__(self):
        if os.path.splitext(self.file_path)[-1][-5:] == "bytes":
            _, self.final_file_path = tempfile.mkstemp(
                suffix=os.path.splitext(self.file_path)[-1][:-5])
            decode(self.file_path, self.__pw, self.final_file_path)
        else:
            print(
                "WARNING:{} file is not end with bytes,noneed to be decrypt!".
                format(self.file_path))
            self.final_file_path = self.file_path
        return self.final_file_path

    def __exit__(self, exc_type, exc_val, exc_tb):
        if os.path.splitext(
                self.file_path)[-1][-5:] == "bytes" and os.path.exists(
                    self.final_file_path):
            os.remove(self.final_file_path)  # type: ignore




def encode(file_path, password, save_path=""):
    """加密文件

    Args:
        file_path: str
            需要加密的文件的路径,文件名需是 bytes 结尾
        password: str
            加密所需的密码,这里密码是明码
        save_path: str
            加密之后文件的保持位置,默认是和未加密文件同一目录,在其名字之后加上bytes
    """
    key = password.encode(encoding='utf-8')
    h = blake2b(salt=SALT, digest_size=32, person=b"captain no 1")
    h.update(key)
    hb = h.digest()
    with open(file_path, 'rb') as f:
        token = f.read()
    new_token = []
    for idx, bb in enumerate(token):
        new_code = bb + hb[idx % len(hb)]
        new_token.append(new_code // 256)
        new_token.append(new_code % 256)

    with open(save_path, 'wb') as f:
        f.write(bytearray(new_token))

    print("加密Token仅显示一次,请好好保管")
    print("加密Token为:{}".format(_pdencrypt(password)))


def decode(file_path, password, save_path=""):
    """解密文件

    Args:
        file_path: str
            需要解密的文件的路径,文件名需是 bytes 结尾
        password: str
            解密所需的密码,这里密码必须是明码
        save_path: str
            解密之后文件的保持位置,默认是和加密文件同一目录,将加密文件名中bytes去掉
    """
    key = password.encode(encoding='utf-8')
    h = blake2b(salt=SALT, digest_size=32, person=b"captain no 1")
    h.update(key)
    hb = h.digest()
    with open(file_path, 'rb') as f:
        token = f.read()
    print(len(token))
    new_token = []
    for idx, bb in enumerate(token[::2]):
        result = bb * 256 + token[idx * 2 + 1] - hb[idx % len(hb)]
        new_token.append(result)

    with open(save_path, 'wb') as f:
        f.write(bytearray(new_token))


def _pdencrypt(pwd: str):
    b = bytearray(pwd.encode("utf-8"))
    n = len(b)
    c = bytearray(n * 2)
    j = 0
    for i in range(0, n):
        b1 = b[i]
        b2 = b1 ^ PDSALT[0]
        c1 = b2 % PDSALT[1]
        c2 = b2 // PDSALT[1]
        c1 = c1 + PDSALT[3]
        c2 = c2 + PDSALT[2]
        c[j] = c1
        c[j + 1] = c2
        j = j + 2
    return c.decode("utf-8")


def _pddecrypt(s):
    c = bytearray(str(s).encode("utf-8"))
    n = len(c)
    if n % 2 != 0:
        return ""
    n = n // 2
    b = bytearray(n)
    j = 0
    for i in range(0, n):
        c1 = c[j]
        c2 = c[j + 1]
        j = j + 2
        c1 = c1 - PDSALT[3]
        c2 = c2 - PDSALT[2]
        b2 = c2 * PDSALT[1] + c1
        b1 = b2 ^ PDSALT[0]
        b[i] = b1
    return b.decode("utf-8")