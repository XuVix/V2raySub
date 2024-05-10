import requests
import re
from github import Github
import schedule
import time

links = ["https://aminerror.sajan87847.workers.dev/sub", "https://proxyhubc.sajan87847.workers.dev/sub"]

index = 2


file_path = "v2ray_config.txt"

github_token = "your_github_token"
github_username = "XuVix"
repository_name = "V2raySub"

def clean_data(data):

    cleaned_data = re.sub(r'^\[|\]$', '', data)
    return cleaned_data


def job():
    try:
        
        g = Github(github_token)
        
        repo = g.get_user().get_repo(repository_name)

        open(file_path, "w").close()
        
        with open(file_path, "a") as file:
            file.write("[")
            for link in links:
                index = index - 1
                response = requests.get(link)
                cleaned_text = clean_data(response.text)
                file.write(cleaned_text)
                if index != 0 :
                    file.write(",\n")
            file.write("]")

        
        try:
            existing_file = repo.get_contents(file_path)
            sha = existing_file.sha
        except Exception as e:
            sha = None

        
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

schedule.every(2).hours.do(job)


while True:
    schedule.run_pending()
    time.sleep(1)
