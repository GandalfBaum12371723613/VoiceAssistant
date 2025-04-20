# Voice Assistant

A Python-based voice assistant that can perform various tasks such as playing music, telling jokes, setting timers, controlling a Home Assistant instance, fetching weather information, and more.

## Contributing

Contributions are welcome and greatly appreciated! Whether you want to add new features, improve existing functionality, fix bugs, or provide feedback, your help is valuable to the project.

### How to Contribute

1. **Report Bugs**: If you encounter any issues, please open a bug report in the [Issues](https://github.com/your-repo/issues) section of the repository. Include as much detail as possible, such as steps to reproduce the issue, error messages, and your environment setup.

2. **Suggest Features**: Have an idea for a new feature? Open a feature request in the [Issues](https://github.com/your-repo/issues) section and describe your idea in detail.

3. **Submit Pull Requests**: If you'd like to contribute code:
   - Fork the repository.
   - Create a new branch for your feature or bug fix.
   - Make your changes and ensure they are well-tested.
   - Submit a pull request with a clear description of your changes.

4. **Provide Feedback**: Share your thoughts on the project, suggest improvements, or discuss ideas in the [Discussions](https://github.com/your-repo/discussions) section.

### Guidelines

- Follow the existing code style and structure.
- Write clear and concise commit messages.
- Include comments and documentation for any new code.
- Ensure your changes do not break existing functionality.

### Getting Started

If you're new to the project, check out the [README](README.md) for setup instructions and an overview of the features. Feel free to reach out if you have any questions or need help getting started.

Thank you for contributing to the Voice Assistant project!

## Features

- Play music
- Tell jokes
- Set timers
- Fetch weather information
- Control Home Assistant devices (e.g., turn heating on/off)
- Answer questions using a large language model

## Setup Instructions

### Prerequisites

1. **Python**: Ensure you have Python 3.13 installed on your system.
   - You can check your Python version by running:
     ```bash
     python3 --version
     ```
   - If Python 3.13 is not installed, download and install it from the [official Python website](https://www.python.org/downloads/).

2. **Virtual Environment**: It is recommended to use a virtual environment to manage dependencies.
    ```bash
    python3 -m venv .venv
    ```
    Then activate it using
    ```bash
    source .venv/bin/activate
    ```

3. **Home Assistant Token**: If you plan on using functions like ```heating_on()``` you have to get a long-lived-access-token to your homeassistant and save it in a file called ```HOMEASSISTANT_TOKEN```.

4. **Open weather map API key**: If you plan on using ```get_weather()``` you have to get a api key from [https://openweathermap.org/api](https://openweathermap.org/api) and save it in a file called ```OPENWEATHER_API_KEY```.

5. **Dependencies**: Install the python dependencies using 
    ```bash
    pip install -r dependencies.txt
    ```
    You also have to install ```espeak-ng``` and ```ollama``` using
    ```
    sudo pacman -S espeak-ng ollama
    ```
    or your distributions package manager.

    Now run 
    ```
    ollama run llama3.1
    ```
    and
    ```
    ollama run mistral
    ```
    to download the needed LLMs.

### Notes

- Ensure your Home Assistant instance is running and accessible at the URL specified in the `homeassistant.py` file (`http://192.168.1.111:8123` by default).
- Logs will be saved in the `logs/` directory for debugging purposes.

## License

This project is licensed under the Creative Commons Attribution-NonCommercial 4.0 International License. See the [LICENSE](LICENSE) file for details.
