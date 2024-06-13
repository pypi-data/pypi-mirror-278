import json
import os
from configparser import ConfigParser
from pathlib import Path
from typing import Optional

import aiofiles

CONFIG_FILE_PATH = Path.home() / ".agentql" / "config" / "config.ini"
DEBUG_FILE_PATH = Path.home() / ".agentql" / "debug"


def ensure_url_scheme(url: str) -> str:
    """
    Ensure that the URL has a scheme.
    """
    if not url.startswith(("http://", "https://", "file://")):
        return "https://" + url
    return url


def minify_query(query: str) -> str:
    """
    Minify the query by removing all newlines and extra spaces.
    """
    return query.replace("\n", "\\").replace(" ", "")


def get_api_key() -> Optional[str]:
    """
    Get the AgentQL API key from a configuration file or an environment variable.

    Returns:
    -------
    Optional[str]: The API key if found, None otherwise.
    """
    try:
        config = ConfigParser()
        config.read(CONFIG_FILE_PATH)
        api_key = config.get("DEFAULT", "AGENTQL_API_KEY", fallback=None)
        if api_key:
            return api_key
    except FileNotFoundError:
        pass

    # Fallback to environment variable if the key wasn't found in the file
    return os.getenv("AGENTQL_API_KEY")


async def get_api_key_async() -> Optional[str]:
    """
    Get the AgentQL API key from a configuration file or an environment variable asynchronously.

    Returns:
    -------
    Optional[str]: The API key if found, None otherwise.
    """
    try:
        config = ConfigParser()
        async with aiofiles.open(CONFIG_FILE_PATH, mode="r") as file:
            content = await file.read()
        config.read_string(content)
        api_key = config.get("DEFAULT", "AGENTQL_API_KEY", fallback=None)
        if api_key:
            return api_key
    except FileNotFoundError:
        pass

    # Fallback to environment variable if the key wasn't found in the file
    return os.getenv("AGENTQL_API_KEY")


def get_debug_files_path() -> str:
    """
    Get the path to the debug files directory through environment variables or a configuration file.

    Returns:
    -------
    str: The path to the debug files directory.
    """

    env_debug_path = os.getenv("AGENTQL_DEBUG_PATH")
    if env_debug_path is not None:
        return env_debug_path

    debug_path = ""
    try:
        config = ConfigParser()
        config.read(CONFIG_FILE_PATH)
        debug_path = config.get("DEFAULT", "AGENTQL_DEBUG_PATH", fallback=None)
    except FileNotFoundError:
        pass

    return debug_path or str(DEBUG_FILE_PATH)


def save_json_file(path, data):
    """Save a JSON file.

    Parameters:
    ----------
    path (str): The path to the JSON file.
    data (dict): The data to save.
    """
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def save_text_file(path, text):
    """Save a text file.

    Parameters:
    ----------
    path (str): The path to the text file.
    text (str): The text to save.
    """
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
