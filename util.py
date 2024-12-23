import os
import requests
from tqdm.auto import tqdm

def download_file_with_progress(url, output_file):
    try:
        with requests.get(url, stream=True) as response:
            response.raise_for_status()

            # Determine file name and destination
            file_name = os.path.basename(response.url) if not output_file else os.path.basename(output_file)
            destination = output_file if output_file else file_name

            # Get total size from headers
            content_size = int(response.headers.get("Content-Length", 0))

            if content_size == 0:
                print("Unable to determine file size. Progress tracking might not work correctly.")

            # Configure progress bar
            with tqdm(
                total=content_size,
                desc=f"Downloading {file_name}",
                unit="B",
                unit_scale=True,
                dynamic_ncols=True,
                leave=False
            ) as progress_bar, open(destination, "wb") as file:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        file.write(chunk)
                        progress_bar.update(len(chunk))

            print(f"\nDownload completed: {destination}")

    except requests.exceptions.RequestException as err:
        print(f"Failed to download resource: {err}")
    except Exception as unexpected_error:
        print(f"An unexpected error occurred: {unexpected_error}")

if __name__ == "__main__":
    url = input("Enter the URL to download: ").strip()
    if not url:
        print("URL is required.")
        sys.exit(1)

    output_file = input("Enter the output file name (default: use file name from URL): ").strip()
    download_file_with_progress(url, output_file)