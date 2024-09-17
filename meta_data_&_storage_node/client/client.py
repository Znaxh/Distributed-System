import os
import requests

# Metadata server URL (e.g., where your metadata server is running)
METADATA_SERVER_URL = "http://localhost:5000"
# Storage node URL (e.g., where your storage node is running)
STORAGE_NODE_URL = "http://localhost:6000"

# Function to upload a file to the storage node
def upload_file_to_storage_node(file_path):
    url = f"{STORAGE_NODE_URL}/upload"
    files = {'file': open(file_path, 'rb')}

    response = requests.post(url, files=files)

    if response.status_code == 200:
        print(f"File '{file_path}' uploaded successfully to storage node.")
        return True
    else:
        print(f"Error uploading file '{file_path}': {response.json()}")
        return False

# Function to inform the metadata server about the file's location
def inform_metadata_server(file_name, storage_node_url):
    url = f"{METADATA_SERVER_URL}/add_file"
    data = {
        "filename": file_name,
        "storage_node": storage_node_url
    }

    response = requests.post(url, json=data)

    if response.status_code == 200:
        print(f"Metadata for '{file_name}' added successfully to metadata server.")
        return True
    else:
        print(f"Error adding metadata for '{file_name}': {response.json()}")
        return False

# Function to download a file by retrieving the correct storage node address from the metadata server
def download_file_from_storage(file_name, download_directory):
    # Step 1: Query the metadata server for the file location
    url = f"{METADATA_SERVER_URL}/get_file"
    response = requests.get(url, params={'filename': file_name})

    if response.status_code == 200:
        file_info = response.json()
        storage_node_url = file_info.get('storage_node')
        print(f"File '{file_name}' is stored at {storage_node_url}")

        # Step 2: Request the file from the storage node
        download_url = f"{storage_node_url}/download/{file_name}"
        download_response = requests.get(download_url)

        if download_response.status_code == 200:
            # Save the file to the specified download directory
            save_path = os.path.join(download_directory, file_name)
            with open(save_path, 'wb') as f:
                f.write(download_response.content)
            print(f"File '{file_name}' downloaded successfully to '{save_path}'.")
            return True
        else:
            print(f"Error downloading file '{file_name}': {download_response.status_code}")
            return False
    else:
        print(f"Error retrieving file location for '{file_name}': {response.json()}")
        return False

# Example usage
if __name__ == '__main__':
    file_path = 'C:/Users/Anurag/Desktop/example.txt'  # Your file path
    file_name = file_path.split('/')[-1]

    # Set the download directory
    download_directory = 'E:/Projects/Academics/Distributed-System/meta_data_&_storage_node/client/client-storage'  # Your custom download location

    # Step 1: Upload the file to the storage node
    if upload_file_to_storage_node(file_path):
        # Step 2: Inform the metadata server about the file's location
        if inform_metadata_server(file_name, STORAGE_NODE_URL):
            # Step 3: Download the file to the custom download directory
            download_file_from_storage(file_name, download_directory)
