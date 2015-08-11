
Description
===========

A lightweight authentication plugin for MySQL which send the data over a UNIX domain socket to a 
daemon which does the actual authentication.

Benefits:

* Write the authentication part in Python, Go, etc.
* If your code crashes or has bugs it won't take the MySQL server down with it.

Status: (very) experimental

## Basic implementation

File: `authsock.py`

Basic authentication with a static username and password

## TOTP implementation

File: `authsock_otp.py`

One time password implementation

To generate a token (valid for 30s by default):

    python3 -c "import oath; print(oath.totp('123456'))"

Setup
=====

This requires the plugin from [this branch](https://github.com/dveeden/mysql-server/tree/authsock)

Start socket authentication service:

    $ ./authsock.py

Plugin installation:

    mysql> INSTALL PLUGIN authsock_srv SONAME 'authsock_srv.so';

User creation:

    mysql> CREATE USER 'as'@'%' IDENTIFIED WITH 'authsock_srv' REQUIRE NONE PASSWORD EXPIRE DEFAULT ACCOUNT UNLOCK;

Setup connection:

    $ mysql -u as --enable-cleartext-plugin -pfoobar

TODO
====

* Support `mysql_native_password`
* Check socket peercred to see if the socket is ran by the correct user
* Check socket privileges
* Move socket to a more secure location
* code cleanup
* example service scripts
 * PAM

Testing
=======

    nc -U /tmp/authsock.sock
