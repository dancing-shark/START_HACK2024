# NIPA VoiceBot 

In this subfolder you can find relevant logic of the NIPA VoiceBot. You can either test it directly with your device microphone or you can run a flask server that sends and recieves audio over websockets.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

Before you begin, ensure you have Python installed on your system. CallBot is compatible with Python 3.7 and above. You can check your Python version by running:

```bash
python --version
```

You  will also need a vector db. The code will expect it to be on the root folder of the project. 

### Installation

Here are two ways to get you started: using Poetry or pip.

1. **Clone the Repository**

```bash
git clone https://github.com/dancing-shark/START_HACK2024.git && cd START_HACK2024
```

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



### Setup

#### Environment

Before running the project, make sure to configure the necessary environment variables.
Create a `.env` file in the project [ root directory  ](.)and add your configurations as needed:

```env
COHERE_API_KEY="your_cohere_api_key_here"
GROQ_API_KEY="your_groq_api_key_here"
```

#### Building the Vector DB

If you weren't provided with the already built DB files you can build it.
For this step please refer to [DatabaseBuilder](../database_builder/README.md)

### Running the Application

After installation, you can run the project:

#### Using own Mic
```bash
python src/main
```

#### Run the Flask server
```bash
python src/flask_app
```
