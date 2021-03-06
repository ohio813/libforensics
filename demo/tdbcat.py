# Copyright 2010 Michael Murr
#
# This file is part of LibForensics.
#
# LibForensics is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# LibForensics is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with LibForensics.  If not, see <http://www.gnu.org/licenses/>.


"""Tool to demonstrate some of the capabilities in lf.win.shell.thumbsdb"""

# stdlib imports
import sys
from optparse import OptionParser

# local imports
from lf.dec import RawIStream, ByteIStream
from lf.win.ole.cfb import CompoundFile
from lf.win.shell.thumbsdb import ThumbsDb

# module constants
VER_MAJOR = 1
VER_MINOR = 0
VERSION_STR = "%prog {ver_major}.{ver_minor} (c) 2010 Code Forensics".format(
    ver_major=VER_MAJOR, ver_minor=VER_MINOR
)


__docformat__ = "restructuredtext en"
__all__ = [
    "main"
]

def main():
    usage = "%prog [options] thumbsdb id"
    description = "\n".join([
        "Extracts raw thumbnail data from a thumbs.db file."
        "",
        "If thumbsdb is '-', then stdin is read."
    ])

    parser = OptionParser(
        usage=usage, description=description, version=VERSION_STR
    )

    parser.add_option(
        "-c",
        dest="catalog_name",
        action="store",
        help="The name of the catalog stream (def: %default)",
        default="Catalog"
    )

    (options, args) = parser.parse_args()

    if len(args) < 2:
        parser.error("You must specify a thumbs.db file or '-' and an id")
    # end if

    if args[0] == "-":
        cfb = CompoundFile(ByteIStream(sys.stdin.buffer.read()))
    else:
        cfb = CompoundFile(RawIStream(args[0]))
    # end if

    tdb = ThumbsDb(cfb, options.catalog_name)
    entry_id = int(args[1])

    sys.stdout.buffer.write(tdb.thumbnails[entry_id].data)
# end def main

if __name__ == "__main__":
    main()
# end if
