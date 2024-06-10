# Copyright (C) 2024 Kian-Meng Ang
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Affero General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more
# details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

"""Info subcommand."""

import argparse
import logging

from PIL import ExifTags, Image

log = logging.getLogger(__name__)


def build_subparser(subparsers) -> None:
    """Build the subparser."""
    info_parser = subparsers.add_parser("info", help="info an image")

    info_parser.set_defaults(func=run)

    info_parser.add_argument(
        dest="image_filename",
        help="set the image filename",
        type=str,
        default=None,
        metavar="IMAGE_FILENAME",
    )


def run(args: argparse.Namespace) -> None:
    """Run info subcommand.

    Args:
        config (argparse.Namespace): Config from command line arguments

    Returns:
        None
    """
    log.debug(args)

    image = Image.open(args.image_filename)
    exif = image._getexif()
    info = {ExifTags.TAGS.get(tag_id): exif.get(tag_id) for tag_id in exif}

    tag_name_width = max(map(len, info))
    for tag_name, tag_value in info.items():
        print(f"{tag_name:<{tag_name_width}}: {tag_value}")
