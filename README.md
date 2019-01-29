# Hubstaff interview test

The idea is get the data from Hubstaff organization and show it in a datable.

Some decisions:
* As this is a small project, with just some basic requierements, I decide to use Flask instead of Django
* Again, because is a small project, I decide to not use a Database and get all the data from hubstaff in the start, this way I don't have to worry about sync the data between the DB and Hubstaff
* Again, bacause is a small project, I'm not using a package/environment manager as pyenv (Maybe I should)
* After do all the functionalities I saw that I forgot that you can select the day of the data to show. 
In a real project, I would move all to Ajax to get the data without refresh the screen, 
but as I have spent more time that I should, I will do it just by http GET


## Deploy
run a pip install command (this could be inside a virtualenv ):
``pip install -r requirements.txt``

And then run:
`` python server.py``

**Note:** you will find here a .env file, this is the configuration file, usually, this file shouldn't be in the 
repository because of security reasons, but in this case, is here to avoid of setup all manually (for the interviewers)