
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

usim : sim_matrix.py util/data.py util/sim_function.py
	pypy sim_matrix.py

create_db : db.py
	python db.py create

del_db : db.py
	python db.py del

feature : gen_feature.py util/db.py util/ds.py
	time python -O gen_feature.py 
