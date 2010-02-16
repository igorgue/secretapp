"""
Bakery is a simple application for full page caching using the database. 
If the site is experiencing a traffic spike then add a rule to the application 
telling it which page to cache. It ignores logged in users, POST requests and 
those with query string arguments.
"""