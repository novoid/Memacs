#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time-stamp: <2026-04-18 13:29:13 (klaus)>

import logging
import os
import time

from PIL import Image
from PIL.ExifTags import TAGS
from orgformat import OrgFormat

from memacs.lib.memacs import Memacs
from memacs.lib.orgproperty import OrgProperties


def get_exif_datetime(filename):
    """
    Get datetime of exif information of a file
    """

    try:
        exif_data_decoded = {}
        image = Image.open(filename)
        if hasattr(image, '_getexif'):
            exif_info = image._getexif()
            if exif_info != None:
                for tag, value in list(exif_info.items()):
                    decoded_tag = TAGS.get(tag, tag)
                    exif_data_decoded[decoded_tag] = value

        if "DateTime" in list(exif_data_decoded.keys()):
            return exif_data_decoded["DateTime"]
        if "DateTimeOriginal" in list(exif_data_decoded.keys()):
            return exif_data_decoded["DateTimeOriginal"]

    except IOError as e:
        logging.warning("IOError at %s:", filename, e)

    return None


class PhotosMemacs(Memacs):
    def _parser_add_arguments(self):
        """
        overwritten method of class Memacs

        add additional arguments
        """
        Memacs._parser_add_arguments(self)

        self._parser.add_argument(
            "-f", "--folder", dest="photo_folder",
            action="store", required=True,
            help="path to search for photos")

        self._parser.add_argument("-l", "--follow-links",
                                  dest="follow_links", action="store_true",
                                  help="follow symbolics links," + \
                                      " default False")

    def _parser_parse_args(self):
        """
        overwritten method of class Memacs

        all additional arguments are parsed in here
        """
        Memacs._parser_parse_args(self)
        if not os.path.exists(self._args.photo_folder):
            self._parser.error("photo folder does not exist")

    def check_image_header(self, filename):
        """
        recognizes image file format based on their first few bytes

        this is a replacement function for imghdr.what() which was deprecated.
        Code based on that function
        (https://github.com/python/cpython/blob/3.12/Lib/imghdr.py) and
        discussion on https://stackoverflow.com/a/14644881
        """
        with open(filename, "rb") as imgfile:
            data = imgfile.read(11)

        filetype = None

        if data[6:10] in (b"JFIF", b"EXIF"):
            filetype = "jpeg"
        if data[:4] in (b"\xff\xd8\xff\xe0", b"\xff\xd8\xff\xe1"):
            filetype = "jpeg"
        if data.startswith(b"\211PNG\r\n\032\n"):
            filetype = "png"
        if data[:6] in (b"GIF87a", b"GIF89a"):
            filetype = "gif"
        if data[:2] in (b"MM", b"II"):
            filetype = "tiff"

        return filetype

    def __handle_file(self, photo_file, filename):
        """
        checks if file is an image, try to get exif data and
        write to org file
        """

        logging.debug("handling file %s", filename)

        # check if file is an image:
        if self.check_image_header(filename) is not None:
            datetime = get_exif_datetime(filename)
            if datetime == None:
                logging.debug("skipping: %s has no EXIF information", filename)
            else:
                try:
                    datetime = time.strptime(datetime, "%Y:%m:%d %H:%M:%S")
                    timestamp = OrgFormat.date(datetime, show_time=True)
                    output = OrgFormat.link(filename, photo_file)
                    properties = OrgProperties(photo_file + timestamp)

                    self._writer.write_org_subitem(timestamp=timestamp,
                                                   output=output,
                                                   properties=properties)
                except ValueError as e:
                    logging.warning("skipping: Could not parse " + \
                                    "timestamp for %s : %s", filename, e)

    def _main(self):
        """
        get's automatically called from Memacs class
        walk through given folder and handle each file
        """

        for rootdir, dirs, files in os.walk(self._args.photo_folder,
                                    followlinks=self._args.follow_links):
            for photo_file in files:
                filename = rootdir + os.sep + photo_file
                self.__handle_file(photo_file, filename)
