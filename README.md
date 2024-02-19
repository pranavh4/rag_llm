# FinBot
Chatbot for Financial Analysts powered by LLMs and Retrieval Augmented Generation.<br>

## How to Run
The project can be run either as a docker container or directly via the terminal.

**However, before following either of these steps, ensure you update the [config.yaml](/llm_server/resources/config.yaml) file (llm_server/resources/config.yaml) with your open_api_key which will be used to query the OpenAI API to get llm responses.
You can refer this [link](https://help.openai.com/en/articles/4936850-where-do-i-find-my-api-key) for generating an openai api key if you don't already have one**

### 1. Docker Container
- Ensure you have docker installed. The code was tested on Docker version 24.0.7
- Once you have updated the config.yaml file with your api key, build a docker image using the following commands. Change the image-name as per you requirements
```shell
cd /path/to/repository/ # Ensure you are in the directory which has the Dockerfile
docker build -f Dockerfile -t <image-name> .
```
- Once the build is complete, run the below command to start a container which will serve the application on port 5000
```shell
docker run -p 5000:5000 <image-name>
```

### 2. Directly via Terminal

- Ensure you meet the following prerequisites
  - `node v21.5.0` and `npm 10.2.4`
  - `python3` (code was tested on `python 3.11.5`)
- Create and activate a python [virtualenv](https://docs.python.org/3/library/venv.html) if required 
- Install the required libraries
```shell
cd /path/to/repository # Ensure you are in the directory which has the requirements.txt
pip install -r requirements.txt
```
- Create an optimized production build of the React frontend, which will be served by flask
```shell
cd /path/to/repository/chatbot-frontend # Ensure you are in the directory which has the package.json
npm install
npm run build
```
- Run the flask application
```shell
cd /path/to/repository # Ensure you are in the directory which has the requirements.txt
flask --app llm_server run --debug
```
