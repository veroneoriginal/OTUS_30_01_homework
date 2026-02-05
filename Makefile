lint:
	pylint server.py utils.py resp.py http_server

test:
	python -m unittest http-test-suite/httptest.py

test_local:
	pytest http_server/test_http_server
