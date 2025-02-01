import sys
import subprocess
subprocess.check_call([sys.executable, "-m", "pip", "install", "toml"])

import toml
from datetime import datetime
import os

def get_remote_url():
    try:
        result = subprocess.run(['git', 'config', '--get', 'remote.origin.url'], capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error getting remote URL: {e}")
        return 'Unknown URL'

def get_project_metadata():
    try:
        with open('pyproject.toml', 'r') as file:
            pyproject_data = toml.load(file)

        project = pyproject_data.get('project', {})
        _project_name = project.get('name', 'Unknown Project')
        _project_version = project.get('version', 'notelab')
        _project_description = project.get('description', 'No description available')
        _project_authors = project.get('authors', [])
        _project_license = project.get('license', 'No license available')

        return _project_name, _project_version, _project_description, _project_authors, _project_license
    except Exception as e:
        print(f"Error reading pyproject.toml: {e}")
        return 'Unknown Project', 'notelab', 'No description available', [], 'No license available'

def get_description():
    try:
        with open('DESCRIPTION.md', 'r') as file:
            return file.read()
    except Exception as e:
        print(f"Error reading README.md: {e}")
        return ''

project_name, project_version, project_summary, project_authors, project_license = get_project_metadata()

author_names = [project_authors['name'] for project_authors in project_authors]
author_emails = [project_authors['email'] for project_authors in project_authors]

project_authors = ', '.join([f"{name} <a href='mailto:{email}'>{email}</a>" for name, email in zip(author_names, author_emails)])

last_updated = datetime.now().strftime('%Y-%m-%d %H:%M')
remote_url = get_remote_url()
folder_name = os.path.splitext(os.path.basename(remote_url))[0]
description = get_description()
license_link = remote_url.replace('.git', '/blob/main/LICENSE')

readme_content = f"""
## {project_name} - {project_version}
## Authors: {project_authors}
## License: [{project_license}]({license_link})
### {project_summary}

## Description
{description}

## Last Updated: {last_updated}

## Repository: [GitHub]({remote_url})

## Prerequisites:
- Python 3.11 or Conda Environment
- Bash Shell

## Installation

1. Clone the repository:
    ```sh
    git clone {remote_url}
    cd {folder_name}
    ```

2. **Run the setup script:**
   ```sh
   source ./scripts/bash/setup/setup.sh
    ```

3. **Run the application:**
   ```sh
   ./scripts/bash/run/main.sh
   ```
"""

with open("README.md", "w") as f:
    f.write(readme_content)

print("README.md generated successfully!")
