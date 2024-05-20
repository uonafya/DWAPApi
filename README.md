# middlewareapi
khis middleware api
## Deployment Steps - Python version 3.9+
### Create a virtual environment
- Install Python 3.9+ or any later version
#### Create an env
- Move into the project folder and create a virtual env
```sh python -m venv env```
#### Activate env & Install requirements
```sh
 . env/bin/activate
 pip install -r requirements.txt
 ```
#### Deploy the application using nohup  and gunicorn on port 8000
```sh
. /path/to/env/bin/activate  # Activate your virtual environment
cd /path/to/project/

nohup gunicorn --bind 0.0.0.0:8000 DITApi.wsgi:application > /path/to/your/log/file/logfile.log 2>&1 & # run application in the background using nohup and monitor logs
````
#### Allow port 8000 on the firewall
```sh
sudo ufw allow 8000
```
