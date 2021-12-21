test_plain:
	python regex-check-logs.py  --in bad.log
test_gz: gzipped_bad.log.gz
	python regex-check-logs.py  --in gzipped_bad.log.gz

gzipped_bad.log.gz: bad.log
	gzip < $< > $@

test_here: gzipped_bad.log.gz
	sudo date
	cp /dev/null re.out
	cp /dev/null re.err
	time script -c 'find . -type f \( -name '*.log' -o -name '*.log.gz' -o -name '*_log' -o -name '*_log.gz' \) -exec  python regex-check-logs.py --out re.out --err re.err --in '{}'  \+'
	cat re.out

find: gzipped_bad.log.gz
	cp /dev/null re.out
	cp /dev/null re.err
	sudo date
	time script -c 'sudo find / -type f \( -name '*.log' -o -name '*.log.gz' -o -name '*_log' -o -name '*_log.gz' \) -exec  python regex-check-logs.py --out re.out --err re.err --in '{}'  \+'
	cat re.out


all.list:
	sudo find / -type f \( -name '*.log' -o -name '*.log.gz' -o -name '*_log' -o -name '*_log.gz' \) > $@

find_all_list: all.list
	cp /dev/null re.out
	cp /dev/null re.err
	sudo date
	time script -c 'sudo python regex-check-logs.py --out re.out --err re.err --in-file-list all.list'
	cat re.out
	wc -l re.out re.err
