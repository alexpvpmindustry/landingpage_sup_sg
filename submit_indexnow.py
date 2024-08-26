import os
import requests
import json

# Define the domain and other key configurations at the top
MAIN_DOMAIN = "sup.sg"  # Replace with your domain
API_KEY = "wxymwdh24smu6s2wr54d826zsrbqm21a"
KEY_LOCATION = f"https://{MAIN_DOMAIN}/wxymwdh24smu6s2wr54d826zsrbqm21a.txt"

def find_html_files(root_directory, main_domain):
    html_files = []
    # Walk through the directory to find all .html files
    for root, dirs, files in os.walk(root_directory):
        for file in files:
            if file.endswith(".html"):
                # Construct the relative path from the root directory
                relative_path = os.path.relpath(os.path.join(root, file), root_directory)
                url = f"https://{main_domain}/{relative_path.replace(os.path.sep, '/')}"
                html_files.append(url)
    return html_files

def submit_to_indexnow(api_key, host, key_location, urls, dry_run=False):
    if dry_run:
        print("Dry run mode enabled. The following URLs would be submitted to IndexNow:")
        for url in urls:
            print(url)
        return 200, "Dry run completed. No actual request made."
    
    url = "https://api.indexnow.org/indexnow"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "host": host,
        "key": api_key,
        "keyLocation": key_location,
        "urlList": urls
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    
    return response.status_code, response.text

if __name__ == "__main__":
    # Root directory to search for HTML files (current directory)
    root_directory = "."

    # Ask the user if they want to do a dry run
    dry_run_input = input("Would you like to perform a dry run? (yes/no): ").strip().lower()
    dry_run = dry_run_input == "yes"

    # Find all .html files in the root and subdirectories
    all_html_files = find_html_files(root_directory, MAIN_DOMAIN)
    
    if all_html_files:
        print(f"Found {len(all_html_files)} HTML files.")
        # Submit to IndexNow (or dry run)
        status_code, response_text = submit_to_indexnow(API_KEY, MAIN_DOMAIN, KEY_LOCATION, all_html_files, dry_run)
        print(f"Response Code: {status_code}")
        print(f"Response Text: {response_text}")
    else:
        print("No HTML files found.")
