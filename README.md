# log4shell-rex-python
based on [back2root/log4shell-rex](https://github.com/back2root/log4shell-rex)

tested on linux with python 2 and python 3

Optimized for speed using mmap

read logs files and gzipped log files

prints out matched lines

```
python regex-check-logs.py  --in bad.log

bad.log:2 2021-12-11 11:01:05,99 http-nio-8080-exec-1 WARN Error looking up JNDI resource ${jndi:ldap://127.0.0.1/a}. javax.
```

```
python regex-check-logs.py  --in gzipped_bad.log.gz
```

```
python regex-check-logs.py  --help
usage: regex-check-logs.py [-h] [--out OUT] [--err ERR] (--in-file-list IN_FILE_LIST | --in INFILES [INFILES ...])

regex-check-logs.py

options:
  -h, --help            show this help message and exit
  --out OUT
  --err ERR
  --in-file-list IN_FILE_LIST
  --in INFILES [INFILES ...]
```

OUT will contain matches

ERR will contain files that could not be searched along with the error


```shell
find . -type f \( -name '*.log' -o -name '*.log.gz' -o -name '*_log' -o -name '*_log.gz' \) -exec  python regex-check-logs.py --out re.out --err re.err --in '{}'  \+
```

```shell
sudo find / -type f \( -name '*.log' -o -name '*.log.gz' -o -name '*_log' -o -name '*_log.gz' \) -exec  python regex-check-logs.py --out re.out --err re.err --in '{}'  \+
```
