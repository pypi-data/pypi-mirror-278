# Uploader Service

  

A tool to upload folders with multipart upload.

  

## Installation

> pip install slizaiupload

  

## Usage

**usage:**
>slizaiupload folder_path [--parent-folder-name PARENT_FOLDER_NAME] [--thread THREAD]
>[--retry-delay RETRY_DELAY] [--env ENV] [--skip-extension SKIP_EXTENSIONS] [--include-folder]
  

**positional arguments:**

folder_path Path to the folder to upload

  

**options:**

-h, --help show this help message and exit

--include-folder Include folder path in key

--parent-folder-name PARENT_FOLDER_NAME: Parent folder name to include in key

--thread THREAD: Number of threads upload

--retry-delay RETRY_DELAY: Time delay (in seconds) before retrying

--skip-extension SKIP_EXTENSIONS: Comma-separated list of file extensions to skip

--env ENV Path file ENV

  

*You can also include the folder name in the key:*

> slizaiupload /path/to/your/folder --include-folder

  

*Or specify a parent folder name:*

> slizaiupload /path/to/your/folder --parent-folder-name parent_folder

  

*Upload all in current path use:* folder_path = .

  

*Example:*

> slizaiupload foldertest --env ./config --thread 10 --retry-delay 30 --skip-extension .mp3,.3gp  --include-folder

  

Create .env file in folder config data config
```
API_URL=https://example

TOKEN=token_string
```