import os
import re
import json
import queue
import errno
import threading
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

# Global definitions
HOME_DIR = os.path.expanduser("~")
CONFIG_DIR = os.path.join(HOME_DIR, '.config', 'pathconf')
CONFIG_FILE = '.file_paths.json'
CONFIG_FILE_PATH = os.path.join(CONFIG_DIR, CONFIG_FILE)
WORKERS = os.cpu_count() * 2

logging.basicConfig(level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def has_extension(filename):
    """
    Check if the given filename has an extension of
    reasonable length (5 characters or fewer).
    """
    return '.' in filename and len(filename.rsplit('.', 1)[1]) <= 5


def search_directories(queue, dir_to_find, target, stop_event,
                       ignore_extension=False, search_folder=False,
                       deprecated=False, regex=False):
    while not queue.empty() and not stop_event.is_set():
        try:
            directory = queue.get_nowait()
        except queue.Empty:
            break

        if stop_event.is_set():
            break

        try:
            for dirpath, dirnames, filenames in os.walk(directory):
                if not deprecated:
                    dirnames[:] = [d for d in dirnames if
                                   'Deprecated' not in d.lower()]

                if stop_event.is_set():
                    break

                if (dir_to_find and
                    not os.path.normpath(dirpath).endswith(
                        os.sep + dir_to_find)):
                    continue

                if search_folder:
                    if target in dirnames:
                        stop_event.set()
                        return os.path.join(dirpath, target)
                else:
                    if regex:
                        pattern = re.compile(target)
                        for filename in filenames:
                            if pattern.match(filename):
                                stop_event.set()
                                return os.path.join(dirpath, filename)
                    else:
                        for filename in filenames:
                            name_part = filename.rsplit('.', 1)[0]
                            if ignore_extension:
                                if '.' in target:
                                    if filename.startswith(target):
                                        stop_event.set()
                                        return os.path.join(dirpath, filename)
                                elif name_part == target:
                                    stop_event.set()
                                    return os.path.join(dirpath, filename)
                            elif filename == target:
                                stop_event.set()
                                return os.path.join(dirpath, filename)
        except Exception as e:
            logging.error(f"Error occurred: {e}")
        finally:
            queue.task_done()

    return None


def load_json_config(file_path):
    """
    Load JSON configuration file. If the file does
    not exist, create a new empty JSON file.
    """
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        if isinstance(e, IOError) and e.errno == errno.ENOENT:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w') as f:
                json.dump({'files': {}, 'folders': {}}, f)
            logging.info(f"Created new config file: {file_path}")
        else:
            logging.error(f"Error occurred: {e}")
        return {'files': {}, 'folders': {}}


def save_json_config(config, file_path):
    """
    Save the configuration dictionary to a JSON file.
    """
    with open(file_path, 'w') as f:
        json.dump(config, f)


def remove(target_path):
    if os.path.isfile(CONFIG_FILE_PATH):
        config = load_json_config(CONFIG_FILE_PATH)
        if target_path in config['files']:
            del config['files'][target_path]
            logging.info(f"Removed {target_path} from file config.")
        if target_path in config['folders']:
            del config['folders'][target_path]
            logging.info(f"Removed {target_path} from folder config.")
        save_json_config(config, CONFIG_FILE_PATH)


def reset():
    """
    Reset the JSON configuration file, removing all items.
    """
    save_json_config({'files': {}, 'folders': {}}, CONFIG_FILE_PATH)
    logging.info("Configuration file reset.")


def list_paths():
    """
    List all file paths stored in the JSON configuration file.
    """
    if os.path.isfile(CONFIG_FILE_PATH):
        paths = load_json_config(CONFIG_FILE_PATH)
        for key, value in paths.items():
            print(f"{key}:")
            for k, v in value.items():
                print(f"  {k}: {v}")
    else:
        logging.info("No configuration file found.")


def get_paths():
    """
    List all file paths stored in the JSON configuration file.
    """
    if os.path.isfile(CONFIG_FILE_PATH):
        return load_json_config(CONFIG_FILE_PATH)
    else:
        logging.info("No configuration file found.")
        return {'files': {}, 'folders': {}}


def find(target_path, folder=False, starting_dir=None,
         deprecated=False, regex=False):
    """
    Main function to find the path of a target file or folder.
    """
    path_parts = []
    if not regex:
        *path_parts, target = os.path.normpath(target_path).split(os.sep)

    dir_to_find = os.path.join(*path_parts) if path_parts else None
    start_path = os.path.expanduser(starting_dir) if starting_dir else HOME_DIR

    config = load_json_config(CONFIG_FILE_PATH)
    config_type = 'folders' if folder else 'files'

    if target_path in config[config_type]:
        saved_path = config[config_type][target_path]
        if os.path.exists(saved_path):
            logging.info(f"Found {target_path} in config.")
            return saved_path
        else:
            logging.info(f"{target_path} in config does not exist. Removing.")
            del config[config_type][target_path]
            save_json_config(config, CONFIG_FILE_PATH)

    ignore_extension = not has_extension(target) and not folder

    if not dir_to_find:
        direct_path = os.path.join(start_path, target)
        if (folder and os.path.isdir(direct_path)) or (
            not folder and (
                (ignore_extension and any(
                    f.split('.')[0] == target for f in os.listdir(start_path)
                )) or os.path.isfile(direct_path)
            )
        ):
            config[config_type][target_path] = direct_path
            save_json_config(config, CONFIG_FILE_PATH)
            return direct_path

    dir_queue = queue.Queue()
    for d in os.listdir(start_path):
        if os.path.isdir(os.path.join(start_path, d)):
            dir_queue.put(os.path.join(start_path, d))

    stop_event = threading.Event()
    found_path = None

    with ThreadPoolExecutor(max_workers=WORKERS) as executor:
        futures = [executor.submit(search_directories, dir_queue, dir_to_find,
                                   target, stop_event, ignore_extension,
                                   folder, deprecated, regex)
                   for _ in range(WORKERS)]
        for future in as_completed(futures):
            result = future.result()
            if result:
                found_path = result
                break

    if found_path:
        config[config_type][target_path] = found_path
        save_json_config(config, CONFIG_FILE_PATH)
        return found_path
    else:
        raise FileNotFoundError(f"{target_path} not found.")


def index(directory, depth=-1, exceptions=[], folders=False, hidden=False):
    """
    Function to index all files and folders in a given directory.
    """
    indexed_items = {}

    def traverse_directory(current_dir, current_depth):
        if depth != -1 and current_depth > depth:
            return

        for item in os.listdir(current_dir):
            item_path = os.path.join(current_dir, item)
            if item not in exceptions and (hidden or not item.startswith('.')):
                if folders and os.path.isdir(item_path):
                    indexed_items[item] = item_path
                elif not folders:
                    indexed_items[item] = item_path

            if os.path.isdir(item_path):
                traverse_directory(item_path, current_depth + 1)

    traverse_directory(directory, 0)
    return indexed_items
