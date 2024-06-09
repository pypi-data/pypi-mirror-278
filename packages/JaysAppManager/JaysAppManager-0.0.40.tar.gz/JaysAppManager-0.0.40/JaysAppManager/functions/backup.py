import os
import zipfile
import hashlib
import json
import docker
from b2sdk.v1 import InMemoryAccountInfo, B2Api
from base64 import b64encode
from Crypto.Cipher import ChaCha20
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import scrypt
from Crypto.Util.Padding import pad, unpad

def hash_file(file_path):
    """Calculate the SHA-256 hash of a file."""
    with open(file_path, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()

def create_zip_with_manifest(directory, zip_file_path, manifest):
    """Create a zip file with all files in the directory and a manifest."""
    with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, directory))
        # Write the manifest to a JSON file inside the zip
        with zipf.open('manifest.json', 'w') as manifest_file:
            manifest_file.write(json.dumps(manifest, indent=4).encode('utf-8'))

def encrypt_file(file_path, password):
    """Encrypt a file using ChaCha20."""
    # Generate a key from the password using scrypt
    salt = get_random_bytes(16)
    key = scrypt(password, salt, key_len=32, N=2**20, r=8, p=1)
    
    # Read the file data
    with open(file_path, 'rb') as file:
        data = file.read()
    
    # Pad the data if necessary
    data = pad(data, ChaCha20.block_size)
    
    # Generate a random nonce
    nonce = get_random_bytes(12)
    
    # Encrypt the data
    cipher = ChaCha20.new(key=key, nonce=nonce)
    ciphertext = cipher.encrypt(data)
    
    # Write the encrypted data to a new file
    encrypted_file_path = file_path + '.enc'
    with open(encrypted_file_path, 'wb') as file:
        file.write(nonce + salt + ciphertext)
    
    # Remove the original file
    os.remove(file_path)
    
    return encrypted_file_path



def upload_to_backblaze(b2_api, bucket_name, file_path, file_name):
    """Upload a file to Backblaze B2."""
    bucket = b2_api.get_bucket_by_name(bucket_name)
    bucket.upload_local_file(
        local_file=file_path,
        file_name=file_name,
    )

def list_mounted_volumes_inside_container():
    """List all volumes mounted inside a Docker container, hash each file, and create a backup."""
    client = docker.from_env()
    container_id = os.environ.get('HOSTNAME')  # Get the container ID from the environment
    container = client.containers.get(container_id)
    mounts = container.attrs['Mounts']

    manifest = {}
    for mount in mounts:
        source_path = mount['Source']
        destination_path = mount['Destination']
        if os.path.isdir(destination_path):
            for root, dirs, files in os.walk(destination_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    file_hash = hash_file(file_path)
                    manifest[file_path] = file_hash

    # Create a temporary zip file path
    zip_file_path = '/tmp/backup.zip'
    create_zip_with_manifest(source_path, zip_file_path, manifest)

    # Encrypt the zip file
    password = 'your_password'  # Replace with your actual password
    encrypt_file(zip_file_path, password)

    # Initialize the Backblaze B2 API
    info = InMemoryAccountInfo()
    b2_api = B2Api(info)
    b2_api.authorize_account("applicationKeyId", "applicationKey")  # Replace with your Backblaze B2 applicationKeyId and applicationKey

    # Upload the encrypted zip file to Backblaze B2
    bucket_name = 'your_bucket_name'  # Replace with your Backblaze B2 bucket name
    file_name_in_bucket = 'backup.zip'  # Replace with the file name you want to use in Backblaze B2
    upload_to_backblaze(b2_api, bucket_name, zip_file_path, file_name_in_bucket)

    # Clean up the temporary zip file
    os.remove(zip_file_path)

# Call the function
list_mounted_volumes_inside_container()

manifest = list_mounted_volumes_inside_container()

def docker():
    return os.path.exists('/.dockerenv')