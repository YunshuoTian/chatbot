# Chatbot
This web application is based on python flask and openai API. The webapp requires user authentication, after logging in, there will be two main functions including chat with code-interpreter assistant and webpage summarization.

**Please note**
- Users and chats data are saved in /instance/testdb.db automatically.
- The user session will be cleared every time when browser closed. So for code interpreter, you need to upload new file when opening browser next time.
- To chat with code interpreter, you need to submit a sample file first for further examination or questions.
- There can be multiple URLs entered for summarizing the content, each URL can be separated by comma.

## Install and run
### Run locally
1. Setup python env and then install all required packages through python pip install
```
pip install -r requirements.txt
```
2. Please fill in the **Openai API_KEY** in .env file and save it
3. export flask app
```
export FLASK_APP=run.py
```
4. Add missing openai certs to python certifi package and initialize database
```
sh entrypoint.sh
```
5. Run flask app and access the app in browser with address 127.0.0.1:5000
```
flask run --debug # debug mode can be turned off by removing '--debug'
```

### Run with Docker container
1. Install docker desktop
2. Pull docker image from the registry
```
docker pull ystian007/chatbot-app:latest
```
3. Download .env file from the repo and place it in the working directory. Please fill in the **Openai API_KEY** in .env file and save it
4. Run docker container locally
```
docker run --env-file .env -p 5000:5000 --name chatbot chatbot-app
```
5. Access the web app from address 127.0.0.1:5000
6. To view saved data in testdb, you may download it from the container to current directory
```
docker cp chatbot:app/instance/testdb.db testdb.db
```
