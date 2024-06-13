import os


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