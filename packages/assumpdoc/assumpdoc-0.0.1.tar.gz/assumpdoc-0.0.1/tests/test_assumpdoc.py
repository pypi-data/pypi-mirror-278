"""Top level package tests."""

import re

import assumpdoc


class TestAssumpdocPackage:
    """Top level tests for the assumpdoc package name and version number."""

    def test_package_name(self):
        """Test package name."""
        assert (
            assumpdoc.__name__ == "assumpdoc"
        ), f"Package name is not `assumpdoc`. Got {assumpdoc.__name__}."

    def test_version(self):
        """Test package version method is accessible."""
        # regex expression taken from https://semver.org/#is-there-a-suggested-
        # regular-expression-regex-to-check-a-semver-string
        pattern = (
            r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-((?:0|[1-9]\d*|\d*["
            r"a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-"
            r"]*))*))?(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$"
        )
        assert re.search(pattern, assumpdoc.__version__), (
            "Package version does not follow expected semvar format. Got "
            f"{assumpdoc.__version__}"
        )
