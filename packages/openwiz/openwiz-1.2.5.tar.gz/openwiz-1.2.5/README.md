# LangChain CLI - PyPI

## Overview
The **LangChain CLI** is a powerful command-line tool that leverages the OpenAI API to generate code snippets based on user prompts. It is designed to assist developers by providing code suggestions and templates, making the coding process more efficient. The CLI also offers functionalities to save and load sessions, manage configurations, and handle generated code effectively.

## Features
- **Generate Code**: Create code snippets based on textual prompts using the OpenAI API.
- **Save Sessions**: Save the current state of your prompts and generated code for later use.
- **Load Sessions**: Load previously saved sessions to continue working seamlessly.
- **Save Generated Code**: Directly save generated code to specified files.
- **Configuration Management**: Easily configure your OpenAI API key and other settings.

## Installation

### Prerequisites
- Python 3.7 or higher
- OpenAI API key

### Steps

1. **Clone the repository**:
    ```bash
    git clone https://github.com/basith-ahmed/langchain-cli-v2.git
    cd langchain-cli-v2
    ```

2. **Install the required packages**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Configure your OpenAI API key**:
    ```bash
    python cli.py configure
    ```

## Usage

### Generate Code
Generate code based on a prompt.

```bash
python cli.py generate-code "Create a Python function to add two numbers"
```

**Output:**
```
Generated Code:
def add(a, b):
    return a + b
```

### Save Generated Code to File
Generate code and save it to a file.

```bash
python cli.py generate-code "Create a Python function to subtract two numbers" --file-name subtract.py
```

**Output:**
```
Generated Code:
def subtract(a, b):
    return a - b

Code saved to subtract.py
```

### Save Session
Save the current session with a specific name.

```bash
python cli.py save-session --session-name my_session --prompt "Create a Python function to add two numbers"
```

**Output:**
```
Session my_session saved
```

### Load Session
Load a previously saved session.

```bash
python cli.py load-session --session-name my_session
```

**Output:**
```
Loaded Session:
{
    "prompt": "Create a Python function to add two numbers",
    "generated_code": "def add(a, b):\n    return a + b"
}
```

### Configure API Key
Configure the OpenAI API key.

```bash
python cli.py configure
```

**Output:**
```
Enter your OpenAI API key: <your_api_key>
```

## Command Reference

### `generate-code`
Generate code based on a prompt.

**Usage**:
```bash
python cli.py generate-code "Create a Python function to add two numbers"
```
**Options**:
- `--file-name`: Save the generated code to a specified file.

### `save-session`
Save the current session with a specified name.

**Usage**:
```bash
python cli.py save-session --session-name my_session --prompt "Create a Python function to add two numbers"
```

### `load-session`
Load a previously saved session.

**Usage**:
```bash
python cli.py load-session --session-name my_session
```

### `configure`
Configure the OpenAI API key.

**Usage**:
```bash
python cli.py configure
```

## Project Structure

```
langchain-cli-v2/
├── cli.py
├── api_client.py
├── openai_api.py
├── session_manager.py
├── code_storage.py
├── config_manager.py
├── error_handler.py
├── logger.py
├── tests/
│   ├── test_cli.py
│   ├── test_api_client.py
│   ├── test_openai_api.py
│   ├── test_session_manager.py
│   ├── test_code_storage.py
│   ├── test_config_manager.py
│   ├── test_error_handler.py
│   └── test_logger.py
├── config/
│   ├── default_config.yaml
│   └── user_config.yaml
├── docs/
│   ├── index.md
│   ├── installation.md
│   ├── usage.md
│   ├── configuration.md
│   └── api_reference.md
├── sessions/
│   └── my_session.json
├── requirements.txt
└── .gitignore
```

## Development

### Running Tests
To run the unit tests:

```bash
pytest tests/
```

**Output:**
```
============================= test session starts =============================
collected 8 items

tests/test_api_client.py ....                                              [ 50%]
tests/test_code_storage.py .                                               [ 62%]
tests/test_config_manager.py .                                             [ 75%]
tests/test_error_handler.py .                                              [ 87%]
tests/test_logger.py .                                                     [100%]

============================= 8 passed in 0.45s ==============================
```

### Adding New Features or Fixes
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes and add tests for them.
4. Commit your changes (`git commit -am 'Add new feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Create a new Pull Request.

## Contributing

We welcome contributions! Please see the [CONTRIBUTING.md](CONTRIBUTING.md) file for more details.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
