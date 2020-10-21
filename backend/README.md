# Picture Tagger Server
The picture-tagger-demo service is composed of a frontend and a backend.
The backend's job is to provide a RESTful interface to the meta data about
pictures.  The "database" in this early protoype is just a pair of flat files,
but there is no reason why sqlite or mysql couldn't be used.

This server back-end runs within a docker container.
These files suffice to build the container around a Python/Flask application
that reads metadata files from the hosts's data directory.  
It is assumed the flask container is running on port 5000 on an ip
address identified in the BACKEND_IP environment variable.
The server side also needs a web-server (Apache in my case) with access to the 
WEBSERVER_PICTURE_ROOT directory.
Thus this picture-tagger-demo backend container serves the meta data 
and tags related to the pictuers, but
the web server will serve the pictures.

# Operations
I've made build.sh, start.sh, logs.sh and stop.sh scripts.  To build
the container, run ./build.sh.  

Once it is built, you can run it, but you 
must set and export the BACKEND_IP and WEBSERVER_PICTURE_ROOT environment
variables.  To run the backend, execute ./start.sh.

If you want to tail the server logs, run ./logs.sh.  You will notice that
we aren't running in production mode.  This app could be run under 
a production WSGI server like gunicorn in the future.

To stop the container, run ./stop.sh.

# Files
- api.py - Flask framework entry file
- PictureDB.py - Python3 database simulation layer
- Dockerfile - defines how to build the docker container
- requirements.txt - Python3 packages to include
- build.sh - builds the docker container
- start.sh - runs the container, listening on port 5000
- logs.sh - finds the running container and shows its logs
- stop.sh - kills the container 

# Directory
- data - contains the unique_sorted_pictures and tags databases.

