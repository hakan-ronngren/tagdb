# TagDB

TagDB is a database for tagging/categorizing and searching among several thousands of arbitrary objects that can be identified by strings, such as file paths.

The persistence layer is a set of text files, so backup is trivial and you will never have to worry about how to export data either. This is a fundamental design prioritization.

For quick access, the entire database is loaded into memory, and there is only one server thread so that no concurrent writes will occur and cause data corruption.

As a consequence, TagDB is unsuitable in applications where there are hundreds of users working with millions of objects.

## Appendix

Learn more about bdd testing with behave:

* https://behave.readthedocs.io/en/latest/
* https://pypi.org/project/sure/
* https://jenisys.github.io/behave.example/
