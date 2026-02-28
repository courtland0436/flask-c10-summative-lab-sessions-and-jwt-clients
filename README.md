cat <<EOF > README.md
# JWT Task Manager Application

This application consists of a React frontend and a Flask backend, providing a complete **JWT-based authentication flow** (sign up, log in, session persistence) and task management functionality.

---

## Quick Setup
To install all dependencies and set up the database automatically, run the following command in the root folder:

```bash
chmod +x setup.sh && ./setup.sh
```

### Running the Application
After running the setup script, follow these steps to start the application:

1.  **Start the Backend:** In one terminal, navigate to \`/server\` and run:
    ```bash
    pipenv run python app.py
    ```
    *The server will run on \`http://localhost:5555\`.*

2.  **Start the Frontend:** In another terminal, navigate to \`/client-with-jwt\` and run:
    ```bash
    npm start
    ```
    *The frontend will open at \`http://localhost:3000\`.*

---

## How to Test

Once the application is running, you can test the functionality in two ways:

1.  **Test Registration:** Register a new user using the Sign Up form in the browser.
2.  **Test Seed Data:** Log in with the following credentials to see the app pre-populated with data from \`seed.py\`:
    * **Username:** \`developer\`
    * **Password:** \`password123\`

---

If you wish to setup the app manually you can do the following.
## Manual Setup

## Frontend Setup

1.  **Navigate to the \`client-with-jwt\` folder** and install dependencies:
    ```bash
    cd client-with-jwt
    npm install
    ```

2.  **Start the frontend application**:
    ```bash
    npm start
    ```



## Backend Setup

1.  **Navigate to the \`server\` folder** and install dependencies:
    ```bash
    cd server
    pipenv install
    pipenv shell
    ```

2.  **Run database migrations**:
    ```bash
    flask db upgrade
    ```

3.  **Seed the database**:
    ```bash
    python seed.py
    ```

4.  **Start the backend application**:
    ```bash
    python app.py
    ```

---

## API Testing (Postman)

To test the backend API directly, import the \`TaskAPI.json\` file located in the root directory into Postman.

### Testing Steps:
1.  **Signup:** Run the \`Signup\` request. Copy the \`token\` from the response body.
2.  **Login:** Run the \`Login\` request. Copy the \`token\` from the response body.
3.  **Create Task:** Open the \`Create Task\` request. Go to the **Authorization** tab, select **Bearer Token**, and paste the token from step 1 or 2 into the Token field. Click Send.
4.  **Get Tasks:** Open the \`Get Tasks\` request. Go to the **Authorization** tab, select **Bearer Token**, and paste the same token. Click Send.

---

## API Endpoints

### Authentication

| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| POST | \`/signup\` | Registers a new user and logs them in | No |
| POST | \`/login\` | Authenticates an existing user | No |
| GET | \`/me\` | Retrieves the current authenticated user | Yes |

### Tasks

| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| GET | \`/tasks\` | Retrieves all tasks for the logged-in user | Yes |
| POST | \`/tasks\` | Creates a new task | Yes |
| PATCH | \`/tasks/:id\`| Updates a specific task | Yes |
| DELETE| \`/tasks/:id\`| Deletes a specific task | Yes |

---

## Token Management

- On login/signup, the \`token\` is saved to \`localStorage\` by the frontend.
- The \`/me\` endpoint checks this token on page load to persist the session.
- On logout, \`localStorage.removeItem("token")\` clears the session.
EOF