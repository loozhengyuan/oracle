# Oracle

Developed by Digital Capabilities Team in Civil Service College, Oracle is a course pairing generator that serves as a heuristic/tool for public officers, agencies, and College's staff to quickly generate a list of course combinations that satisfy the learning outcomes that a user group desires to learn.

## Methodology
This example helps to understand the logic, but does not use the exact course or outcome data.

##### Step 1: Collate a list of course outcomes

List of course outcomes

| Outcome Code | Outcome Descriptor |
| ------------ | ------------------ |
| DSG1         | Demonstrate willingness to contribute new ideas on ways of working to achieve the desired goals of the organisation/transformation. |
| DGG6         | Recognise when regulations might need to shift to manage the impact of emerging digital solutions. |
| UEB1         | Identify the available tools (e.g. data analytics, behavioural insights and cost-benefit analysis) to design and evaluate digital services, policies and programmes. |

##### Step 2: Determine a list of courses that fulfills the outcomes

List of selected outcomes and their corresponding course associations

| Outcome Code | Course Associations |
| ------------ | ------------------ |
| DSG1         | CSR01, PIP10 |
| DGG6         | CSR01, PIP10, PELP1 |
| UEB1         | MTP10, SDS10|

##### Step 3: Generate all a unique set of courses that can fulfill the three learning outcomes

```
all_courses = [CSR01, PIP10, CSR01, PIP10, PELP1, PELP2, MTP10, SDS10, CSR02]
unique_courses = [CSR01, PIP10, PELP1, MTP10, SDS10]
```

##### Step 4: Create a powerset


```
CSR01
PIP10
PELP1
MTP10
SDS10
CSR01 + PIP10
CSR01 + PELP1
CSR01 + MTP10
CSR01 + SDS10
PIP10 + PELP1
PIP10 + MTP10
PIP10 + SDS10
PELP1 + MTP10
PELP1 + SDS10
MTP10 + SDS10
CSR01 + PIP10 + PELP1
CSR01 + PIP10 + MTP10
CSR01 + PIP10 + SDS10
...
```

##### Step 5: Each combination is ranked accordingly

```
CSR01
PIP10
PELP1
MTP10
SDS10
```

## Preparation

##### Domain Registration

