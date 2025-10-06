# Pawfect Mate 🐾

Pawfect Mate is a Retrieval-Augmented Generation (RAG) application designed to help individuals and families find the right dog breed that matches their lifestyle, activity level, and preferences. By combining a curated dataset of dog breeds with AI solutions, the application provides clear, tailored guidance to support better decision-making when choosing a furry friend.

## Problem Description

Choosing the right dog breed can be a challenging process. Families and individuals often struggle with questions such as:

- *Which breeds are best for apartments or small living spaces?*  
- *What breeds are more compatible with active owners who enjoy outdoor activities?*  
- *Which dogs have temperaments that fit with children or other pets?*  
- *What are the common health concerns or life expectancy for a given breed?*  

Without reliable and consolidated information, people risk adopting dogs that may not fit their lifestyle, leading to mismatched expectations, stress for the owner, and reduced quality of life for the pet.

**Use Cases**

* Families choosing a dog that fits well with children and home environment
* Active individuals looking for high-energy companions
* Seniors or people in smaller spaces searching for calmer breeds
* First-time owners seeking guidance on temperament, health, and care needs

## Data

The application uses a **custom dataset of dog breeds** created by scraping breed-related pages from Wikipedia.  
- **Size:** 354 records (dog breeds)  
- **Format:** JSON-like structured data  
- **Fields include:**  
  - `breed_name` – the official breed name  
  - `history` – historical background of the breed  
  - `health` – common health concerns and life expectancy data  
  - `characteristics` – physical traits and breed standards  
  - `appearance` – descriptive details of how the breed looks  
  - `temperament` – typical behavioral traits  
  - `description` – general overview of the breed  

Example entry (simplified for readability):

```json
{
  "breed_name": "Chihuahua (dog breed)",
  "history": "DNA studies suggest that native American dogs entered North America from Siberia roughly 10,000 years ago ...",
  "health": "The Chihuahua has some genetic predisposition to several neurological diseases, among them atlantoaxial instability ...",
  "description": "",
  "characteristics": "'Chihuahua breed standards specify an 'apple-head' or 'apple-dome' skull conformation ...",
  "appearance": "",
  "temperament": "",
}
```
## Technologies

* Python 3.10
* Docker for containerization
* Minsearch for full-text search
* FastAPI for API Inferface
* Grafana for monitoring
* PostgreSQL for database (feedback)
* OpenAI as LLM

## Preparation
Since we use OpenAI, you need to provide your API key to ```.env``` file in the main directory. 

We use pipenv for managing dependencies and Python 3.10. 

Make sure you have pipenv installed:
```bash
pip install pipenv
```

After it is installed, add dependencies:
```bash
pipenv install --dev
```

## Running the application

### Database configuration

Before the application starts for the first time, the database needs to be initialized.

First, run `postgres`:

```bash
docker-compose up postgres
```
Then run the db_prep.py script:

```bash
pipenv shell

cd pawfect_mate

export POSTGRES_HOST=localhost
python db_prep.py
```
To check the content of the database, use `pgcli` (already installed with pipenv):

```bash
pipenv run pgcli -h localhost -U your_username -d course_assistant -W
```
You can view the schema using the `\d` command:

```bash
\d conversations;
```
And select from this table:
```bash
select * from conversations;
```
### Running locally

The easiest way to run this application is with `docker-compose`:
```bash
docker-compose up 
```
Then you can test the application running test.py script:

```bash
pipenv shell
export POSTGRES_HOST=localhost
python test.py
```
### Running with Docker
If you want to run the application in Docker without `docker-compose`, e.g. for debugging purposes, prepare the environment as described in the sections above.

Then build an image:
```bash
docker build -t pawfect-mate .
```
Create network:
```bash
docker network create pawfect-net
```
Run PostgreSQL:
```bash
docker run -d \
  --name postgres \
  --network pawfect-net \
  -e POSTGRES_USER=your_username \
  -e POSTGRES_PASSWORD=your_password \
  -e POSTGRES_DB=course_assistant \
  -p 5432:5432 \
  postgres:13
```
Initialize database:
```bash
pipenv shell
export POSTGRES_HOST=localhost
cd pawfect-mate
python db_prep.py
```
Run app:
```bash
docker run -it --rm \
  --name pawfect-mate \
  --network pawfect-net \
  --env-file=".env" \
  -e OPENAI_API_KEY=${OPENAI_API_KEY} \
  -e DATA_PATH="data/rag_dataset.csv" \
  -p 5000:5000 \
  pawfect-mate
```
## Testin the app

When the application is running, you can use `requests` or `curl` for testing it.

### Requests
Run script `test.py` to send question to the app:
```bash
pipenv run python test.py
```
You can change question to test it.

### CURL
You can also use `curl` for interacting with the API to ask question:
```bash
DATA='{
      "question": "I have 2+2 family with children in age 10-15. We are very active and want to have middle-size dog, easy to train. Write me 5 breeds."}'
URL=http://localhost:5000
curl -X POST \
     -H "Content-Type: application/json" \
     -d "${DATA}" \
     ${URL}/ask 
```
or to send feedback:
```bash
ID="d314c573-ac5a-4e1c-b7c6-749aac1c0912"
URL=http://localhost:5000
FEEDBACK_DATA='{
  "conversation_id": "'${ID}'",
  "feedback": 1
}' 

curl -X POST \
  -H "Content-Type: application/json" \
  -d "${FEEDBACK_DATA}" \
  ${URL}/feedback
```

### Other
Running Jupyter notebook for experiments:

```bash
cd notebooks
pipenv run jupyter notebook
```

## Interface

We use FastAPI for serving the application as API. 

Refer to ["Running the application" section](#running-the-application) for more detail.

## Ingestion

The ingestion script is in [pawfect-mate/ingest.py](pawfect-mate/ingest.py) and it's run on the startup of the app in [pawfect-mate/rag.py](pawfect-mate/rag.py).

## Evaluation

For the code for evaluating the system, you can check the [notebooks/03_evaluation_data_generation.ipynb](notebooks/03_evaluation_data_generation.ipynb) notebook. 

### Retrieval 

The basic approach - using minsearch without any boosting - gave the following metrics:  

* hit rate: 97%
* MRR: 91%

The improved version (with tuned boosting):
* hit rate: 98%
* MRR: 92%

The best boostinf parameters: 
```python
boost = {
        'breed_name': 1.05,
        'history': 1.5,
        'health': 0.38,
        'description': 0.95,
        'characteristics': 0.94,
        'appearance': 1.23,
        'temperament': 0.83,
    }
```

### RAG Flow

We used the LLM-as-a-Judge metric to evaluate the quality of our RAG flow. 

Among 50 records, we had:
* 41 relevant
* 6 partly - relevant 
* 3 irrelevant 

## Background
Here we provide background on some tech not used in the course and links for further reading. 

### FastAPI

**FastAPI** is a modern, fast (high-performance) web framework for building APIs with Python 3.7+ based on standard Python type hints. It allows developers to quickly create RESTful APIs with automatic validation, interactive documentation, and type-checked request/response handling. FastAPI is designed to be easy to use while maintaining high performance, making it suitable for both small projects and production-grade applications. 

In our case, we can send question to `http://localhost:5000/ask`.

For more information and detailed documentation, visit the [FastAPI official website](https://fastapi.tiangolo.com/).
