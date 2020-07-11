Image is based on https://github.com/tiangolo/uwsgi-nginx-flask-docker

To build, 
1) cd into citsciclassify directory, 
2) docker build -t scripps/citsciclassify .

To run (powershell), stay in citsciclassify
1) docker run --rm -d --name citsciclassify -p 8080:80 -v ${PWD}/db:/db scripps/citsciclassify
2) Browse to http://localhost:8080

To run (bash), stay in citsciclassify
1) docker run --rm -d --name citsciclassify -p 8080:80 -v $(pwd)/db:/db scripps/citsciclassify
2) Browse to http://localhost:8080