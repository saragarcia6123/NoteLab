from datetime import datetime
import toml
import subprocess
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

        project = pyproject_data.get('tool', {}).get('poetry', {})
        _project_name = project.get('name', 'Unknown Project')
        _project_version = project.get('version', 'notelab')
        _project_description = project.get('description', 'No description available')
        _project_authors = project.get('authors', [])
        _project_license = project.get('license', 'No license available')

        return _project_name, _project_version, _project_description, ', '.join(_project_authors), _project_license
    except Exception as e:
        print(f"Error reading pyproject.toml: {e}")
        return 'Unknown Project', 'notelab', 'No description available', [], 'No license available'

project_name, project_version, project_description, project_authors, project_license = get_project_metadata()

last_updated = datetime.now().strftime('%Y-%m-%d %H:%M')

remote_url = get_remote_url()
folder_name = os.path.splitext(os.path.basename(remote_url))[0]

readme_content = f"""
## {project_name} - {project_version}
## Authors: {project_authors}
## License: {project_license}

## Description
{project_description}

## Last Updated: {last_updated}

## Installation

1. Clone the repository:
    ```bash
    git clone {remote_url}
    cd {folder_name}
    ```

2. **Run the setup script:**
   ```sh
   source ./scripts/setup.sh

3. **Run the application:**
   ```sh
   ./scripts/run.sh
   ```
"""

with open("README.md", "w") as f:
    f.write(readme_content)

print("README.md generated successfully!")
