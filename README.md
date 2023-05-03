# Project Rocky

![D&D Logo](static/img/dndlogo.png)

## Overview

Project Rocky is the expansion of an idea brought to me by a colleague, a Dungeons &amp; Dragons nerd. Super-nerd, right? He comes up with this idea to help solve a pain point of the game which is keeping track of active effects. It should be fun, no one wants to do all the math.

This app is going to be a dashboard instead of a timer. Not to suggest my colleage had a bad idea, I actually plan to include it as part of the core app. But what use is an app that you have to keep inputting data every turn?

Project Rocky will give users access to a profile where they can create characters, post blogs, status updates and even create new games and host as Dungeon Master &lsqb;DM&rsqb;. Your team will login and join the game from the dashboard, where the players submit to the DM.

DM's will have admin rights to the game and will have access to your characters to update their stats during gameplay, including active effects. All of which will update in real-time and the system will update the several feeds that will be included in the app.

Users can have and join many games and all of their characters will be updated accordingly on their public profile and on the characters portal area on your user dashboard to see all updates in one area. The same goes for game updates and user updates such as status updates and blog posts for friends to see.

## Project Rocky v1.0

In this version:

1. Basic Flask App
2. [User Profile](#user-profile)
3. [Dungeon Masters](#dungeon-masters)
4. [Characters](#characters)
5. [Blog](#blog)

### Setup

1. Install from `requirements.txt`

*OR

1. Install [Flask](https://pypi.org/project/Flask/)
2. Install [Flask SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart/)
3. Install [SQLite Browser](https://sqlitebrowser.org/dl/)
4. Install [Flask Login](https://pypi.org/project/Flask-Login/)
5. Install [Flask Gravatar](https://pypi.org/project/Flask-Gravatar/)
6. Install [Psycopg2](https://pypi.org/project/psycopg2/)
7. Install [Gunicorn](https://pypi.org/project/gunicorn/)
8. Sign Up with [GitHub](https://www.github.com)

### Instructions

#### Local Settings

1. Create an `.env` file with [Python Environment Variables](https://able.bio/rhett/how-to-set-and-get-environment-variables-in-python--274rgt5)
2. In `main.py`
   1. Change the `SQLALCHEMY_DATABASE_URI` variable in the `.env` file
   2. Change the `SECRET_KEY` variable in the `.env` file

#### Heroku Local Settings

1. Create a new file in the main directory
   1. Name it exactly as `Procfile` without an extension
   2. In the file add `web: gunicorn main:app`

#### Heroku Host Settings

This is the trickiest part, so follow these steps carefully.

1. Sign Up or log into Heroku
2. At your dashboard page, click to create a new app and give it a name
3. On the app page
   1. Click the "deploy" tab
      1. Scroll down to "deployment method"
      2. Select GitHub, follow the instructions to authorize
      3. Search for your blog repo and connect it
      4. Scroll down to "automatic deploys" and click to enable
   2. Click the "resources" tab
      1. Scroll to the "add-ons" section
      2. Search for "Heroku Postgres"
      3. Click to add and select the free option
   3. Click the "settings" tab
      1. Scroll to "config vars" and select to reveal
      2. Click to edit the "DATABASE_URL" variable and copy the key
         1. Close the menu by clicking cancel
      3. Create a new key as "DB_URL"
         1. Paste the code you copied into the value box
         2. Change "postgres" to "postgresql"
         3. Click "add"
         4. Be sure to add your other hidden environment variables
            1. i.e. SECRET_KEY
   4. Click the "deploy" tab
      1. Scroll down to "manual deploy"
      2. Click "deploy branch"
      3. Once completed, click "view"

If you followed the steps correctly, you will see your app. If not, it will provide you with an error screen. From here you can just go into your app dashboard and locate the "more" button at the top right and view the log for the error messages.

### Features

#### User Profile

   Each person will be able to sign up and create their own user profile in the app. For this version, we will be building just the basics such as the ability to log in, see their character profiles, see their active games, update their information and security items.

#### Dungeon Masters

   The Dungeon Masters (DM's) will be regular users, but each user will have the ability to create games for users to join and will become the host for the game. The DM's will have access to update the game blog, update character statuses, add and modify active effects, and kick members.

#### Characters

   Each user will be able to create charaters to attach to their login. They will also be able to upload a profile photo and have the ability to modify their characters along the way. They can have several characters and play multiple games simultaneously.

#### Blog

   The blog feature will allow users to track their stories over time. And it will also allow characters to post updates to their page feed. Other users will be able to interact and discuss through comments in a forum.

### Roadmap

Due to my lack of artistic skills, and since I have already built one, I am using an old blog template I found a while ago when I was learning Flask. This will let me focus on the main features.

- [ ] Landing Page
- [ ] Sign Up
- [ ] Login Portal
- [ ] User Dashboard
- [ ] User Menu
- [ ] Character Dashboard
- [ ] Character Menu
- [ ] Games Dashboard
- [ ] Games Menu

### Additional Resources

- [Flask Documentation](https://flask.palletsprojects.com/en/2.1.x/) - Documentation for the Flask package
- [Flask SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart/) - Documentation for Flask SQLAlchemy
- [Flask SQLAlchemy - ORM, One-to-many](https://docs.sqlalchemy.org/en/14/orm/basic_relationships.html#one-to-many)
- [Flask Login](https://flask-login.readthedocs.io/en/latest/#configuring-your-application) - Documentation for the flask_login module
- [How to Set and Get Environment Variables in Python](https://able.bio/rhett/how-to-set-and-get-environment-variables-in-python--274rgt5) - This is a great resource to learn how to create persistent environment variables
