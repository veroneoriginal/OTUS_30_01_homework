curl -I http://localhost:8080/

curl -I http://localhost:8080/../../etc/passwd
curl --path-as-is -I http://localhost:8080/../../etc/passwd

curl -i http://localhost:8080/../../etc/passwd
curl --path-as-is -i http://localhost:8080/../../etc/passwd

curl -i -X POST http://localhost:8080/
