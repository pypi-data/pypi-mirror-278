import os
import json
import hashlib
from astropy.io import fits

CACHE_FILENAME = '.astrostats'

def calculate_checksum(file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def read_exposure_from_fits(file_path):
    try:
        with fits.open(file_path) as hdul:
            header = hdul[0].header
            if 'EXPTIME' in header:
                return int(header['EXPTIME'])
    except Exception as e:
        print(f"Error reading FITS file {file_path}: {e}")
    return None

def calculate_directory_hash(root_dir):
    sha256_hash = hashlib.sha256()
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in sorted(filenames):
            file_path = os.path.join(dirpath, filename)
            if filename.endswith(".fit"):
                total_size += os.path.getsize(file_path)
                sha256_hash.update(filename.encode())
                sha256_hash.update(str(os.path.getsize(file_path)).encode())
    return sha256_hash.hexdigest(), total_size

def load_cache(root_dir):
    cache_file = os.path.join(root_dir, CACHE_FILENAME)
    if os.path.exists(cache_file):
        with open(cache_file, 'r') as f:
            return json.load(f)
    return {}

def save_cache(root_dir, cache_data):
    cache_file = os.path.join(root_dir, CACHE_FILENAME)
    with open(cache_file, 'w') as f:
        json.dump(cache_data, f)

def is_cache_valid(root_dir):
    cache_data = load_cache(root_dir)
    if 'directory_hash' not in cache_data or 'total_size' not in cache_data:
        return False
    current_hash, current_size = calculate_directory_hash(root_dir)
    return current_hash == cache_data['directory_hash'] and current_size == cache_data['total_size']

def update_cache(root_dir):
    cache_data = load_cache(root_dir)
    current_hash, current_size = calculate_directory_hash(root_dir)

    exposure_cache = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith(".fit"):
                file_path = os.path.join(dirpath, filename)
                exposure = read_exposure_from_fits(file_path)
                if exposure is not None:
                    exposure_cache.append({"dirpath": dirpath, "filename": filename, "exposure": exposure})

    cache_data['exposure_cache'] = exposure_cache
    cache_data['directory_hash'] = current_hash
    cache_data['total_size'] = current_size

    save_cache(root_dir, cache_data)
    return exposure_cache

def get_cached_data(root_dir):
    cache_data = load_cache(root_dir)
    return cache_data.get('exposure_cache', [])
