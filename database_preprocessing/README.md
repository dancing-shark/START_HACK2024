# NIPA DatabaseBuilder 

In this subfolder you can find the scrapped data and a little script you can use to build a vector database from it.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

Before you begin, ensure you have Python installed on your system. CallBot is compatible with Python 3.7 and above. You can check your Python version by running:

```bash
python --version
```

You  will also need a vector db. The code will expect it to be on this path: `src/chroma_db`

### Installation

Here are two ways to get you started: using Poetry or pip.

#### Option 1: Using Poetry

[Poetry](https://python-poetry.org/) is a tool for dependency management and packaging in Python. It allows you to declare the libraries your project depends on and it will manage (install/update) them for you.

2. **Install Poetry**

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

2. **Create a Virtual Environment**

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

Remember that the VoiceBot will expect the db in its own directory. So if you build it please move the folder there.

#### You can also test it with your own prompt

```bash
python test_db_with_prompt
```
