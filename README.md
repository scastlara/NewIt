# README
<img src="https://github.com/scastlara/NewIt/blob/master/newsreader/search_news/static/search_news/Images/newit_logo.png"/>


## Version

v.0.5.0

* Each time you fix a bug (backwards-compatible solution), increase the PATCH version.
* Each time you change the model, fix a bug (incompatible solution), add new features... increase the MINOR version.
* We won't change the MAJOR version until we have a fully working version of the website.

See: http://semver.org/



## TO DO

### Models and Database

- [ ] [**IMPORTANT**] Add a table with all the source links and names (link it to our articles table).
- [ ] [**IMPORTANT**] Add a table with all the categories (link it to our articles table).
- [ ] [**IMPORTANT**] Design the queries to be done (remember that each user will have only a set of sources).
- [x] Improve Database design to increase performance. * Performance seems to be good enough*
- [x] Check if Data-Types and constrains are correct.
- [x] Learn how to check if a record exist before uplading it and change rss_getter.py to do that.
    - See: http://stackoverflow.com/questions/10369042/how-to-check-if-record-exists-if-not-insert
- [x] Change rss_getter.py to work with the new database.
- [x] Learn how to do Full text search using SQL.
- [x] Learn how to do the queries on Django
    - Full text search over multiple columns is not possible using Django models.
     However, one can execute SQL queries and map the results to Django Models. See: https://docs.djangoproject.com/en/dev/topics/db/sql/

### Design and CSS
- [ ] Create Logo and Header (we need a name!)
- [ ] Create CSS for 'h1', 'h2', and 'p' to have a consistent design.
- [ ] Create CSS for the sidebar.
- [ ] Create CSS divs for user login box.
- [ ] Improve padding for current (and future) divs.
- [ ] Search box design and position (maybe centered? ykse tio xd)
- [ ] Better checkboxes for the subscriptions page (see mockups). See:
    - http://tutorialzine.com/2011/03/better-check-boxes-jquery-css/
    - http://www.hongkiat.com/blog/html-checkbox-ios7-switchery-js/
- [ ] [ OPTIONAL ] Tweak CSS and javascript to have responsive desing (so it can be used on phones).

### Application
- [ ] **BUG** Search keywords with quotes don't work.
- [ ] **BUG** Searches with small words don't work e.g: PP. Increase min-size and add stopwords.
    - See:
        - http://stackoverflow.com/questions/8301586/mysql-full-text-search-search-for-short-words
        - http://www.ranks.nl/stopwords/spanish
- [ ] Implement search modifiers +palabra -esta_no "literal"
- [x] Drop down menu to choose category (using another GET request parameter).  
- [x] Basic DB search implementation using the GET request.
- [ ] Implement User login view + template.
- [ ] Implement a way to sign up in our application.
- [ ] User subscriptions and user settings.
- [ ] Create view + template for user settings (user management before this).
- [ ] [ OPTIONAL ] Integrate Javascript word clouds for categories? news read by the user? search terms?
- [ ] [ OPTIONAL ] Implement a way to add or request the addition of new RSS sources.
- [ ] [ OPTIONAL ] Related news after reading one? that's machine learning ;)
- [ ] [ OPTIONAL ] User organization of subscriptions by folders, and displayed in the sidebar.


## Github tips

You need to be inside the Git project folder: the one with newsreader/ and bin/

### Add new changes

```
git add your_file.py
git commit -m 'Your message'
git push
```

### Update your local repository

```
git pull
```

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

```bash
sudo pip3 install PyMySQL
```

To install *MySQLdb*

```bash
sudo pip install MySQLdb
```

Then, you have to configure your Django application. You should have all the files up-to-date
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

### Full text search
In order to do full text searches, one has to use the MYSIAM engine (put it in your settings.py).
Then, you have to create indexes for the fields on which you want to search.
Add this to your settings.py

```python
'OPTIONS': {
    "init_command": "SET storage_engine=MYISAM",
}
```

Run this on your MySQL:

```sql
ALTER TABLE search_news_articles ADD FULLTEXT(title);
ALTER TABLE search_news_articles ADD FULLTEXT(content);
```

### Enter Mysql in the Server:
``` mysql
mysql -u dbw13 -p
```
password: dbw2016


### REMOVE CACHE FROM Server
> Do it each time you upload/change something

```sh
 yes | public_html/appnoticiosa/bin/remove_cache.sh
 ```
