# flask-oktan
Site provides different pages about Fitness company, made on python with Flask and psycopg2, database is based on PostgreSQL. Site provides admin page, where you can edit most of the pages, logging admins, adding and deleting admins, logging all admins' actions, adding more content to the page with js fetch requests.
Services and prices page is forming via excel file
Coaches, schedule and news pages are forming via PostgreSQL database
All pages except main page can be edited on site with admin page
To visit admin page you should go to '/admin' url where you should login, login session lasts 15 minutes
All admins actions are logged to the database, the logs stores 100 days
