lint:
	pylint server.py handler.py utils.py resp.py

test:
	python -m unittest http-test-suite/httptest.py