At the very least, this app should have a public domain name for two main reasons:
1. An easy way for users to remember the site URL
2. Ability to use free SSL certs like [Let's Encrypt](https://docs.djangoproject.com/en/2.0/)

The current domain name `digitalcapabilities.team` is managed through [Namecheap](https://www.namecheap.com/). 

##### Web Hosting

Next, the web app needs to sit somewhere but generally I would recommend it to sit on Linux server that is based in Singapore.

The current app is hosted on [DigitalOcean](https://www.digitalocean.com/). They offer Linux Virtual Private Servers (VPS), or Droplets as they call it, at an affordable rate of USD$5/month. 

## Installation

##### Assumptions
1. Web server, database, app to be installed in a single server
2. Server is based on Debian 9.4
3. You have `root` privileges

### Step 1: Setting up your new server

Update all packages to the latest version
```shell
sudo apt-get update && sudo apt-get -y upgrade
```

Run this command to install Python (which should already have been installed) and its package manager `pip`
```shell
sudo apt install -y python3 python3-pip python3-dev
```

### Step 2: Installing database server (Optional if using existing database)
By default, Django uses SQLite3 as the database server. However, since we intend to use the Full Text Search function of PostgreSQL, we would need to use this instead.
For the purpose of this tutorial, we will be showing how to setup a PostgreSQL database server on the same host.

##### Installing the required packages
```shell
sudo apt install -y postgresql postgresql-contrib postgresql-doc postgresql-client
```

##### Allow PostgreSQL to be accessed outside of localhost (Optional)

First, we need to locate the directory that your postgresql is stored:
```shell
sudo find / -name postgresql.conf
```
Access the config files for postgresql
```shell
sudo nano /etc/postgresql/9.6/main/postgresql.conf
```
Uncomment the line `#listen_addresses = 'locahost'` and change it to '*'
```shell
listen_addresses = '*'
```

##### Set the appropriate authentication methods

Next, we need to change authentication methods for the users
```shell
sudo nano /etc/postgresql/9.6/main/pg_hba.conf
```

Set the auth method from `peer` to `md5` so local connections require password authentication
```shell
local    all             all                                              md5
```

Allow connections from outside of localhost by changing to `0.0.0.0/0` and `::/0`
```shell
host     all             all              0.0.0.0/0                       md5
host     all             all              ::/0                            md5
```

Restart Postgresql to reflect changes
```shell
sudo service postgresql restart
```

##### Creating users and permissions

We're going to use the default admin account `postgres` to create a new admin account. We are going to use `cscadmin` as the username; you can set the password during the prompt. The first command will create a new user in postgresql, whereas the second command will create a new database with the same name as the user, which is `cscadmin` in this case.

###### If you have `root` access:
```shell
su - postgres -c 'createuser --interactive --pwprompt'
su - postgres -c 'createdb -O cscadmin cscadmin'
```

###### If you only have `sudo` access:
```shell
sudo -u postgres createuser --interactive --pwprompt
sudo -u postgres createdb -O cscadmin cscadmin
```

##### Create database schemas
Lastly, for the purpose of this webapp, we will be confining the database tables under the `oracle` schema.
```shell
sudo psql -U cscadmin -c 'CREATE SCHEMA oracle;'
```

For more information on how to configure a database server like PostgreSQL, visit [this article](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-18-04) on DigitalOcean would help to give you a brief introduction.

### Step 3: Retrieve files using `git`

The easiest way to get the files is to have `git` manage the files. You can install `git` with this command:
```shell
sudo apt install -y git
```

In your home directory, create a project folder to house the project. We will be using 'civil-service-college' in this case.
```shell
mkdir civil-service-college
cd civil-service-college
```

Clone the repository by running the following command
```shell
git clone http://gitlab.zhengyuan.me/civil-service-college/oracle.git
```

### Step 4: Create a virtualenv for the project

Next, we will be creating an isolated environment to run this app. This requires a powerful Python library called `virtualenv`. You can install it via `pip`:
```shell
sudo pip3 install virtualenv
```

We will be naming our virtualenv as `venv` and housing it in the project directory
```shell
cd oracle
virtualenv venv
```

Activate the environment
```shell
. venv/bin/activate
```

### Step 5: Install required dependencies

To install the last-known working version of the packages, use the `requirements.txt` to install
```shell
pip install -r requirements.txt
```

(Optional) If you prefer to install the up-to-date version of the packages instead, run this command instead:
```shell
pip install django psycopg2 psycopg2-binary gunicorn
```

### Step 6: Initial settings
Contrary to the default `settings.py` file generated by Django, we made the settings file into a package. 

##### Settings Directory Structure
By the end of this step, your settings directory should appear like this. All files are included, but you would need to create `production.py`.
```
# ~/civil-service-college/oracle/oracle/

settings
├─ __init__.py
├─ base.py
└─ production.py
```

##### Create `production.py`

Navigate to the settings directory, create file and launch it the text editor
```shell
cd ~/civil-service-college/oracle/oracle/settings
sudo touch production.py
sudo nano production.py
```

Paste the following code inside and edit accordingly
```shell
# ~/civil-service-college/oracle/oracle/settings/production.py

from .base import *

SECRET_KEY = '' # You should have this SECRET KEY, insert it here

DEBUG = False

ALLOWED_HOSTS = [
    'oracle.digitalcapabilities.team', # Change this if your domain changes
]

CSRF_COOKIE_SECURE = True

STATIC_ROOT = '/var/www/oracle.digitalcapabilities.team/static/'   # This too

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'OPTIONS': {'options': '-c search_path=oracle'},
        'NAME': 'cscadmin',
        'USER': 'cscadmin',
        'PASSWORD': 'password', # Input your password here
        'HOST': '127.0.0.1',    # If the database is hosted else, change the HOST accordingly
        'PORT': '5432',
    }
}
```

##### Initialise database tables

Django uses the settings defined in core/models.py to create tables in the database. To initialise the tables:
```shell
python manage.py makemigrations
python manage.py migrate
```

##### Create superuser

In order to access the admin panel, you would need to create a superuser. You can create superusers using this command, but do take note that these users have COMPLETE control over your project, so choose wisely who you'd like to delegate this to.
```shell
python manage.py createsuperuser
```

##### Collect staticfiles

Gunicorn manages the running of the application, but much of the static files will be hosted by a webserver. This command will collect all the static files used in your project and place them in the `STATIC_ROOT` directory that you have defined earlier.
```shell
python manage.py collectstatic
```

##### Test run

Since Techxicon runs on Django, they provided a very very good [https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/](documentation) of checklist that needs to be completed before deploying. Some of these can even be automated using the following command:
```shell
python manage.py check --deploy
```

Test run the app using this command (0.0.0.0:80)
```shell
python manage.py runserver 0:80
```


### Step 7: Setup Webserver

Currently, the easiest way to deploy Techxicon is by using Caddy. Alternatively, as recommended by Gunicorn, you can deploy this on Nginx as well.

One-click install script by Caddy
```shell
curl https://getcaddy.com | bash -s personal
```

Create and edit Caddyfile
```shell
cd ~
sudo touch Caddyfile
sudo nano Caddyfile
```

Copy and paste these settings
```shell
# ~/Caddyfile

oracle.digitalcapabilities.team {
    proxy / localhost:8001 {
        transparent
    }
}

oracle.digitalcapabilities.team/static {
    root /var/www/oracle.digitalcapabilities.team/static
}

```

Increase file descriptor limit from 1024 to 8192 by editing the `/etc/security/limits.conf` file

```shell
sudo nano /etc/security/limits.conf
```

###### If you have `root` access:
Add these two lines in the file:
```shell
# /etc/security/limits.conf

root               soft    nofile          8192
root               hard    nofile          8192
```

###### If you only have `sudo` access:
Add these two lines in the file:
```shell
# /etc/security/limits.conf

*                  soft    nofile          8192
*                  hard    nofile          8192
```

### Step 8: Go live!

Reboot server to make sure everything is in order and persists restarts
```shell
sudo reboot
```

Run wsgi server
```shell
screen
cd ~/civil-service-college/oracle
. venv/bin/activate
gunicorn oracle.wsgi -b 0:8001
```

Run web server
```shell
screen
cd ~
caddy
```

List of `screen` commands:
```shell
screen          # To create a new screen
screen -ls      # To list the list of created sessions
screen -d       # To disconnect from current screen (or CTRL-A -> CTRL-D)
screen -r XXXX  # To reconnect to a specific screen
```

### Step 9: Using `systemd` to manage (Optional)

##### Gunicorn

First, lets create a Gunicorn service file
```shell
sudo nano /etc/systemd/system/gunicorn.service
```

Copy this into the file
```shell
# /etc/systemd/system/gunicorn.service

[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=root
Group=wheel
WorkingDirectory=~/civil-service-college/oracle
ExecStart=~/civil-service-college/oracle/venv/bin/gunicorn --workers 3 --bind unix:~/civil-service-college/oracle/oracle.sock oracle.wsgi:application

[Install]
WantedBy=multi-user.target
```

Next, we'll start the service and enable it to start at boot:
```shell
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
```

Verify that the service is running by running:
```shell
sudo systemctl status gunicorn
```

## Maintenance

### Golden Rule #1: Backup

Whatever changes you intend to make, do make sure you back up everything so that if anything goes wrong, you have a last known working copy of the files/droplet. 
This can be easily done using DigitalOcean's platform by taking snapshot of the droplet. For more information, check out DigitalOcean's [documentation page on its Snapshots](https://www.digitalocean.com/docs/images/snapshots/) feature.

### Content Management

Majority of the customisation can be managed via the admin portal. If you would like to add word or amend the definitions, you can enter the admin portal with this url:
```
https://oracle.digitalcapabilities.team/admin
```

### Code Management

##### Getting updates
Periodically, the code may be updated and you would want to make the changes reflected.
The golden rule would be to backup all settings first, which can be easily done using 

Run this command pull changes from the `Git` repository
```shell
git pull
```

## Credits

Many content posted here comes from a wealth of resources available on DigitalOcean's [docs](https://www.digitalocean.com/docs/) and [tutorials](https://www.digitalocean.com/community/tutorials) page. In addition, Django also provides a very very good [documentation](https://docs.djangoproject.com/en/2.0/) on the framework. 

Special thanks to my colleagues at DCT and CSC for contributing to this, in a way or another.
 
## License

This project is licensed under the GNU GPLv3 License
