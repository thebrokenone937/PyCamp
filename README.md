PyCamp
======

A project management tool somewhat similar to Basecamp

Features
========

This application is loosely based on basecamp. I find basecamp useful for managing projects at work but I didn't want to pay the money for it for the personal projects I work on so I built this application. Also I wanted to improve my python skills so it was a good project to work on for that.

The application will let you:

Login and Register

Create New Projects

Edit Projects

Add Todo Lists

Edit Todo Lists

Delgete Todo Lists

Add Todo Items

Edit Todo Items

Delete Todo Items

Drag and drop todo items into different Lists

Add Comments to Todo Items

Edit Comments

Delete Comments

Upload Files

Add Users to Projects (There's currently a javascript bug in this feature though that limits you to adding 4 users)

View Project Summary Screen

View Todo Comments

Show Todo Items Assigned to a particular user

Testing
=======

I've added unit tests for the core features of the application. To run them just type the following from the command line in the main directory:

python run_tests.py test

Notes:
======

I haven't added email sending functionality for things like registration confirmation and the forgot password link yet. I need to add links to the register & forgot password pages also.

I could add a few more features like email notifications to users that subscribe to todo items. Search functionality, change password, Ordering of todo items/Lists that sort of thing.

Finally you'll need to change the database settings in engine.py under the models directory to get this working on your machine. The database settings should probably be loaded from config files with different files for different environments but that's a future task.
