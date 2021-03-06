# Copyright 2009 Michael Murr
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

"""
Objects for Microsoft Word.

.. moduleauthor:: Michael Murr (mmurr@codeforensics.net)
"""

__docformat__ = "restructuredtext en"
__all__ = [
    "Fib", "SttbShort", "SttbLong", "SttbShortUnicode", "SttbLongUnicode"
]

from copy import copy

from lf.io.consts import SEEK_SET
from lf.datatype import Extractor, structuple
from lf.datatype.extractors import uint8, uint16_le, uint32_le

from lf.apps.msoffice.word import datatypes
from lf.apps.msoffice.word.consts import (
    NFIB_WORD_97, NFIB_WORD_2000, NFIB_WORD_2002, NFIB_WORD_2003,
    NFIB_WORD_2007
)

def extract_fib_array(record, size, stream, offset=None):
    """
    Extracts an array from the FIB.

    :parameters:
        record
            The data structure for the array.

        size
            The size of the stream (in bytes).

        stream
            A stream that contains the array.

        offset
            The start of the array.

    :rtype: structuple
    :returns: The extracted values
    """

    if size < record._size_:
        padding = b"\x00" * (record._size_ - size)
        if offset is not None:
            stream.seek(offset, SEEK_SET)
        # end if
        data = b"".join([stream.read(size), padding])
    else:
        if offset is not None:
            stream.seek(offset, SEEK_SET)
        # end if
        data = stream.read(record._size_)
    # end if

    return Extractor(record).extract(data)
# end def extract_fib_array

class Fib():
    """
    Represents the File Information Block (FIB).

    .. attribute:: header

        The FIB's header values.

    .. attribute:: shorts

        The array of short values.

    .. attribute:: longs

        The array of long values.

    .. attribute:: fc_lcb

        The array of FcLcb values.
    """

    def __init__(self, stream, offset=None):
        """
        Initializes a Fib object.

        :parameters:
            stream
                A stream that contains the FIB.

            offset
                The byte offset in the stream of the start of the FIB.
        """

        extractor = Extractor(datatypes.FibHeader)

        if offset is not None:
            stream.seek(offset, SEEK_SET)
        else:
            offset = stream.tell()
        # end if

        self.header = extractor.extract(stream.read(32))
        offset += 32

        # Get the size of the shorts array
        size = uint16_le.extract(stream.read(2))[0] * 2
        offset += 2

        # Get the shorts array
        self.shorts = extract_fib_array(
            datatypes.FibShorts, size, stream, offset
        )
        offset += size

        # Get the size of the longs array
        size = uint16_le.extract(stream.read(2))[0] * 4
        offset += 2

        # Get the longs array
        self.longs = extract_fib_array(
            datatypes.FibLongs, size, stream, offset
        )
        offset += size

        # Get the size of the fc_lcb array
        size = uint16_le.extract(stream.read(2))[0] * 8
        offset += 2

        # Figure out which data structure we need...
        if size <= 744: # Size of FibFcLcb97
            record = datatypes.FibFcLcb97
        elif size <= 864: # Size of FibFcLcb2000
            record = datatypes.FibFcLcb2000
        elif size <= 1088: # Size of FibFcLcb2002
            record = datatypes.FibFcLcb2002
        elif size <= 1312: # Size of FibFcLcb2003
            record = datatypes.FibFcLcb2003
        else:
            record = datatypes.FibFcLcb2007
        # end if

        # Get the fc_lcb array
        self.fc_lcb = extract_fib_array(record, size, stream, offset)
    # end def __init__
# end class Fib

class SttbBase():
    """
    Base class for STring TaBles (STTBs)

    .. attribute:: extended

        True if the data fields are extended (2-byte unicode).
    """

    def __init__(self, stream, offset=0):
        """
        Initializes an Sttb object.

        :parameters:
            stream
                A stream that contains the Sttb.

            offset
                The byte offset of the Sttb in the stream.
        """

        stream.seek(offset, SEEK_SET)
        if stream.read(2) == b"\xFF\xFF":
            self.extended = True
        else:
            self.extended = False
        # end if
    # end def __init__
# end class SttbBase

class SttbShort(SttbBase):
    """
    Represents a STring TaBle (STTB) with a two-byte count attribute.

    .. attribute:: extra_size

        The size of extra data fields.

    .. attribute:: data

        A list of the data elements.

    .. attribute:: extra_data

        A list of the extra data elements.
    """

    def __init__(self, stream, offset=0):
        """
        Initializes an SttbShort object.

        :parameters:
            stream
                A stream that contains the Sttb.

            offset
                The byte offset of the start of the Sttb.
        """

        super(SttbShort, self).__init__(stream, offset)
        extended = self.extended

        if extended:
            offset += 2
        # end if

        stream.seek(offset, SEEK_SET)
        count = uint16_le.extract(stream.read(2))[0]

        extra_size = uint16_le.extract(stream.read(2))[0]

        data = list()
        extra_data = list()

        for index in range(count):
            if extended:
                char_count = uint16_le.extract(stream.read(2))[0] * 2
            else:
                char_count = uint8.extract(stream.read(1))[0]
            # end if

            data.append(stream.read(char_count))
            if extra_size:
                extra_data.append(stream.read(extra_size))
            # end if
        # end for

        self.extra_size = extra_size
        self.data = data
        self.extra_data = extra_data
    # end def __init__
# end class SttbShort

class SttbLong(SttbBase):
    """
    Represents a STring TaBle (STTB) with a four-byte count attribute.

    .. attribute:: extra_size

        The size of extra data fields.

    .. attribute:: data

        A list of the data elements.

    .. attribute:: extra_data

        A list of the extra data elements.
    """

    def __init__(self, stream, offset=None):
        """
        Initializes an SttbLong object.

        :parameters:
            stream
                A stream that contains the Sttb.

            offset
                The byte offset of the start of the Sttb.
        """

        if offset is None:
            offset = stream.tell()
        # end if

        super(SttbLong, self).__init__(stream, offset)
        extended = self.extended

        if extended:
            offset += 2
        # end if

        stream.seek(offset, SEEK_SET)
        count = uint32_le.extract(stream.read(4))[0]

        extra_size = uint16_le.extract(stream.read(2))[0]

        data = list()
        extra_data = list()

        for index in range(count):
            if extended:
                char_count = uint16_le.extract(stream.read(2))[0] * 2
            else:
                char_count = uint8.extract(stream.read(1))[0]
            # end if

            data.append(stream.read(char_count))
            if extra_size:
                extra_data.append(stream.read(extra_size))
            # end if
        # end for

        self.extra_size = extra_size
        self.data = data
        self.extra_data = extra_data
    # end def __init__
# end class SttbLong

class SttbShortUnicode(SttbShort):
    """An SttbShort with data elements that are unicode"""

    def __init__(self, stream, offset=None):
        """
        Initializes an SttbShortUnicode object.

        :parameters:
            stream
                A stream that contains the Sttb.

            offset
                The start of the Sttb.
        """

        super(SttbShortUnicode, self).__init__(stream, offset)
        self.data = [element.decode("utf_16_le") for element in self.data]
    # end def __init__
# end class SttbShortUnicode

class SttbLongUnicode(SttbLong):
    """An SttbLong with data elements that are unicode"""

    def __init__(self, stream, offset=None):
        """
        Initializes an SttbLongUnicode object.

        :parameters:
            stream
                A stream that contains the Sttb.

            offset
                The start of the Sttb.
        """

        super(SttbLongUnicode, self).__init__(stream, offset)
        self.data = [element.decode("utf_16_le") for element in self.data]
    # end def __init__
# end class SttbLongUnicode
