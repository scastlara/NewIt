# README

## TO DO

### Models and Database

- [ ] Improve Database design to increase performance.
- [ ] Check if Data-Types and constrains are correct.
- [ ] Change rss_getter.py to work with the new database.

### Design and CSS
- [ ] Create Logo and Header (we need a name!)
- [ ] Create CSS for 'h1', 'h2', and 'p' to have a consistent design.
- [ ] Create CSS for the sidebar.
- [ ] Create CSS divs for user login box.
- [ ] Improve padding for current (and future) divs.
- [ ] Search box design and position (maybe centered? ykse tio xd)

### Application
- [ ] Drop down menu to choose category (using another GET request parameter).  
- [ ] Basic DB search implementation using the GET request.
- [ ] Implement User login view + template.
- [ ] Implement a way to sign up in our application.
- [ ] Create view + template for user settings (user management before this).


## Github tips

You need to be inside the Git project folder: the one with newsreader/ and bin/

### Add new changes

git add your_file.py
git commit -m 'Your message'
git push

### Update your local repository

git pull


## Run the server

To run the server, go to the directory newsreader/ and run the following command:

```
python3 manage.py runserver
```

Then, open the webpage: http://127.0.0.1:8000/


## Database Model
To apply the database model you need to do several things.

First, you need to install a MySQL driver for python. If you are using Django with Python3,
then you need to install *PyMySQL*. Otherwise, use *MySQLdb*.

To install *PyMySQL*:

```
sudo pip3 install PyMySQL
```

To install *MySQLdb*

```
sudo pip install MySQLdb
```

Then, you have to configure your Django application. You shoiuld have all the files up-to-date
with our Github repository, because you don't want to mess around with all the config files by yourself.

The user and the password are in this folder (obviously, for the final version we will change it):

```
newsreader/
    newsreader/
        settings.py
```

The model is defined in:

```
newsreader/
    search_news/
        models.py
```

Feel free to experiment with the fields and data types and commit your changes.

To apply the model and create the MySQL tables:

```
python3 manage.py migrate
python3 manage.py makemigrations

# See the SQL query to be executed by django
less search_news/migrations/0001_initial.py

# Create the table
python3 manage.py sqlmigrate search_news 0001
```
