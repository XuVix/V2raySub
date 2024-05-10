import requests
from github import Github

# The link from which we will retrieve the data
link = "https://aminerror.sajan87847.workers.dev/sub"

# The file to save the retrieved data
file_path = "v2ray_config.txt"

# Enter your GitHub token and username here
github_token = "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"
github_username = "XuVix"
repository_name = "V2raySub"

try:
    # Establish connection to GitHub
    g = Github(github_token)

    # Find the repository
    repo = g.get_user().get_repo(repository_name)

    # Retrieve data from the link and save it to the file
    response = requests.get(link)
    with open(file_path, "w") as file:
        file.write(response.text)

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

    print("Data successfully retrieved and uploaded to GitHub.")

except Exception as e:
    print(f"An error occurred: {e}")
