from typing import Tuple

import pytest

from anyscale._private.anyscale_client.fake_anyscale_client import FakeAnyscaleClient
from anyscale._private.models.image_uri import ImageURI
from anyscale.image._private.image_sdk import ImageSDK
from anyscale.image.models import ImageBuild, ImageBuildStatus


@pytest.fixture()
def sdk_with_fake_client() -> Tuple[ImageSDK, FakeAnyscaleClient]:
    fake_client = FakeAnyscaleClient()
    return ImageSDK(client=fake_client), fake_client


class TestBuildImageFromRequirements:
    def test_build_image_from_requirements(
        self, sdk_with_fake_client: Tuple[ImageSDK, FakeAnyscaleClient],
    ):
        sdk, fake_client = sdk_with_fake_client
        base_image_uri = ImageURI.from_str("docker.io/my/base-image:latest")
        base_build_id = fake_client.get_cluster_env_build_id_from_image_uri(
            base_image_uri
        )
        image_name = "bldname123"
        build_id = sdk.build_image_from_requirements(
            image_name, base_build_id, requirements=["requests", "flask"],
        )

        expected_containerfile = "\n".join(
            [
                "# syntax=docker/dockerfile:1",
                f"FROM {base_image_uri}",
                'RUN pip install "requests"',
                'RUN pip install "flask"',
            ]
        )

        assert fake_client._builds[build_id].containerfile == expected_containerfile


class TestGetImage:
    def test_get_image(self, sdk_with_fake_client: Tuple[ImageSDK, FakeAnyscaleClient]):
        sdk, fake_client = sdk_with_fake_client
        fake_client.get_cluster_env_build_id_from_containerfile(
            "my-image", "FROM python:3.8", anonymous=False, ray_version="2.24.0"
        )
        img_build = sdk.get("my-image")
        assert img_build == ImageBuild(
            status=ImageBuildStatus.SUCCEEDED,
            uri="anyscale/image/my-image:1",
            ray_version="2.24.0",
        )
