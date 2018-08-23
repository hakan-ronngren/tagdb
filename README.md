# TagDB

TagDB is a database for tagging/categorizing and searching among several thousands of arbitrary objects that can be identified by strings, such as file paths.

The persistence layer is a set of text files, so backup is trivial and you will never have to worry about how to export data either. This is a fundamental design prioritization.

For quick access, the entire database is loaded into memory, and there is only one server thread so that no concurrent writes will occur and cause data corruption.

As a consequence, TagDB is unsuitable in applications where there are hundreds of users working with millions of objects.

## SSL, authentication and authorization

TagDB responds to unencrypted HTTP request on a local port, which is usually secure enough for a single-user application running on a personal computer. If your application serves a workgroup over your network, you need a web server (e.g. [Apache](http://httpd.apache.org/)) working as a reverse proxy in front of TagDB, providing encryption and the authentication and method-level authorization your application requires.

## Appendix

Learn more about bdd testing with behave:

* https://behave.readthedocs.io/en/latest/
* https://pypi.org/project/sure/
* https://jenisys.github.io/behave.example/
