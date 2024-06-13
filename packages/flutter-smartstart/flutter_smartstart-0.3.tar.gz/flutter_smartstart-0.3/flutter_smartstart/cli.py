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



def main():
    project_name = prompt("Enter the name of the project: ")
    
    if create_flutter_app(project_name):
        add_lib = prompt("Do you want to add a library ? (y/n): ")
        if add_lib.lower() == 'y':
            package_name = prompt("Enter the package name to add (eg. providers) : ")
            if package_name:
                add_libraries(package_name)
            else:
                print("Please enter the package name :")




if __name__ == '__main__':
    main()
    print("Succefully created Flutter project !")