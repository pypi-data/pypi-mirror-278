import os
import subprocess
from prompt_toolkit import prompt
from prompt_toolkit.validation import Validator, ValidationError

def create_flutter_app(project_name):
    try:
        subprocess.run(["flutter", "create", project_name], check=True)
    except subprocess.CalledProcessError:
        print("Failed to create Flutter project")
        return False

    os.chdir(project_name)
    add_custom_files()
    return True

def add_custom_files():
    readme_content = ''' # Flutter App
   Welcome to the custom flutter app @iambkpl '''

    with open("README.md", 'w') as f:
       f.write(readme_content)


def add_libraries(package_name):
    try:
        subprocess.run(["flutter", "pub", "add", package_name], check=True)
    except subprocess.CalledProcessError:
        print("Failed to get Flutter packages")



def create_clean_code_folder_structure(base_path, feature_name="feature_name"):
    root_folders = ["assets", "lib"]

    sub_root_folders = {
        "assets": ["images", "fonts"],
        "lib": ["core", feature_name],
    }

    sub_folders = {
        "lib/core": ["connection", "constants", "errors", "param"],
        f"lib/{feature_name}": ["business", "data", "presentation"],
    }

    business_sub_folders = ["entities", "repositories", "usecases"]
    data_sub_folders = ["datasources", "models", "repositories"]
    presentation_sub_folders = ["pages", "widgets", "providers"]

    for folder in root_folders:
        os.makedirs(os.path.join(base_path, folder), exist_ok=True)

    for root, subs in sub_root_folders.items():
        for sub in subs:
            os.makedirs(os.path.join(base_path, root, sub), exist_ok=True)

    for root, subs in sub_folders.items():
        for sub in subs:
            os.makedirs(os.path.join(base_path, root, sub), exist_ok=True)

    for folder in business_sub_folders:
        os.makedirs(os.path.join(base_path, "lib", feature_name, "business", folder), exist_ok=True)

    for folder in data_sub_folders:
        os.makedirs(os.path.join(base_path, "lib", feature_name, "data", folder), exist_ok=True)

    for folder in presentation_sub_folders:
        os.makedirs(os.path.join(base_path, "lib", feature_name, "presentation", folder), exist_ok=True)

"""
What is your project named? my-app
Would you like to use TypeScript? No / Yes
Would you like to use ESLint? No / Yes
Would you like to use Tailwind CSS? No / Yes
Would you like to use `src/` directory? No / Yes
Would you like to use App Router? (recommended) No / Yes
Would you like to customize the default import alias (@/*)? No / Yes
What import alias would you like configured? @/*
"""
def main():
    action = prompt(""" What would you like to do? \n 1. Create a flutter project \n 2. Create a folder structure \n 3. Install a package \n 4. Exit \n""")
    
    project_name = ""
    while action != "4":
        if action == '1':
            project_name = prompt("What is your project named? ")
            create_flutter_app(project_name)
            print("Successfully created flutter app")
            continue
        
        elif action == "2":
            feature_name = prompt("What is your feature name (eg. auth, users ....) ? ")
            create_clean_code_folder_structure(project_name, feature_name)
            continue
            
        elif action =="3":
            package_name = prompt("Enter the package name to add (eg. providers) : ")
            add_libraries(package_name)
            continue
        
        else:
              action = prompt(""""
                    What would you like to do? \n 
                    1. Create a flutter project \n
                    2. Create a folder structure \n
                    3. Install a package \n
                    4. Exit \n
                    """)
    
    # if create_flutter_app(project_name):
    #     add_lib = prompt("Do you want to add a library ? (y/n): ")
    #     if add_lib.lower() == 'y':
    #         package_name = prompt("Enter the package name to add (eg. providers) : ")
    #         if package_name:
    #             add_libraries(package_name)
    #         else:
    #             print("Please enter the package name :")




if __name__ == '__main__':
    main()
    print("Bye :)")