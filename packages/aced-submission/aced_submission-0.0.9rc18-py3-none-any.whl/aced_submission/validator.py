import pathlib
from typing import List

from fhir.resources.fhirresourcemodel import FHIRResourceModel
from fhir.resources.coding import Coding
from fhir.resources.identifier import Identifier
from fhir.resources.reference import Reference
from dataclasses import dataclass
from urllib.parse import urlparse

from aced_submission.util import directory_reader


@dataclass
class ValidateDirectoryResult:
    """Results of FHIR validation of directory."""
    resources: List[FHIRResourceModel]
    exceptions: List[Exception]


def _check_coding(self: Coding, *args, **kwargs):
    """MonkeyPatch replacement for dict(), check Coding."""
    # note `self` is the Coding
    assert self.code, f"Missing `code` {self}"
    assert (not self.code.startswith("http")), f"`code` should _not_ be a url http {self.code}"
    assert ":" not in self.code, f"`code` should not contain ':' {self.code}"
    assert self.system, f"Missing `system` {self}"
    assert "%" not in self.system, f"`system` should be a simple url without uuencoding {self.system}"
    parsed = urlparse(self.system)
    assert parsed.scheme, f"`system` is not a URI {self}"
    assert self.display, f"Missing `display` {self}"
    # call the original dict() method
    return orig_coding_dict(self, *args, **kwargs)


def _check_identifier(self: Identifier, *args, **kwargs):
    """MonkeyPatch replacement for dict(), check Identifier."""
    # note `self` is the Identifier
    assert self.value, f"Missing `value` {self}"
    assert self.system, f"Missing `system` {self}"
    parsed = urlparse(self.system)
    assert parsed.scheme, f"`system` is not a URI {self}"
    assert "%" not in self.system, f"`system` should be a simple url without uuencoding {self.system}"
    # call the original dict() method
    return orig_identifier_dict(self, *args, **kwargs)


def _check_reference(self: Reference, *args, **kwargs):
    """MonkeyPatch replacement for dict(), check Reference."""
    # note `self` is the Identifier
    assert self.reference, f"Missing `reference` {self}"
    assert '/' in self.reference, f"Does not appear to be Relative reference {self}"
    assert 'http' not in self.reference, f"Absolute references not supported {self}"
    assert len(self.reference.split('/')) == 2, f"Does not appear to be Relative reference {self}"

    # call the original dict() method
    return orig_reference_dict(self, *args, **kwargs)


def validate_directory(directory_path: pathlib.Path) -> ValidateDirectoryResult:
    """Check FHIR data, accumulate results."""
    exceptions = []
    resources = []
    for parse_result in directory_reader(directory_path):
        if parse_result.exception:
            exceptions.append(parse_result)
        else:
            resources.append(parse_result.resource)
    return ValidateDirectoryResult(resources=resources, exceptions=exceptions)


#
# monkey patch dict() methods
#
orig_coding_dict = Coding.dict
Coding.dict = _check_coding

orig_identifier_dict = Identifier.dict
Identifier.dict = _check_identifier

orig_reference_dict = Reference.dict
Reference.dict = _check_reference
