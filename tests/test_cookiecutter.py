import filecmp
from pathlib import Path

from cookiecutter.main import cookiecutter


def test_meta_yaml_matches_reference(tmp_path):
    cookiecutter(
        ".",
        no_input=True,
        extra_context={
            "github_username_or_orgname": "diffpy",
            "package_import_name": "diffpy.pdfgui",
            "github_repo_name": "diffpy.pdfgui",
            "version": "3.1.0",
            "min_python_version": "3.11",
            "project_short_description": "Python package for doing science.",
            "project_full_description": "This is a Python package for doing science.",  # noqa: E501
            "license_file": "LICENSE.rst",
            "recipe_maintainers": "sbillinge, bobleesj",
            "build_requirements": "",
            "host_requirements": "setuptools, setuptools-git-versioning >=2.0, pip",  # noqa: E501
            "runtime_requirements": "numpy",
            "testing_requirements": "pip, pytest",
        },
        output_dir=str(tmp_path),
    )
    actual_meta = tmp_path / "diffpy.pdfgui" / "meta.yaml"
    expected_meta = Path("tests/diffpy.example/meta.yaml")
    assert filecmp.cmp(actual_meta, expected_meta)
