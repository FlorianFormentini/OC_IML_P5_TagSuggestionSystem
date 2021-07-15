# [Openclassrooms IML - Project 5 : StackOverflow tag suggestion](#)

## API
The swagger contains all endoints documentation.

### 1. Installation (local) :
- You need to create a **`.env`** file containing these environnment variables :
    - `API_KEY=[apiKey]` - The key to send in the requests header to verify the users
    - `FLASK_ENV : {'development', 'production'}` - Define the app environment. Needs to be loaded before the app instance creation.
    - `OC_P5_ENV : {'dev', 'prod'}` - Used configuration (a third type `'test'` also exist but it's automatically set when testing).

- Then you have to install the dependencies (in a virtual env) : `pip install -r requirements.txt`

- **Run the app :** `$ python manage.py run`

### 2. Testing
To test the application, just use the following command to execute all test files:  
`$ python manage.py test`




