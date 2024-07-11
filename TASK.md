### Task: Todo List API with Email and Google Sign-In Authentication
#### Objective:

Create a Django project with a RESTful API to manage a todo list, incorporating
authentication via email and Google Sign-In. Each todo item should have the following
attributes:

* Title
* Description
* Created At
* Due Date
* Completed (Boolean)

---
#### Requirements:

1. **Setup**:
   - Use Django and Django Rest Framework (DRF) to create the project.
   - Use SQLite as the database.

2. **Authentication**:
   - Implement email-based authentication using django-allauth.
   - Implement Google Sign-In authentication using django-allauth.

3. **Views**:
   - Create API views using DRF's generic views or viewsets to handle the
   following actions:
     - List all todo items for the authenticated user
     - Retrieve a single todo item by ID
     - Create a new todo item
     - Update an existing todo item
     - Delete a todo item
   - Ensure that only authenticated users can access these views.

4. **URLs**:
   - Set up the necessary URL routing to access the API endpoints.
   - Include endpoints for email and Google Sign-In authentication.

5. **Testing**:
   - Write basic tests for the API endpoints, including authentication tests.

6. **Documentation**:
   - Provide a README file with instructions on how to set up and run the project.

---
#### Bonus Points:
- Add filtering capabilities to the list endpoint (e.g., filter by due date, completed
status).
- Implement pagination for the list endpoint.
- Add validation to the Todo model (e.g., ensure the due date is in the future).

---
### Instructions:
1. **Model Definition**:
   - Define the Todo model in the models.py file of the app.
   - Ensure each todo item is associated with a user.

2. **Serializer**:
   - Create a serializer for the Todo model.

3. **Views**:
   - Implement the API views to handle CRUD operations for todo items.
   - Protect these views with authentication.

4. **URLs**:
   - Set up the URL routing for the API endpoints.
   - Include endpoints for email registration, login, and Google Sign-In.

5. **Testing**:
   - Write tests to ensure the API endpoints, including authentication tests, work
   as expected.

6. **README**:
   - Provide detailed instructions on how to set up and run the project, including:
     - Creating and activating a virtual environment
     - Installing dependencies
     - Running migrations
     - Running the development server
     - Accessing the API endpoints
     - Setting up email and Google Sign-In authentication