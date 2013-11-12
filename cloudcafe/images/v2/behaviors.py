"""
Copyright 2013 Rackspace

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from cafe.engine.behaviors import BaseBehavior
from cloudcafe.common.resources import ResourcePool
from cloudcafe.common.tools.datagen import rand_name
from cloudcafe.images.common.types import \
    ImageContainerFormat, ImageDiskFormat, ImageVisibility


class ImagesV2Behaviors(BaseBehavior):
    """@summary: Behaviors class for images v2"""

    def __init__(self, images_client, images_config):
        super(ImagesV2Behaviors, self).__init__()
        self.config = images_config
        self.client = images_client
        self.resources = ResourcePool()

    def register_basic_image(self):
        """
        @summary: Register a basic image, add it for deletion and return the
        image id
        """

        response = self.client.create_image(
            container_format=ImageContainerFormat.BARE,
            disk_format=ImageDiskFormat.RAW, name=rand_name('image'),
            visibility=ImageVisibility.PUBLIC)
        image = response.entity
        self.resources.add(self.client.delete_image, image.id)
        return image.id

    def register_private_image(self):
        """
        @summary: Register a private image, add it for deletion and return the
        image id
        """

        response = self.client.create_image(
            container_format=ImageContainerFormat.BARE,
            disk_format=ImageDiskFormat.RAW, name=rand_name('image'),
            visibility=ImageVisibility.PRIVATE)
        image = response.entity
        self.resources.add(self.client.delete_image, image.id)
        return image.id

    def get_member_ids(self, image_id):
        """
        @summary: Return a complete list of ids for all members for a given
        image id
        """

        response = self.client.list_members(image_id)
        return [member.member_id for member in response.entity]
