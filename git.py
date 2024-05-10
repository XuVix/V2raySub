import requests
import re
from github import Github
import schedule
import time

# The links from which we will retrieve the data
links = [""]

# The file to save the retrieved data
file_path = "v2ray_config.txt"

# Enter your GitHub token here
github_token = "your_github_token"
github_username = "XuVix"
repository_name = "V2raySub"

def clean_data(data):
    # Remove [] at the beginning and end of the data
    cleaned_data = re.sub(r'^\[|\]$', '', data)
    return cleaned_data


def job():
    try:
        # Establish connection to GitHub
        g = Github(github_token)

        # Find the repository
        repo = g.get_user().get_repo(repository_name)

        # Clear existing content of the file
        open(file_path, "w").close()

        # Aggregate data from all links and save it to the file
        with open(file_path, "a") as file:
            file.write("[")
            for link in links:
                response = requests.get(link)
                cleaned_text = clean_data(response.text)
                file.write(cleaned_text)
                file.write(",\n")  # Add two empty lines as a separator between each data
            file.write("]")

        # Get the SHA checksum of the existing file (if it exists)
        try:
            existing_file = repo.get_contents(file_path)
            sha = existing_file.sha
        except Exception as e:
            sha = None

        # Upload the file to GitHub
        with open(file_path, "r") as file:
            content = file.read()
            if sha:
                repo.update_file(file_path, "Commit message", content, sha)
            else:
                repo.create_file(file_path, "Commit message", content)

        print("Data successfully retrieved from all links and uploaded to GitHub.")

    except Exception as e:
        print(f"An error occurred: {e}")

job()
# Schedule the job to run every two hours
schedule.every(2).hours.do(job)

# Run the scheduler
while True:
    schedule.run_pending()
    time.sleep(1)
