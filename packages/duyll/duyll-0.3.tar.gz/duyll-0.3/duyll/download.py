import os
import requests

# Define the URL of the file to be downloaded
def download_model():
    url = "https://huggingface.co/DuySota/retouch/resolve/main/pretrained_weights/pytorch_model.pth?download=true"
    url_yml = "https://huggingface.co/DuySota/retouch/resolve/main/RetinexFormer_FiveK.yml?download=true"

    # Get the user's home directory
    home_dir = os.path.expanduser("~")

    # Define the .cache directory path
    cache_dir = os.path.join(home_dir, ".cache/retouchsota")

    # Create the .cache directory if it doesn't exist
    os.makedirs(cache_dir, exist_ok=True)

    # Define the output path for the downloaded file
    output_path = os.path.join(cache_dir, "pytorch_model.pth")
    output_path_yml = os.path.join(cache_dir, "model.yml")

    # Check if the file already exists
    if not os.path.exists(output_path):
        # Download the file
        response = requests.get(url)
        if response.status_code == 200:
            with open(output_path, 'wb') as file:
                file.write(response.content)
            print(f"File downloaded successfully and saved as {output_path}")
        else:
            print(f"Failed to download file. Status code: {response.status_code}")
    else:
        print(f"File already exists at {output_path}. No download needed.")

    if not os.path.exists(output_path_yml):
        # Download the file
        response = requests.get(url_yml)
        if response.status_code == 200:
            with open(output_path_yml, 'wb') as file:
                file.write(response.content)
            print(f"File downloaded successfully and saved as {output_path_yml}")
        else:
            print(f"Failed to download file. Status code: {response.status_code}")
    else:
        print(f"File already exists at {output_path_yml}. No download needed.")


download_model()