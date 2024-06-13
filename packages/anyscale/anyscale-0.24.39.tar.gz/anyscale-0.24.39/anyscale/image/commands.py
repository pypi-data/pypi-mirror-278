from typing import Optional

from anyscale._private.sdk import sdk_command
from anyscale.image._private.image_sdk import ImageSDK
from anyscale.image.models import ImageBuild


_IMAGE_SDK_SINGLETON_KEY = "image_sdk"

_BUILD_EXAMPLE = """
import anyscale

containerfile = '''
FROM anyscale/ray:2.21.0-py39
RUN pip install --no-cache-dir pandas
'''

image_uri: str = anyscale.image.build(containerfile, name="mycoolimage")
"""


@sdk_command(
    _IMAGE_SDK_SINGLETON_KEY,
    ImageSDK,
    doc_py_example=_BUILD_EXAMPLE,
    arg_docstrings={
        "name": "The name of the image.",
        "containerfile": "The content of the Containerfile.",
        "ray_version": "The version of Ray to use in the image",
    },
)
def build(
    containerfile: str, *, name: str, _sdk: ImageSDK, ray_version: Optional[str] = None
) -> str:
    """Build an image from a Containerfile.

    Returns the URI of the image.
    """
    build_id = _sdk.build_image_from_containerfile(
        name, containerfile, ray_version=ray_version
    )
    image_uri = _sdk.get_image_uri_from_build_id(build_id)
    if image_uri:
        return image_uri.image_uri
    raise RuntimeError(
        f"This is a bug! Failed to get image uri for build {build_id} that just created."
    )


_GET_EXAMPLE = """
import anyscale

image_status = anyscale.image.get(name="mycoolimage")
"""


@sdk_command(
    _IMAGE_SDK_SINGLETON_KEY,
    ImageSDK,
    doc_py_example=_GET_EXAMPLE,
    arg_docstrings={
        "name": (
            "Get the details of an image.\n\n"
            "The name can contain an optional version, e.g., 'name:version'. "
            "If no version is provided, the latest one will be used.\n\n"
        )
    },
)
def get(*, name: str, _sdk: ImageSDK) -> ImageBuild:
    """The name can contain an optional version tag, i.e., 'name:version'.

    If no version is provided, the latest one will be returned.
    """
    return _sdk.get(name)
