# log4shell-rex-python
based on [back2root/log4shell-rex](https://github.com/back2root/log4shell-rex)

tested on linux with python 2 and python 3
Optimized for speed using mmap

```shell
find . -type f \( -name '*.log' -o -name '*.log.gz' -o -name '*_log' -o -name '*_log.gz' \) -exec  python regex-check-logs.py --out re.out --err re.err --in '{}'  \+
```

```shell
sudo find / -type f \( -name '*.log' -o -name '*.log.gz' -o -name '*_log' -o -name '*_log.gz' \) -exec  python regex-check-logs.py --out re.out --err re.err --in '{}'  \+
```
