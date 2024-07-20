# To-do list application

---
## System dependencies
- [Docker](https://www.docker.com/products/docker-desktop/)
- [GNU make](https://www.gnu.org/software/make/)
- [Python 3.11+](https://www.python.org/downloads/)
- [Poetry](https://python-poetry.org/docs/)

---
## Setup and Usage

1. ### Configure Environment Variables
   - Copy `.env-example` to `.env`:
     ```bash
     cp .env-example .env
     ```
   - Configure the necessary environment variables in the `.env` file.

2. ### Setup Google OAuth2

   - **Create a Google API Console Project**
      - Go to the [Google API Console](https://console.developers.google.com/)
      - Click on "Select a project" -> "NEW PROJECT"
      - Enter a project name and click "CREATE"

   - **Configure OAuth Consent Screen**
      - In the API Console, go to `Credentials`
      - Click on `OAuth consent screen`
      - Choose `External` and click `CREATE`
      - Fill out the required fields such as `App name`, `User support email`, etc.
      - Add your domain to `Authorized domains`
      - Click `SAVE AND CONTINUE`

   - **Create OAuth Client ID**
      - In the API Console, go to `Credentials`
      - Click on `Create credentials` -> `OAuth 2.0 Client IDs`
      - Select `Web application`
      - Name your client (e.g., "Todo List OAuth Client")
      - Add your authorized frontend redirect URIs (e.g., http://localhost:8080/login/google/complete/)
      - Click `CREATE`
      - Copy your `Client ID` and `Client Secret`

   - **Configure Environment Variables**
      - Open your `.env` file
      - Add the following variables:
        ```
        GOOGLE_OAUTH2_KEY = <your_client_id>
        GOOGLE_OAUTH2_SECRET = <your_client_secret>
        ```

3. ### Setup Email

   - **Obtain an App Password from Google**
      - Open your Google Account settings: [Google Account](https://myaccount.google.com/?hl=en)
      - Go to `Security`
      - Under `Signing in to Google`, click `App Passwords`.
        You may need to sign in.
        If you don't have this option, it might be because:
        - 2-Step Verification is not set up for your account.
        - 2-Step Verification is only set up for security keys.
        - Your account is through work, school, or another organization.
        - You turned on Advanced Protection.
      - Click `Select app` and choose the app.
      - Click `Select device` and pick the device you're using.
      - Click `Generate`.
      - Follow the instructions to enter the app password.
        The app password is the 16-character code in the yellow bar on your device.
      - Copy password and tap `Done`.

      **Tip**: Most of the time, you'll only have to enter an app password once per app or device, so don't worry about memorizing it.

   - **Configure Environment Variables**
      - Open your `.env` file
      - Add the following variables:
        ```
        EMAIL_HOST_USER = <your_email_address>
        EMAIL_HOST_PASSWORD = <your_app_password>
        ```

4. ### Build the Project
   - Build the project with the following command:
     ```bash
     make build
     ```

5. ### Run the Project
   - Start the project:
     ```bash
     make up
     ```

6. ### Create Superuser
   - Create a superuser:
     ```bash
     make create-superuser
     ```

7. ### Get Access Token
   - Log in with superuser credentials using one of the following endpoints:
     - [localhost:8000/api/auth/login](http://localhost:8000/api/auth/login)
     - [localhost:8000/api/auth/token/obtain](http://localhost:8000/api/auth/token/obtain)

8. ### Add Access Token to Headers
   - Install the Google Chrome extension [Requestly](https://chromewebstore.google.com/detail/requestly-intercept-modif/mdnleldcmiljblolnjhpnblkcekpdkpa)
   - Create a new rule `Modify Headers`
   - Enter the URL of the endpoint you want to change, for example, `http://localhost:8000`
   - Add the request header `Authorization` with the value `Bearer <your_token>`

9. ### Access Documentation Endpoints
   - You now have access to the documentation at the following endpoints:
     - [localhost:8000/api/docs](http://localhost:8000/api/docs)
     - [localhost:8000/api/redoc](http://localhost:8000/api/redoc)
