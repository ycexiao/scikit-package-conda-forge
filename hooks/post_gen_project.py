import warnings
from hashlib import sha256
from pathlib import Path

import requests

# Get SHA256 hash from the PyPI .tar file
pkg_name = "{{ cookiecutter.package_import_name }}".replace(".", "_").replace("-", "_").lower()
pypi_source_URL = f"https://pypi.org/packages/source/{pkg_name[0]}/{pkg_name}/{pkg_name}-{{ cookiecutter.version }}.tar.gz"
tar_gz_dist = requests.get(pypi_source_URL)
tar_gz_sha256 = sha256(tar_gz_dist.content).hexdigest()

# Warn the user if there is no package found on PyPI
if tar_gz_sha256 == "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855":
    raise ValueError(
        "Empty file detected: No SHA256 value was retrieved. "
        "This typically means the source file is empty or missing. "
        "Please ensure your package is uploaded to PyPI and the version number is correct. "
        "Then re-run - package create conda-forge"
    )

# Read the template meta.yml file line by line and replace the placeholders
meta_yml_path = Path.cwd() / "meta.yaml"
with open(meta_yml_path, 'r') as mfile:
    meta_yml_text = mfile.read()

    # Add the SHA256 and SOURCE
    meta_yml_text = meta_yml_text.replace("GENERATE_SHA", f"{tar_gz_sha256}")
    meta_yml_text = meta_yml_text.replace("GENERATE_PYPI_URL", f"{pypi_source_URL}")

    def add_list(csv, replace_string, txt):
        file_txt = txt
        csv_list = list(map(str.strip, csv.split(',')))
        csv_list_pruned = []
        for element in csv_list:
            if len(element) > 0:
                # Requirements version formatting
                while ">= " in element:
                    element = element.replace(">= ", ">=")
                csv_list_pruned.append(element)
        csv_list = csv_list_pruned
        if len(csv_list) == 0:
            # Depends on how the carriage return is stored
            file_txt = file_txt.replace(f"\n    - {replace_string}", "")
        else:
            csv_str = "\n    - ".join(csv_list)
            file_txt = file_txt.replace(f"{replace_string}", csv_str)
        return file_txt

    # Add the build requirements
    meta_yml_text = add_list("{{ cookiecutter.build_requirements }}", "GENERATE_BUILD_REQUIREMENTS", meta_yml_text)

    # Add the host requirements
    meta_yml_text = add_list("{{ cookiecutter.host_requirements }}", "GENERATE_HOST_REQUIREMENTS", meta_yml_text)

    # Add the runtime requirements
    meta_yml_text = add_list("{{ cookiecutter.runtime_requirements }}", "GENERATE_RUN_REQUIREMENTS", meta_yml_text)

    # Add the testing requirements
    meta_yml_text = add_list("{{ cookiecutter.testing_requirements }}", "GENERATE_TEST_REQUIREMENTS", meta_yml_text)

    # Add the maintainers
    meta_yml_text = add_list("{{ cookiecutter.recipe_maintainers }}", "GENERATE_MAINTAINERS", meta_yml_text)

with open(meta_yml_path, 'w') as mfile:
    mfile.write(meta_yml_text)

print("Done! meta.yaml file has been created under the new {{ cookiecutter.package_import_name }} directory.")