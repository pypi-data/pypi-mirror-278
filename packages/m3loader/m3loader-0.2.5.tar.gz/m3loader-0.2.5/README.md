
# m3loader

## Overview
`m3loader` is a Python tool that downloads and merges M3U8 segments into a single MP4 file using asynchronous operations for fast downloads. It supports progress bars, retries, and unique segment directories for concurrent sessions.

## Features
- Asynchronous downloading of M3U8 segments
- Merging segments into a single MP4 file
- Support for progress bars and retries
- Timeout support for downloads
- Unique segment directories for concurrent sessions

## Installation
You can install `m3loader` via pip:

```sh
pip install m3loader
```

## Usage

### Command Line Interface (CLI)

To use `m3loader` from the command line, you can use the following command:

```sh
m3loader <M3U8_URL> -d <OUTPUT_DIR> -o <OUTPUT_FILE> -p -t <TIMEOUT> -r <RETRIES>
```

#### Options
- `<M3U8_URL>`: The URL of the M3U8 file.
- `-d <OUTPUT_DIR>`: Output directory for the MP4 file. Default is the current directory.
- `-o <OUTPUT_FILE>`: Output file name (with or without .mp4 extension). If not provided, a default name is used.
- `-p`: Show progress bar and merging messages.
- `-t <TIMEOUT>`: Set timeout for downloading in seconds.
- `-r <RETRIES>`: Set maximum number of retries for downloading segments.

#### Example

```sh
m3loader "https://example.com/path/to/playlist.m3u8" -d workers -o video -p -t 300 -r 3
```

### As a Function

You can also use `m3loader` as a function in your Python scripts. First, import the `download` function from the `m3loader.dloader` module:

```python
from m3loader.dloader import download

m3u8_url = "https://example.com/path/to/playlist.m3u8"
output_path = "workers"
output_name = "video"
progress = True
timeout = 300
retries = 3

download(m3u8_url, output_path, output_name, progress, timeout, retries)
```

#### Function Parameters
- `m3u8_url (str)`: URL of the M3U8 file.
- `output_path (str)`: Output path for the MP4 file. Default is the current directory.
- `output_name (str)`: Output file name (with or without .mp4 extension). If not provided, a default name is used.
- `progress (bool)`: Show progress bar and merging messages. Default is `False`.
- `timeout (int)`: Set timeout for downloading in seconds. Default is `None`.
- `retries (int)`: Set maximum number of retries for downloading segments. Default is `None`.

### Example Script

Here’s a complete example script using the `m3loader` function:

**`example_script.py`**
```python
from m3loader.dloader import download

m3u8_url = "https://example.com/path/to/playlist.m3u8"
output_path = "workers"
output_name = "video"
progress = True
timeout = 300
retries = 3

download(m3u8_url, output_path, output_name, progress, timeout, retries)
```

### Project Structure

The `m3loader` project has the following structure:

```
m3loader/
├── LICENSE
├── README.md
├── requirements.txt
├── setup.py
├── m3loader/
│   ├── __init__.py
│   ├── dloader.py
└── example/
    ├── sample.m3u8
    └── test_video.mp4
```

### Contributing

If you would like to contribute to `m3loader`, please fork the repository and submit a pull request. For major changes, please open an issue first to discuss what you would like to change.

### License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

### Acknowledgments

- [aiohttp](https://github.com/aio-libs/aiohttp)
- [tqdm](https://github.com/tqdm/tqdm)
- [ffmpeg-python](https://github.com/kkroening/ffmpeg-python)
