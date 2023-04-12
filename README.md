[中文文档](./README_ZH.md)
# Description

Encrypt and decrypt files, can be used as a tool to encrypt and decrypt files directly, or as a context manager in the code to temporarily decrypt files that need to be decrypted. If you want to use your own exclusive encryption method, you can modify the `SALT` and `PDSALT` variables in line 5 and 6 of [./simecy/simecy](./simecy/simecy), and then recompile and install it.

# Dependencies

# Compilation

```shell
python setup.py build_ext --inplace
python setup.py bdist_wheel
```

# Installation

```shell
pip install .
```

# Usage

The default password is `imsohandsome`.

## Used as a standalone tool

For example, to encrypt the file `rising.mp4`:

```shell
python -m simecy -f ./rising.mp4 -m e -pd imsohandsome
```

A file named `rising.mp4bytes` should be generated in the same directory. Similarly, to decrypt:

```shell
python -m simecy -f ./rising.mp4bytes -m d -pd imsohandsome
```

A file named `rising.mp4` should be generated in the same directory.

## Used in code

Assuming we already have a mysterious file `secret.txt` that has been encrypted using the above command and become `secret.txtbytes`, now decrypt it as follows:

```python
from simecy import decrypt
import yaml
with decrypt("./secret.txtbytes","imsohandsome") as d:
    # do your work, for example:
        with open(d,"r") as fr:
            line=fr.readline()
        ...
```

# TODO

-  [ ] Manually set the lifecycle of decrypted files
-  [ ] Only context management is a bit messy
-  [ ] Decrypted files support file object
-  [ ] Efficiency optimization