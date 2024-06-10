# ByteCoreFast Emulator

ByteCoreFast is a high-performance drop-in replacement for the [ByteCore Emulator](https://github.com/joakimwinum/bytecore). It extends the ByteCore classes and replaces the emulator engine with a custom engine written in C for enhanced speed. This project aims to maintain 100% compatibility with the public interfaces of the [ByteCore Emulator](https://github.com/joakimwinum/bytecore). If you encounter any incompatibilities, please [create an issue](https://github.com/joakimwinum/bytecorefast/issues) detailing the discrepancy.

## Key Features

- Fast performance for long-running programs.
- Seamless integration with ByteCore Emulator projects.
- Simple installation and usage.

## Installation

### Using pip

To install ByteCoreFast, run:

```bash
pip3 install bytecorefast
```

### Manual Setup

1. Ensure you have Python 3.11 or newer installed.
2. Clone the repository and navigate into the root directory.
3. (Optional) Create a Python virtual environment to isolate dependencies.
4. Install the necessary dependencies:

```bash
pip3 install -r requirements.txt
```

### Gitpod Setup

You can also use Gitpod to run the emulator by clicking [here](https://gitpod.io/#https://github.com/joakimwinum/bytecorefast).

## How to Use

To use ByteCoreFast, replace the import statement in your project:

```python
# Original import
from bytecore.emulator import ByteCore

# New import for faster performance
from bytecorefast.emulator import ByteCore
```

You should now see improved performance for long-running programs. Note that small programs or step-by-step execution might be slower due to overhead.

## Running the Emulator

To run the emulator, follow the instructions provided in the [ByteCore project](https://github.com/joakimwinum/bytecore).

### Troubleshooting

If the C code is not compiled for your system, you may encounter issues. In such cases, please revert to the original ByteCore Emulator written entirely in Python.

## License

This project is licensed under the terms of the MIT License. See the [LICENSE](https://github.com/joakimwinum/bytecorefast/blob/main/LICENSE) file for the full text.
