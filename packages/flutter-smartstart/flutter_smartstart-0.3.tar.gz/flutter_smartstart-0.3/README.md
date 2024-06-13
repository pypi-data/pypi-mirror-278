# Flutter SmartStart

Flutter SmartStart is a CLI tool to create and customize Flutter projects with a clean code folder structure. It helps you quickly set up a new Flutter project with a standardized and maintainable architecture.

## Features

- Interactive prompts for project name, package name, and package version
- Automatically adds specified packages to `pubspec.yaml`
- Creates a README.md file with project information
- Ensures a clean and organized code structure

## Installation

You can install Flutter SmartStart using `pip`:

```sh
    pip install flutter-smartstart
```

## Usage

Run the flutter-smartstart command and follow the prompts to create a new Flutter project:

```shell
Copy code
Enter the name of the Flutter project: my_flutter_app
Enter the package name to add (e.g., provider): provider
Enter the package version (e.g., ^6.0.0): ^6.0.0
After providing the inputs, Flutter SmartStart will create the Flutter project, add the specified package, and set up the initial folder structure.
```

### Project Structure

The generated Flutter project will have the following structure:

```css
my_flutter_app/
├── android/
├── ios/
├── lib/
│   ├── main.dart
│   └── ... (your Flutter code here)
├── test/
├── pubspec.yaml
├── README.md
└── ...
```

Contact
If you have any questions or feedback, feel free to open an issue or reach out to the project maintainer:

Name: Kapil Bhandari
Email: iam.bkpl03@gmail.com
