# Auto Clicker Module

**Python auto-clicker script that automates mouse clicks at defined intervals and visually indicates each click with a bubble overlay.**

## Installation

To install the module, use pip:

```sh
pip install auto-clicker
```

## Usage

### Command Line Usage

After installing the module, you can run the auto-clicker from the command line:

```sh
auto-clicker
```

This will start the auto-clicker with the default interval of 5 seconds.

### Script Usage

You can also use the module in your own scripts. Here’s an example:

```python
from auto_clicker import start_auto_clicker

# Define the time interval between clicks in seconds
click_interval = 5.0  # Change this value as needed

# Start the auto clicker
start_auto_clicker(click_interval)
```

## Features

- **Automates Mouse Clicks**: Clicks the mouse at specified intervals.
- **Visual Feedback**: Shows a bubble overlay at the click location.

## Examples

### Running from the Command Line

1. Open a terminal or command prompt.
2. Run the following command:

    ```sh
    auto-clicker
    ```

### Running from a Python Script

1. Create a Python script file (e.g., `run_clicker.py`).
2. Add the following code:

    ```python
    from auto_clicker import start_auto_clicker

    # Define the time interval between clicks in seconds
    click_interval = 5.0  # Change this value as needed

    # Start the auto clicker
    start_auto_clicker(click_interval)
    ```

3. Run the script:

    ```sh
    python run_clicker.py
    ```

## Customization

You can customize the click interval by passing a different value to the `start_auto_clicker` function:

```python
from auto_clicker import start_auto_clicker

# Set a custom click interval (e.g., 2 seconds)
click_interval = 2.0

# Start the auto clicker with the custom interval
start_auto_clicker(click_interval)
```

## Requirements

- `pyautogui`: For automating mouse clicks.
- `tkinter`: For showing visual feedback (bubble overlay).

Both libraries should be installed automatically with the module. If you encounter any issues, you can install them manually:

```sh
pip install pyautogui
```

## License

This project is licensed under the MIT License.

---

# Contributing

If you would like to contribute to the project, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes and commit them (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a new Pull Request.

# Author

David Oduse (odusedavid@gmail.com)

---