import requests
from github import Github

# The link from which we will retrieve the data
link = "https://aminerror.sajan87847.workers.dev/sub"

# The file to save the retrieved data
file_path = "v2ray_config.txt"

# Enter your GitHub token and username here
github_token = "your_github_token"
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

    try:
        # Upload the file to GitHub
        with open(file_path, "r") as file:
            content = file.read()
            repo.create_file(file_path, "Commit message", content)

        print("Data successfully retrieved and uploaded to GitHub.")

    except Exception as upload_error:
        print(f"An error occurred while uploading to GitHub: {upload_error}")

except Exception as e:
    print(f"An error occurred: {e}")
      
