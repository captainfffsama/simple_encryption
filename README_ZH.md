# 说明
对文件进行加密解密,可以直接作为工具对文件进行加解密,也可以在代码中作为上下文管理,对需要解密的文件进行临时解密使用,想使用自己的专属加密方式,可以修改 [./simecy/simecy](./simecy/simecy)中第5,6行的 `SALT`和`PDSALT`变量,然后重新编译安装即可

# 依赖

# 编译
```shell
python setup.py build_ext --inplace
python setup.py bdist_wheel
```

# 安装
```shell
pip install .
```

# 使用说明
默认密码是`imsohandsome`
## 作为单独的工具使用
比如要加密文件`大国崛起.mp4`
```shell
python -m simecy -f ./大国崛起.mp4 -m e -pd imsohandsome
```
同目录下应该会生成`大国崛起.mp4bytes`
同理解密
```shell
python -m simecy -f ./大国崛起.mp4bytes -m d -pd imsohandsome
```
同目录下应该会生成`大国崛起.mp4`

## 在代码中使用
假如我们已有一个神秘的`secret.txt`文件已经使用上述命令加密变成了`secret.txtbytes`,现在解密如下:
```python
from simecy import decrypt
import yaml
with decrypt("./secret.txtbytes","imsohandsome") as d:
    # do your work ,for example:
        with open(d,"r") as fr:
            line=fr.readline()
        ...
```

# TODO
- [ ] 可以手动设定解密文件的生命周期
- [ ] 只有上下文管理的方式有点脏
- [ ] 解密文件是文件对象支持
- [ ] 效率优化