# NIPA DatabaseBuilder 

In this subfolder you can find the scrapped data and a little script you can use to build a vector database from it.

## Getting Started

Remember that a `.env` file is needed on this directory. There is the following expected:

```env
COHERE_API_KEY="your_key"
GROQ_API_KEY="your_key"
# Here is where the test script will search for db to test it 
CHROMA_DB_PATH="../chroma_db"
# Here is where the built version will be saved
CHROMA_DB_RES_PATH="../chroma_db"
```

### Installation

Here are two ways to get you started: using Poetry or pip.

#### Option 1: Using Poetry

[Poetry](https://python-poetry.org/) is a tool for dependency management and packaging in Python. It allows you to declare the libraries your project depends on and it will manage (install/update) them for you.

1. **Install Poetry**

    If you don't have Poetry installed, install it by following the instructions on the official Poetry website.


- **Install Dependencies and Setup the Project**

    Run the following command inside the project directory:

    ```bash
    poetry install
    ```

    This command creates a virtual environment and installs all the dependencies specified in `pyproject.toml`.

- **Activate the Virtual Environment**

    To activate the Poetry-created virtual environment, run:

    ```bash
    poetry shell
    ```

#### Option 2: Using pip

1. **Create a Virtual Environment**

    It's recommended to create a virtual environment for your project to avoid dependency conflicts. But depends on your setup so up to you.

- **Install Dependencies**

    Install all dependencies using `requirements.txt`:

    ```bash
    pip install -r requirements.txt
    ```

### Building the Vector DB

After installation, you can run the script:

```bash
python vector_db_builder
```

#### You can also test it with your own prompt

```bash
python test_db_with_prompt
```
