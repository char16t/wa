install:
	pip install -r requirements.txt
	setup.py install
develop:
	pip install -r requirements.txt
	setup.py develop
test:
	py.test
