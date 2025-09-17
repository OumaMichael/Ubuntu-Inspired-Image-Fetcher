import requests
import os
from urllib.parse import urlparse
import hashlib

def get_filename_from_url(url):
    """
    Extract filename from URL. If missing, generate one using a hash.
    """
    parsed_url = urlparse(url)
    filename = os.path.basename(parsed_url.path)
    
    if not filename or "." not in filename:
        # Generate a unique filename if none exists
        hash_name = hashlib.md5(url.encode()).hexdigest()[:10]
        filename = f"image_{hash_name}.jpg"
    
    return filename

def fetch_image(url, folder="Fetched_Images"):
    """
    Download a single image from a URL and save it in the given folder.
    Handles errors gracefully in the Ubuntu spirit of respect.
    """
    try:
        # Create folder if it doesn't exist
        os.makedirs(folder, exist_ok=True)

        # Fetch image
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        # Extract filename
        filename = get_filename_from_url(url)
        filepath = os.path.join(folder, filename)

        # Prevent duplicates
        if os.path.exists(filepath):
            print(f"⚠ Skipped (duplicate): {filename}")
            return

        # Check Content-Type header before saving
        content_type = response.headers.get("Content-Type", "")
        if not content_type.startswith("image/"):
            print(f"✗ Not an image: {url} (Content-Type: {content_type})")
            return

        # Save image in binary mode
        with open(filepath, "wb") as f:
            f.write(response.content)

        print(f"✓ Successfully fetched: {filename}")
        print(f"✓ Image saved to {filepath}")

    except requests.exceptions.RequestException as e:
        print(f"✗ Connection error: {e}")
    except Exception as e:
        print(f"✗ An error occurred: {e}")

def main():
    print("Welcome to the Ubuntu Image Fetcher")
    print("A tool for mindfully collecting images from the web")
    print("Ubuntu: I am because we are 🌍\n")

    # Ask user for one or multiple URLs
    urls = input("Please enter image URL(s), separated by commas:\n").split(",")

    for url in [u.strip() for u in urls if u.strip()]:
        fetch_image(url)

    print("\nConnection strengthened. Community enriched.")

if __name__ == "__main__":
    main()
