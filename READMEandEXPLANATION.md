NOTE TO PROFESSOR: The username and password are admin and password. You need to run appdb.py first and then run app.py. I submitted on May 20th but then made some quick fixes on May 21st. I wanted to include in an email that I've been pressed for time and under a lot pressure due to this being my last semester and from finals, so there are some issues in the code, as mentioned in the design choices section below. My apologies for the issues mentioned. The commit count is 9 because I missed a few things due to stress and later did some small fixes. Thank you for reading this.

DESIGN CHOICES:
There are a few things that I'm aware of, such as the delete controller letting silent failures happen or the time zone not being EDT. I would have handled situations like these if there had been more time. I did make some quick corrections for smaller issues though.

SOLUTION EXPLANATION:
This solution is a single-account Flask app for blogging. Users can view posts on a dashboard, and after logging in, they can create, edit, or delete posts. Session checks are done to verify the user is logged in. 

HOW THE SOLUTION WORKS:
The solution works by using Flask routes to handle various actions and pages. For example, when a user goes to the dashboard, data is pulled from the SQLite database and displayed via an HTML template. Forms are used for POST requests when a user is creating, editing, or deleting a post. Once the database is updated, the user is redirected to the dashboard.

MODEL EXPLANATION:
The solution uses a single table database called posts. All blog information is stored within this table. post_id is the primary key, while post_date is handled by the database and generated automatically. post_title, post_author, and post_content are entered by the user.



PYTHON EXPLANATION:

Database Connection:
get_db() and close_connection handle the database connections. get_db() checks if a connection exists, if it doesn't then
it makes one and keeps the connection stored in g for reuse. row_factory is used so that data can be accessed as if it were a dictionary instead of tuples, it makes working on the app easier because now you don't need to use index-based accessing. close_connection() closes the connection after app context ends so that connections don't persist.



Main Controller:
This is the main controller. When the user visits the route URL, they are redirected to dashboard. 



Dashboard Controller:
The dashboard controller loads and displays the data from the database, connecting via get_db() getting all information from the table ordered in reverse chronological order, then hands the data to the html template. Basic error handling was used to catch issues, with an error message being displayed if something does go wrong.



Login/Logout:
valid_login() checks if the entered username/password match the expected credentials, which are "admin" and "password".

The login_controller handles logging in. A GET request allows the login form to be displayed, while on a POST request it goes over the entered credentials and validates the entered information via valid_login(). If the information is correct, the username is kept in the session to maintain logged in status. The user is then redirected to the dashboard. If the information entered was wrong then an error message is displayed with the form being empty again.

Logout lets the user sign out by removing the username from the session. They are then redirected to the dashboard. 



Create Controller:
The create controller does a session check, and lets them create new posts if they are logged in. A logged out user will be redirected to the login form. On a POST request, the form is submitted, a check is done to ensure that all fields are filled out. If the check is passed, the new post is inserted and committed to the database and appears on the dashboard, with the user being redirected there. If other errors happen, the form is displayed again with an error message. The GET request renders the form.


Edit Controller:
The edit controller does a session check, and lets the user edit posts if they are logged in. A logged out user will be redirected to the login form. Posts are retrieved via their ID. On a POST request, updated fields undergo validation similar to the create controller, then the database is updated if the check is passed. One detail to note is that edits also update the timestamp to when the post was edited. Once the changes are committed, the user is redirected to the dashboard where they can see the updated post. If other issues occur, the form is displayed again with an error message. The GET request renders the form.

Delete Controller:
The delete controller does a session check, and lets the user delete posts if they are logged in. A logged out user will be redirected to the login form. It uses a POST request for deletion, posts are removed through their ID, then the change is committed and the user is redirected to the dashboard where they will see the post has been deleted. If something goes wrong, the user is still redirected to the dashboard instead of seeing an error message.

HTML EXPLANATION:

dashboard_page.html shows all posts in a table. A Jinja loop is used for iterating through posts data and displays each post's information such as title or author, using dictionary-style access. Each post has an edit link that passes the post_id to load the edit form with the post's information in the form. The delete button for each post sends a POST request via form to delete posts.

login_form.html displays a form that allows a user to enter their credentials. A POST request is sent when submitted. It's checked if an error message exists, and the message is shown if an error occurs. 

create.html displays a form that allows a logged in user to create a post. A POST request is sent to "/create" when submitted. An error message is checked for, and is shown if an error occurs.

edit.html displays a form that allows a logged in user to edit a post. The form has information from the existing post that the user wishes to edit. A POST request is sent to "/edit/{{ post['post_id'] }}" when submitted. An error message is checked for, and is shown if an error occurs.

SQL EXPLANATION:
The script first connects to app.db. It then creates a table for posts if the table doesn't exist already. This was chosen instead of drop table if exists to ensure the db persists over time instead of being reset when ran. The table stores information on the post such as title or date. After the table is made, the changes are committed and the connection closed.








