
data_dump : data.py util/read_conf.py util/ds.py
	python3 data.py -d $(data_type) -a dump

data_load : data.py util/read_conf.py util/ds.py
	python3 data.py -d $(data_type) -a load

stat : data.py statistics.py util/read_conf.py util/ds.py
	pypy statistics.py

split : data.py split.py util/read_conf.py util/ds.py
	pypy split.py

test_sp : util/sparse_vector.py
	python util/sparse_vector.py
