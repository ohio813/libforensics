

# Introduction #

These are a series of small tools I wrote to demonstrate some of the
functionality within the framework. The coding isn't the best, but gets the
job done.

All of the tools will read from standard in, if you don't give them a file
name. If you're on a Windows system, you'll have to make sure to run python
with the -u option (to force stdin to be unbuffered.) Each file has it's own
readme with more information and examples.

Feel free to use the tools, and report and bugs you find to the issue tracker
at libforensics.com.

  * datedecoder.py: decodes various timestamp formats
  * info2ls.py: Lists the contents of INFO2 (recycle bin) files
  * info2stat.py: Prints statistics about a specific entry in an INFO2 file
  * olels.py: Lists the directory entries in an OLE compound file
  * olestat.py: Prints statistics about a directory entry in an OLE compound file
  * olecat.py: Extracts the contents of a stream in an OLE compound file
  * oleps.py: Displays property sets from a stream in an OLE compound file
  * tdbls.py: Lists entries in a thumbs.db file
  * tdbstat.py: Displays statistics about a specific entry in a thumbs.db file
  * tdbcat.py: Extracts thumbnail images from thumbs.db files
  * wmg.py: extracts metadata from Microsoft Word documents
  * recdump.py: Dumps information about record data types (data structures)
  * lnkinfo.py: Dumps information from shell link (.lnk, shortcut) files

# Tools #

## datedecoder.py ##
From demo/README.datedecoder.txt

<pre>
Decodes various timestamp formats.<br>
<br>
<br>
Usage:<br>
------<br>
<br>
$ python3.1 datedecoder.py  -h<br>
Usage: datedecoder.py [options] timestamp<br>
<br>
Decodes various timestamp formats.  If timestamp is '-' then stdin is read.<br>
<br>
Options:<br>
--version             show program's version number and exit<br>
-h, --help            show this help message and exit<br>
-b BASE, --base=BASE  The numeric base for the input (def: 16).  This only<br>
applies when the input type is int.<br>
-m INPUT_MODE, --input-mode=INPUT_MODE<br>
Set input to (binary, text) (def: text).  Binary is<br>
only available when reading from stdin.<br>
-i TYPE, --input-type=TYPE<br>
The data type of timestamp (int, float).  The default<br>
for variant timestamps is float.  For all other<br>
timestamps the default is int.<br>
-t TIMESTAMP_TYPE, --timestamp-type=TIMESTAMP_TYPE<br>
The type of timestamp (filetime, unix|posix, dosdate,<br>
dostime, variant).<br>
-e ENDIAN, --endian=ENDIAN<br>
The byte order to use (big, little). (def: little).<br>
This only applies when the input type is int.<br>
-s FORMAT, --format-str=FORMAT<br>
The format string to print the decoded timestamp.  If<br>
this is not specified ISO 8601 format is used.<br>
-f, --filetime        Implies -t filetime<br>
-u, --unix            Implies -t unix<br>
-p, --posix           Implies -t posix<br>
-d, --decimal         Implies -b 10<br>
-x, --hex             Implies -b 16<br>
<br>
<br>
Examples:<br>
---------<br>
<br>
1) Decoding a Windows FILETIME timestamp in little endian:<br>
<br>
$ python3.1 datedecoder.py -f -e little 0x0008f4eb6f04ca01<br>
2009-07-14 10:43:28<br>
<br>
<br>
2) Decoding the same timestamp, as a decimal, in big endian, using a custom<br>
format string:<br>
<br>
$ python3.1 datedecoder.py -f -e big -d 128920418080000000 \<br>
-s "%m/%d/%Y %H:%M:%S"<br>
07/14/2009 10:43:28<br>
<br>
<br>
3) Decoding a variant timestamp:<br>
<br>
$ python3.1 datedecoder.py -t variant 3.25<br>
1900-01-02 06:00:00<br>
<br>
<br>
4) Decoding the same timestamp, this time it is a little endian decimal value:<br>
<br>
$ python3.1 datedecoder.py -t variant -i int -d -e little 2624<br>
1900-01-02 06:00:00<br>
<br>
<br>
5) Decoding a binary timestamp, little endian embedded in a word document<br>
(blair.doc from http://www.computerbytesman.com/privacy/blair.doc)<br>
<br>
$ dd if=blair.doc bs=512 skip=1 count=2 | dd bs=1 skip=850 count=8 | \<br>
python3.1 datedecoder.py -f -m binary -<br>
2+0 records in<br>
[... output truncated ...]<br>
2003-02-03 11:18:31.234000<br>
<br>
<br>
6) Decoding the same timestamp, but with output copy/pasted from a hex editor<br>
(text instead of binary)<br>
<br>
$ dd if=blair.doc bs=512 skip=1 count=2 | dd bs=1 skip=850 count=8 | \<br>
xxd -g 1 -u<br>
2+0 records in<br>
[... output truncated ...]<br>
0000000: 20 52 96 FB 75 CB C2 01                           R..u...<br>
<br>
$ python3.1 datedecoder.py -e little -f 20 52 96 FB 75 CB C2 01<br>
2003-02-03 11:18:31.234000<br>
<br>
</pre>

## info2ls.py ##
From demo/README.info2ls.txt

<pre>
Lists information from INFO2 (recycle bin) files.<br>
<br>
<br>
Usage:<br>
------<br>
<br>
$ python3.1 info2.py -h<br>
Usage: info2ls.py [options] info2file<br>
<br>
Lists the entries in an INFO2 file.  If info2file is '-', then stdin is read.<br>
<br>
Options:<br>
--version   show program's version number and exit<br>
-h, --help  show this help message and exit<br>
-R          Display details in Rifiuti-style format<br>
-l          Display details in long format<br>
-m          Display details in mactime format<br>
<br>
<br>
Examples:<br>
---------<br>
<br>
1) List the entries in the INFO2 file under unittests/data/INFO2/INFO2_1.bin<br>
<br>
$ python3.1 info2ls.py INFO2<br>
r/r * 3 C:\Documents and Settings\lftest1\Desktop\file2.bmp<br>
r/r * 4 C:\Documents and Settings\lftest1\Desktop\folder3.lnk<br>
r/r 5 C:\Documents and Settings\lftest1\Desktop\file1.txt<br>
r/r 6 C:\Documents and Settings\lftest1\Desktop\file2.bmp<br>
v/v 7 $HEADER<br>
<br>
<br>
2) List the entries in the INFO2 file in rifiuti-style output.<br>
(INFO2 from CFReDS hacking case http://www.cfreds.nist.gov/Hacking_Case.html)<br>
<br>
$ python3.1 info2ls.py -R INFO2<br>
INDEX  Deleted time         Drive number  Size        Deleted  Original name<br>
1      2004-08-25 16:18:25  2             2160128     No       C:\Documents and<br>
2      2004-08-27 15:12:30  2             1325056     No       C:\Documents and<br>
[... output truncated ...]<br>
<br>
<br>
3) Listing entries from the same INFO2 file in mactime format, using icat<br>
instead to send the file to stdout, and read from stdin.  Use mactime to<br>
generate a timeline based on the deleted timestamps (shown as metadata change<br>
time).<br>
<br>
$ icat -o 63 CFReDS/SCHARDT.00* 11850 | python3.1 info2ls.py -m - > bodyfile<br>
$ mactime -b bodyfile<br>
Wed Aug 25 2004 09:18:25  2160128 ..c. 1 C:\Documents and Settings\Mr. Evil\...<br>
Fri Aug 27 2004 08:12:30  1325056 ..c. 2 C:\Documents and Settings\Mr. Evil\...<br>
Fri Aug 27 2004 08:15:26   442880 ..c. 3 C:\Documents and Settings\Mr. Evil\...<br>
Fri Aug 27 2004 08:29:58  8460800 ..c. 4 C:\Documents and Settings\Mr. Evil\...<br>
[... output truncated ...]<br>
</pre>

## info2stat.py ##
From demo/README.info2stat.txt
<pre>
Prints information about a specific entry in an INFO2 file.<br>
<br>
<br>
Usage:<br>
------<br>
<br>
$ python3.1 info2stat.py -h<br>
y -h<br>
Usage: info2stat.py info2file index<br>
<br>
Displays statistics about a specific entry in an INFO2 file. If info2file is<br>
'-', then stdin is read.<br>
<br>
Options:<br>
--version   show program's version number and exit<br>
-h, --help  show this help message and exit<br>
<br>
<br>
<br>
Examples:<br>
---------<br>
<br>
1) Print statistics about the entry with index 3 in an INFO2 ifle.<br>
(INFO2 from CFReDS hacking case http://www.cfreds.nist.gov/Hacking_Case.html)<br>
<br>
$ python3.1 info2stat.py INFO2 3<br>
Deleted name: Dc3.exe<br>
Index: 3<br>
Drive number: 2 (C:)<br>
ASCII name: C:\\Documents and Settings\\Mr. Evil\\Desktop\\WinPcap_3_01_a.exe<br>
Unicode name: C:\Documents and Settings\Mr. Evil\Desktop\WinPcap_3_01_a.exe<br>
File size: 442880 bytes<br>
Deleted time: 2004-08-27 15:15:26<br>
Exists on disk: Yes<br>
<br>
<br>
2) Print statistics about the header (index 5) of the same INFO2 file.<br>
<br>
$ icat -o 63 CFReDS/SCHARDT.00* 11850 | python3.1 info2stat.py - 5<br>
Version: 5<br>
Item size: 800<br>
</pre>


## olels.py ##
From demo/README.olels.txt

<pre>
Lists entries in an OLE compound file.<br>
<br>
<br>
Usage:<br>
------<br>
<br>
$ python3.1 olels.py -h<br>
Usage: olels.py [options] olefile [dir. entry #]<br>
<br>
Lists entries in an OLE compound file.  If file is '-', then stdin is read. If<br>
a directory entry number is not specified, root is assumed.<br>
<br>
Options:<br>
--version   show program's version number and exit<br>
-h, --help  show this help message and exit<br>
-D          Display only directories (storages)<br>
-F          Display only files (streams)<br>
-l          Display details in long format<br>
-m PATH     Display details in mactime format (prefixed by PATH)<br>
-p          Display full path when recursing<br>
-r          Recurse into sub-directories<br>
<br>
<br>
Examples:<br>
---------<br>
<br>
(sample.doc is found under the unittests/data/doc directory)<br>
<br>
1) List the streams at the root directory (storage)<br>
<br>
$ python3.1 olels.py sample.doc<br>
r/r 2 WordDocument<br>
d/d 16 Macros<br>
r/r 1 Data<br>
r/r 38 1Table<br>
d/d 3 ObjectPool<br>
r/r 45 \x01CompObj<br>
d/d 41 MsoDataStore<br>
r/r 39 \x05SummaryInformation<br>
r/r 40 \x05DocumentSummaryInformation<br>
v/v 48 $Header<br>
v/v 49 $DIFAT<br>
v/v 50 $FAT<br>
v/v 51 $MiniFAT<br>
<br>
(Note: the last 4 entries are virtual and don't actually exist in the file.)<br>
<br>
<br>
2) Recursively list the streams<br>
<br>
$ cat sample.doc | python3.1 olels.py -r -<br>
r/r 2 WordDocument<br>
d/d 16 Macros<br>
r/r 31 +PROJECT<br>
d/d 17 +VBA<br>
r/r 21 ++__SRP_2<br>
r/r 19 ++__SRP_0<br>
r/r 18 ++dir<br>
r/r 20 ++__SRP_1<br>
[... output truncated ...]<br>
<br>
<br>
3) Recursively list the streams, showing the full path<br>
<br>
$ python3.1 olels.py -r -p sample.doc<br>
r/r 2 WordDocument<br>
d/d 16 Macros<br>
r/r 31 Macros/PROJECT<br>
d/d 17 Macros/VBA<br>
r/r 21 Macros/VBA/__SRP_2<br>
r/r 19 Macros/VBA/__SRP_0<br>
r/r 18 Macros/VBA/dir<br>
r/r 20 Macros/VBA/__SRP_1<br>
[... output truncated ...]<br>
<br>
<br>
4) List the entries under the ObjectPool directory (storage)<br>
<br>
$ python3.1 olels.py sample.doc 3<br>
d/d 4 _1326562448<br>
d/d 11 _1326567708<br>
<br>
<br>
5) Recursively list the entries under the ObjectPool directory (storage)<br>
showing the full path<br>
<br>
$ python3.1 olels.py -rp sample.doc 3<br>
d/d 4 _1326562448<br>
r/r 6 _1326562448/\x01CompObj<br>
r/r 5 _1326562448/\x01Ole<br>
r/r 8 _1326562448/Workbook<br>
r/r 7 _1326562448/\x03ObjInfo<br>
r/r 9 _1326562448/\x05SummaryInformation<br>
r/r 10 _1326562448/\x05DocumentSummaryInformation<br>
d/d 11 _1326567708<br>
r/r 13 _1326567708/\x03ObjInfo<br>
r/r 12 _1326567708/\x01Ole<br>
r/r 14 _1326567708/\x03LinkInfo<br>
r/r 15 _1326567708/\x02OlePres000<br>
<br>
<br>
6) Recursively list (showing full path) just the files (streams)<br>
<br>
$ python3.1 olels.py -rpF sample.doc<br>
r/r 2 WordDocument<br>
r/r 31 Macros/PROJECT<br>
r/r 21 Macros/VBA/__SRP_2<br>
r/r 19 Macros/VBA/__SRP_0<br>
r/r 18 Macros/VBA/dir<br>
r/r 20 Macros/VBA/__SRP_1<br>
r/r 25 Macros/VBA/__SRP_6<br>
[... output truncated ...]<br>
<br>
<br>
7) Generate mactime output for all entries, saving the output to bodyfile.<br>
Then run mactime against bodyfile to generate a timeline<br>
<br>
$ python3.1 olels.py -rm "c:\\sample.doc" sample.doc > bodyfile<br>
$ mactime -b bodyfile<br>
Wed Dec 31 1969 16:00:00 20288 .acb d/d 0  c:\sample.doc/Root Entry<br>
0 .ac. d/d 11 c:\sample.doc/ObjectPool/_1326567708<br>
0 .ac. d/d 16 c:\sample.doc/Macros<br>
0 .ac. d/d 17 c:\sample.doc/Macros/VBA<br>
0 .ac. d/d 3  c:\sample.doc/ObjectPool<br>
0 .ac. d/d 33 c:\sample.doc/Macros/UserForm1<br>
0 .ac. d/d 4  c:\sample.doc/ObjectPool/_1326562448<br>
0 .ac. d/d 41 c:\sample.doc/MsoDataStore<br>
[... output truncated ...]<br>
<br>
(Note: Some of the columns and spacing have been removed for display purposes)<br>
</pre>


## olestat.py ##
From demo/README.olestat.txt

<pre>
Displays statistics about a directory entry in an OLE compound file.<br>
<br>
<br>
Usage:<br>
------<br>
<br>
$ python3.1 olestat.py -h<br>
Usage: olestat.py olefile sid<br>
<br>
Displays statistics about entries in an OLE compound file.  If file is '-'<br>
then stdin is read.<br>
<br>
Options:<br>
--version   show program's version number and exit<br>
-h, --help  show this help message and exit<br>
<br>
<br>
Examples:<br>
---------<br>
<br>
(sample.doc is found under the unittests/data/doc directory)<br>
<br>
1) Display statistics on the root entry<br>
<br>
$ python3.1 olestat.py sample.doc 0<br>
Stream id: 0<br>
Name size: 22<br>
Name: Root Entry<br>
Type: STGTY_ROOT (0x5)<br>
Color: Black (0x1)<br>
Left stream id: STREAM_ID_NONE (0xFFFFFFFF)<br>
Right stream id: STREAM_ID_NONE (0xFFFFFFFF)<br>
Child stream id: 2<br>
CLSID: 00020906-0000-0000-c000-000000000046<br>
State: 0x0<br>
Size: 20288<br>
<br>
Timestamps:<br>
Stream creation time: 1601-01-01 00:00:00<br>
Stream modification time: 2010-02-02 06:46:38.627000<br>
<br>
Normal sector(s):<br>
13366, 13393, 16879, 16880, 16881, 16882, 16883, 16908<br>
16909, 16910, 16911, 16912, 16913, 16915, 16916, 16918<br>
16920, 16921, 16922, 16924, 16925, 16926, 16927, 16928<br>
16929, 16930, 16931, 16932, 16933, 16934, 16935, 16936<br>
16939, 17244, 17245, 17246, 17247, 17248, 17249, 17251<br>
<br>
<br>
2) Display statistics about stream 40<br>
<br>
$ python3.1 olestat.py sample.doc 40<br>
Stream id: 40<br>
Name size: 56<br>
Name: \x05DocumentSummaryInformation<br>
Type: STGTY_STREAM (0x2)<br>
Color: Red (0x0)<br>
Left stream id: STREAM_ID_NONE (0xFFFFFFFF)<br>
Right stream id: STREAM_ID_NONE (0xFFFFFFFF)<br>
Child stream id: STREAM_ID_NONE (0xFFFFFFFF)<br>
CLSID: 00000000-0000-0000-0000-000000000000<br>
State: 0x0<br>
Size: 2572<br>
<br>
Timestamps:<br>
Stream creation time: 1601-01-01 00:00:00<br>
Stream modification time: 1601-01-01 00:00:00<br>
<br>
Mini stream sector(s):<br>
264, 265, 266, 267, 268, 269, 270, 271<br>
272, 273, 274, 275, 276, 277, 278, 279<br>
280, 281, 282, 283, 284, 285, 286, 287<br>
288, 289, 290, 291, 292, 293, 294, 295<br>
296, 297, 298, 299, 300, 301, 302, 303<br>
304<br>
<br>
<br>
2) Display statistics about the OLE compound file header<br>
<br>
$ cat sample.doc | python3.1 olestat.py - 48<br>
Signature: b'\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1'<br>
CLSID: 00000000-0000-0000-0000-000000000000<br>
Major version: 3<br>
Minor version: 62<br>
Transaction signature #: 0<br>
Byte order: 0xFFFE<br>
Sector size: 512 bytes<br>
Mini sector size: 64 bytes<br>
Mini stream cutoff: 4096 bytes<br>
Number of dir. sectors: 0<br>
Dir. sector offset: 13363<br>
Reserved value: b'\x00\x00\x00\x00\x00\x00'<br>
<br>
FATs:<br>
DI FAT sector offset: 13911<br>
Number of DI FAT sectors: 1<br>
Number of FAT sectors: 135<br>
Mini FAT sector offset: 13365<br>
Number of Mini FAT sectors: 3<br>
<br>
<br>
3) Display statistics about the double indirect FAT (DI FAT)<br>
<br>
$ python3.1 olestat.py sample.doc 49<br>
Double Indirect FAT:<br>
<br>
0: 13258<br>
1: 13259<br>
2: 13260<br>
3: 13261<br>
4: 13262<br>
5: 13263<br>
[... output truncated ...]<br>
<br>
<br>
4) Display statistics about the FAT<br>
<br>
$ python3.1 olestat.py sample.doc 50<br>
FAT:<br>
<br>
0-20 (21) -> EOC<br>
21-13257 (13237) -> 13395<br>
13258: 0xFFFFFFFD (FAT sector)<br>
13259: 0xFFFFFFFD (FAT sector)<br>
13260: 0xFFFFFFFD (FAT sector)<br>
13261: 0xFFFFFFFD (FAT sector)<br>
13262: 0xFFFFFFFD (FAT sector)<br>
[... output truncated ...]<br>
<br>
<br>
5) Displays statistics about the mini FAT<br>
<br>
$ python3.1 olestat.py sample.doc 51<br>
Mini FAT:<br>
<br>
0-0 (1) -> EOC<br>
1-2 (2) -> EOC<br>
3-3 (1) -> EOC<br>
4-7 (4) -> EOC<br>
8-11 (4) -> EOC<br>
[... output truncated ...]<br>
</pre>


## olecat.py ##
From demo/README.olecat.txt

<pre>
Displays the contents of an OLE stream to standard out.<br>
<br>
<br>
Usage:<br>
------<br>
<br>
$ python3.1 olecat.py -h<br>
Usage: olecat.py [options] olefile sid<br>
<br>
Displays the contents of an OLE stream to standard out. If file is '-', then<br>
stdin is read.<br>
<br>
Options:<br>
--version   show program's version number and exit<br>
-h, --help  show this help message and exit<br>
-s          Include slack space<br>
<br>
<br>
Examples:<br>
---------<br>
<br>
(blair.doc from http://www.computerbytesman.com/privacy/blair.doc)<br>
<br>
1) Extract the contents of stream 2<br>
<br>
$ python3.1 olecat.py -i 2 blair.doc > blair.doc.2<br>
<br>
<br>
2) Extract the contents of stream 2, including slack<br>
<br>
$ cat blair.doc | python3.1 olecat.py  -s - 2 > blair.doc.2.slack<br>
</pre>


## oleps.py ##
From demo/README.oleps.txt

<pre>
Displays OLE property sets from a stream in an OLE compound file.<br>
<br>
<br>
Usage:<br>
------<br>
<br>
$ python3.1 oleps.py -h<br>
Usage: oleps.py [options] -i sid olefile<br>
<br>
Displays OLE property sets from a stream in an OLE compound file.  If file is<br>
'-' then stdin is read.<br>
<br>
Options:<br>
--version   show program's version number and exit<br>
-h, --help  show this help message and exit<br>
-r          Input is just a stream (not an OLE compound file)<br>
-i SID      Stream to analyze<br>
<br>
<br>
Examples:<br>
---------<br>
<br>
(sample.doc is found under the unittests/data/doc directory)<br>
<br>
1) Extract the property set(s) from the SummaryInformation stream.<br>
<br>
$ python3.1 oleps.py -i 39 sample.doc<br>
Property Set Stream Header<br>
--------------------------<br>
Byte order: 0xFFFE<br>
Version: 0<br>
Sys. id: b'\x05\x01\x02\x00'<br>
CLSID: 00000000-0000-0000-0000-000000000000<br>
Number of property sets: 1<br>
Property set 0 FMTID: f29f85e0-4ff9-1068-ab91-08002b27b3d9<br>
Property set 0 offset: 48<br>
<br>
Property Set 0<br>
--------------<br>
Header size: 153200 bytes<br>
Number of pid/offset pairs: 18<br>
<br>
Property: 1<br>
Type: VT_I2 (0x2)<br>
Offset: 200<br>
Size: 8 bytes<br>
Name: <not found><br>
Value: 1252<br>
[... output truncated ...]<br>
<br>
<br>
2) Use olecat.py to extract the DocumentSummaryInformation stream and then<br>
extract the property set(s).<br>
<br>
$ python3.1 olecat.py sample.doc 40 | python3.1 oleps.py -r -<br>
Property Set Stream Header<br>
--------------------------<br>
Byte order: 0xFFFE<br>
Version: 0<br>
Sys. id: b'\x05\x01\x02\x00'<br>
CLSID: 00000000-0000-0000-0000-000000000000<br>
Number of property sets: 2<br>
Property set 0 FMTID: d5cdd502-2e9c-101b-9397-08002b2cf9ae<br>
Property set 0 offset: 68<br>
Property set 1 FMTID: d5cdd505-2e9c-101b-9397-08002b2cf9ae<br>
Property set 1 offset: 504<br>
<br>
Property Set 0<br>
--------------<br>
Header size: 436 bytes<br>
Number of pid/offset pairs: 15<br>
<br>
Property: 1<br>
Type: VT_I2 (0x2)<br>
Offset: 196<br>
Size: 8 bytes<br>
Name: <not found><br>
Value: 1252<br>
[... output truncated ...]<br>
</pre>


## tdbls.py ##
From demo/README.tdbls.txt

<pre>
Lists information from thumbs.db files.<br>
<br>
<br>
Usage:<br>
------<br>
<br>
$ python3.1 tdbls.py -h<br>
Usage: tdbls.py [options] thumbsdb<br>
<br>
Lists the entries in an thumbs.db file.  If thumbsdb is '-', then stdin is<br>
read.<br>
<br>
Options:<br>
--version        show program's version number and exit<br>
-h, --help       show this help message and exit<br>
-p               Display details in 'pretty-print' format<br>
-l               Display details in long format<br>
-m               Display details in mactime format<br>
-c CATALOG_NAME  The name of the catalog stream (def: Catalog)<br>
<br>
<br>
<br>
Examples:<br>
---------<br>
<br>
1) List the entries in the thumbs.db file under unittests/data/thumbsdb.<br>
<br>
$ python3.1 tdbls.py thumbs.db<br>
r/r 1: zoolemur1.jpg<br>
r/r 2: Copy (2) of danger-sign-shock.jpg<br>
r/r 3: Copy (2) of Kookaburra_at_Marwell.jpg<br>
r/r 4: Copy (2) of Makari_the_Tiger.jpg<br>
r/r 5: Copy (2) of prairiedogs.jpg<br>
r/r 6: Copy (2) of zoolemur1.jpg<br>
r/r 7: Copy of danger-sign-shock.jpg<br>
r/r 8: Copy of Kookaburra_at_Marwell.jpg<br>
r/r 9: Copy of Makari_the_Tiger.jpg<br>
r/r 10: Copy of prairiedogs.jpg<br>
r/r 11: Copy of zoolemur1.jpg<br>
r/r 12: danger-sign-shock.jpg<br>
r/r 13: Kookaburra_at_Marwell.jpg<br>
r/r 14: Makari_the_Tiger.jpg<br>
r/r 15: prairiedogs.jpg<br>
v/v 16: $Catalog<br>
<br>
<br>
2) List the entries in the same thumbs.db file, with long output.<br>
<br>
$ python3.1 tdbls.py -l thumbs.db<br>
r/r 1:  zoolemur1.jpg   2010-02-02 03:25:06 3039<br>
r/r 2:  Copy (2) of danger-sign-shock.jpg   2010-02-02 03:25:04 4098<br>
r/r 3:  Copy (2) of Kookaburra_at_Marwell.jpg   2010-02-02 03:25:02 2878<br>
r/r 4:  Copy (2) of Makari_the_Tiger.jpg    2010-02-02 03:25:04 5238<br>
r/r 5:  Copy (2) of prairiedogs.jpg 2010-02-02 03:25:06 2963<br>
r/r 6:  Copy (2) of zoolemur1.jpg   2010-02-02 03:25:06 3039<br>
r/r 7:  Copy of danger-sign-shock.jpg   2010-02-02 03:25:04 4098<br>
r/r 8:  Copy of Kookaburra_at_Marwell.jpg   2010-02-02 03:25:02 2878<br>
r/r 9:  Copy of Makari_the_Tiger.jpg    2010-02-02 03:25:04 5238<br>
r/r 10: Copy of prairiedogs.jpg 2010-02-02 03:25:06 2963<br>
r/r 11: Copy of zoolemur1.jpg   2010-02-02 03:25:06 3039<br>
r/r 12: danger-sign-shock.jpg   2010-02-02 03:25:04 4098<br>
r/r 13: Kookaburra_at_Marwell.jpg   2010-02-02 03:25:02 2878<br>
r/r 14: Makari_the_Tiger.jpg    2010-02-02 03:25:04 5238<br>
r/r 15: prairiedogs.jpg 2010-02-02 03:25:06 2963<br>
v/v 16: $Catalog    0   0<br>
<br>
<br>
3) List the entries in the same thumbs.db file, with pretty-print output.<br>
<br>
$ python3.1 tdbls.py -p thumbs.db<br>
ID  Modified time        Size    File name<br>
1   2010-02-02 03:25:06  3039    zoolemur1.jpg<br>
2   2010-02-02 03:25:04  4098    Copy (2) of danger-sign-shock.jpg<br>
3   2010-02-02 03:25:02  2878    Copy (2) of Kookaburra_at_Marwell.jpg<br>
4   2010-02-02 03:25:04  5238    Copy (2) of Makari_the_Tiger.jpg<br>
5   2010-02-02 03:25:06  2963    Copy (2) of prairiedogs.jpg<br>
6   2010-02-02 03:25:06  3039    Copy (2) of zoolemur1.jpg<br>
7   2010-02-02 03:25:04  4098    Copy of danger-sign-shock.jpg<br>
8   2010-02-02 03:25:02  2878    Copy of Kookaburra_at_Marwell.jpg<br>
9   2010-02-02 03:25:04  5238    Copy of Makari_the_Tiger.jpg<br>
10  2010-02-02 03:25:06  2963    Copy of prairiedogs.jpg<br>
11  2010-02-02 03:25:06  3039    Copy of zoolemur1.jpg<br>
12  2010-02-02 03:25:04  4098    danger-sign-shock.jpg<br>
13  2010-02-02 03:25:02  2878    Kookaburra_at_Marwell.jpg<br>
14  2010-02-02 03:25:04  5238    Makari_the_Tiger.jpg<br>
15  2010-02-02 03:25:06  2963    prairiedogs.jpg<br>
<br>
<br>
4) List the entries in the same thumbs.db file (read from stdin) in mactime<br>
format.  Use mactime to generate a timeline.<br>
<br>
$ cat tdbls.py | python3.1 - -m thumbs.db > bodyfile<br>
$ mactime -b bodyfile<br>
Mon Feb 01 2010 19:25:02     2878 m... 13 Kookaburra_at_Marwell.jpg<br>
2878 m... 3  Copy (2) of Kookaburra_at_Marwell.jpg<br>
2878 m... 8  Copy of Kookaburra_at_Marwell.jpg<br>
Mon Feb 01 2010 19:25:04     4098 m... 12 danger-sign-shock.jpg<br>
5238 m... 14 Makari_the_Tiger.jpg<br>
[... output truncated ...]<br>
</pre>


## tdbstat.py ##
From demo/README.tdbstat.txt

<pre>
Prints information about a specific entry in a thumbs.db file.<br>
<br>
<br>
Usage:<br>
------<br>
<br>
$ python3.1 tdbstat.py -h<br>
Usage: tdbstat.py thumbsdb id<br>
<br>
Displays statistics about a specific entry in a thumbs.db file. If thumbsdb is<br>
'-', then stdin is read.<br>
<br>
Options:<br>
--version        show program's version number and exit<br>
-h, --help       show this help message and exit<br>
-c CATALOG_NAME  The name of the catalog stream (def: Catalog)<br>
<br>
<br>
<br>
Examples:<br>
---------<br>
<br>
1) Print statistics about the entry with id 4 in thumbs.db.<br>
(thumbs.db from unittests/data/thumbsdb)<br>
<br>
$ python3.1 tdbstat.py thumbs.db 4<br>
ID: 4<br>
Catalog entry size: 84<br>
File name: Copy (2) of Makari_the_Tiger.jpg<br>
File size: 5238<br>
Stream name: 4<br>
Modification time: 2010-02-02 03:25:04<br>
<br>
<br>
2) Print statistics about the catalog from the same thumbs.db file<br>
<br>
$ cat thumbs.db | python3.1 tdbstat.py - 16<br>
Thumbnail width: 96<br>
Thumbnail height: 96<br>
Thumbnail count: 15<br>
</pre>


## tdbcat.py ##
From demo/README.tdbcat.txt

<pre>
Extracts a thumbnail from a thumbs.db file<br>
<br>
<br>
Usage:<br>
------<br>
<br>
$ python3.1 tdbcat.py -h<br>
Usage: tdbcat.py [options] thumbsdb id<br>
<br>
Extracts raw thumbnail data from a thumbs.db file. If thumbsdb is '-', then<br>
stdin is read.<br>
<br>
Options:<br>
--version        show program's version number and exit<br>
-h, --help       show this help message and exit<br>
-c CATALOG_NAME  The name of the catalog stream (def: Catalog)<br>
<br>
<br>
Examples:<br>
---------<br>
<br>
1) Extract the image with id 4.<br>
(thumbs.db from unittests/data/thumbsdb)<br>
<br>
$ python3.1 tdbcat.py thumbs.db 4 > thumb.jpg<br>
<br>
<br>
2) Extract the thumbnail with id 4 from the same thumbs.db file.  Send the<br>
output to imagemagic to identify image metadata.<br>
<br>
$ cat thumbs.db | python3.1 tdbcat.py - 4 | identify -verbose -<br>
Image: /tmp/magick-XXZPK0Vw<br>
Base filename: -<br>
Format: JPEG (Joint Photographic Experts Group JFIF format)<br>
Class: DirectClass<br>
Geometry: 96x96+0+0<br>
Resolution: 96x96<br>
Print size: 1x1<br>
Units: PixelsPerInch<br>
Type: TrueColor<br>
Endianess: Undefined<br>
Colorspace: RGB<br>
Depth: 8-bit<br>
[... output truncated ...]<br>
</pre>

## wmg.py ##
From demo/README.wmg.txt

<pre>
Grabs metadata from Microsoft Word (.doc) files.<br>
<br>
$ python3.1 wmg.py -h<br>
Usage: wmg.py <word file><br>
<br>
Options:<br>
-h, --help  show this help message and exit<br>
<br>
Note: If you don't specify a word file, stdin is used.  Output is written to<br>
stdout.<br>
<br>
Examples:<br>
<br>
1) Dump metadata on blair.doc<br>
(blair.doc from http://www.computerbytesman.com/privacy/blair.doc)<br>
<br>
$ python3.1 wmg.py blair.doc<br>
Compound File Information<br>
-------------------------<br>
File: blair.doc<br>
Root directory creation time: Mon Feb  3 11:08:06 2003 UTC<br>
Root directory modification time: Mon Feb  3 11:18:31 2003 UTC<br>
<br>
Summary Information<br>
-------------------<br>
Title: Iraq- ITS INFRASTRUCTURE OF CONCEALMENT, DECEPTION AND INTIMIDATION<br>
Subject:<br>
Author: default<br>
Code page: 1252<br>
Keywords:<br>
Comments:<br>
Template used: Normal.dot<br>
Last author: MKhan<br>
Revision: 4<br>
Creator: Microsoft Word 8.0<br>
Last printed: Thu Jan 30 21:33:00 2003<br>
Creation time: Mon Feb  3 09:31:00 2003<br>
Last saved: Mon Feb  3 11:18:00 2003<br>
Total edit time: 0 days, 0 hours, 3 mins, 0 secs<br>
<br>
Document Summary Information<br>
----------------------------<br>
Category: (not in file)<br>
Presentation format: (not in file)<br>
Slide count: (not in file)<br>
Manager: (not in file)<br>
Company: default<br>
Major version: 8<br>
Minor version: 49<br>
Content type: (not in file)<br>
Content status: (not in file)<br>
Language: (not in file)<br>
Document version: (not in file)<br>
<br>
User Defined Properties<br>
-----------------------<br>
Code page: 1252<br>
_PID_GUID: {5E2C2E6C-8A16-46F3-8843-7F739FA12901}<br>
<br>
Word Information<br>
----------------<br>
Magic: Word 8.0 (0xA5EC)<br>
Version: 0xC1<br>
Language: United States English<br>
Encryption key: 0<br>
Created in: Windows<br>
Created by: Word 97 (Build date: Fri Aug 21 1998)<br>
Last revised by: Word 97 (Build date: Fri Aug 21 1998)<br>
<br>
Miscellaneous Properties<br>
------------------------<br>
Is a template: no<br>
Is a glossary: no<br>
Is in complex format: no<br>
Has pictures: no<br>
Is encrypted: no<br>
Is Far East encoded: no<br>
Last saved on a Mac: no<br>
<br>
Last Authors / Locations<br>
------------------------<br>
10: MKhan: C:\WINNT\Profiles\mkhan\Desktop\Iraq.doc<br>
9: MKhan: C:\TEMP\Iraq - security.doc<br>
8: ablackshaw: A:\Iraq - security.doc<br>
7: ablackshaw: C:\ABlackshaw\A;Iraq - security.doc<br>
6: ablackshaw: C:\ABlackshaw\Iraq - security.doc<br>
5: JPratt: A:\Iraq - security.doc<br>
4: JPratt: C:\TEMP\Iraq - security.doc<br>
3: cic22: C:\DOCUME~1\phamill\LOCALS~1\Temp\AutoRecovery save of Iraq - security.asd<br>
2: cic22: C:\DOCUME~1\phamill\LOCALS~1\Temp\AutoRecovery save of Iraq - security.asd<br>
1: cic22: C:\DOCUME~1\phamill\LOCALS~1\Temp\AutoRecovery save of Iraq - security.asd<br>
<br>
Associated Strings<br>
------------------<br>
Template used:<br>
Title: Iraq- ITS INFRASTRUCTURE OF CONCEALMENT, DECEPTION AND INTIMIDATION<br>
Subject:<br>
Keywords:<br>
Comments:<br>
Author: default<br>
Last revised by: MKhan<br>
<br>
Users / Roles<br>
-------------<br>
No users / roles in document<br>
<br>
<br>
2) Dump metadata from _IMMYJ~1.DOC<br>
(image from SOTM24 http://old.honeynet.org/scans/scan24/)<br>
<br>
$ icat -r image 5 | python3.1 wmg.py<br>
Compound File Information<br>
-------------------------<br>
File: --stdin--<br>
Root directory creation time: Mon Jan  1 00:00:00 1601 UTC<br>
Root directory modification time: Mon Apr 15 21:42:29 2002 UTC<br>
<br>
Summary Information<br>
-------------------<br>
Title: Jimmy Jungle<br>
Subject:<br>
Author: 0000<br>
Code page: 1252<br>
Keywords:<br>
Comments:<br>
Template used: Normal<br>
Last author: 0000t<br>
Revision: 9<br>
Creator: Microsoft Word 10.0<br>
Last printed: (not in file)<br>
Creation time: Mon Apr 15 20:30:00 2002<br>
Last saved: Mon Apr 15 21:42:00 2002<br>
Total edit time: 0 days, 0 hours, 18 mins, 0 secs<br>
<br>
Document Summary Information<br>
----------------------------<br>
Category: (not in file)<br>
Presentation format: (not in file)<br>
Slide count: (not in file)<br>
Manager: (not in file)<br>
Company: OOOO<br>
Major version: 10<br>
Minor version: 65<br>
Content type: (not in file)<br>
Content status: (not in file)<br>
Language: (not in file)<br>
Document version: (not in file)<br>
<br>
User Defined Properties<br>
-----------------------<br>
(not in file)<br>
<br>
Word Information<br>
----------------<br>
Magic: Word 8.0 (0xA5EC)<br>
Version: 0xC1<br>
Language: United States English<br>
Encryption key: 0<br>
Created in: Windows<br>
Created by: Word 97 (Build date: Wed Feb 27 1901)<br>
Last revised by: Word 97 (Build date: Wed Feb 27 1901)<br>
<br>
Miscellaneous Properties<br>
------------------------<br>
Is a template: no<br>
Is a glossary: no<br>
Is in complex format: no<br>
Has pictures: no<br>
Is encrypted: no<br>
Is Far East encoded: no<br>
Last saved on a Mac: no<br>
<br>
Last Authors / Locations<br>
------------------------<br>
1: CSTC:<br>
<br>
Associated Strings<br>
------------------<br>
Template used:<br>
Title: Jimmy Jungle<br>
Subject:<br>
Keywords:<br>
Comments:<br>
Author: CSTC<br>
Last revised by: CSTC<br>
<br>
Users / Roles<br>
-------------<br>
No users / roles in document<br>
</pre>

## recdump.py ##
From demo/README.recdump.txt

<pre>
Dumps information about record data types (data structures).<br>
<br>
<br>
Usage:<br>
------<br>
<br>
$ python3.1 recdump.py -h<br>
Usage: recdump.py [options] RECORD [file]<br>
<br>
Dumps information about record data types (data structures). By specifying a<br>
file (or '-' for stdin) data from the file (or stdin) is extracted and printed<br>
inline with the data structure<br>
<br>
Options:<br>
--version             show program's version number and exit<br>
-h, --help            show this help message and exit<br>
-r MAX_DEPTH          Maximum depth for recursion (-1 is unlimited)<br>
-f FILE MODNAME, --file=FILE MODNAME<br>
Load RECORD from FILE using MODNAME as the module name<br>
<br>
Formatting Options:<br>
The options are used for formatting output of numbers.  Valid values<br>
for BASE are: [b]inary, [d]ecial, [o]ctal, and he[x|X].<br>
<br>
-o BASE             The base for offsets (default: X)<br>
-d BASE             The base for data (default: X)<br>
-s BASE             The base for sizes (default: d)<br>
-i BASE             The base for indices (default: d)<br>
<br>
<br>
Examples:<br>
---------<br>
<br>
1) Display the structure of an INFO2 deleted file entry.<br>
<br>
$ python3.1 recdump.py lf.win.shell.recyclebin.dtypes.INFO2Item<br>
File: n/a<br>
Module: lf.win.shell.recyclebin.dtypes<br>
Record: INFO2Item<br>
Size of record: 800 bytes<br>
Data: n/a<br>
<br>
0000:     name_asc                   ; raw (260)<br>
0104:     id                         ; DWORD (4)<br>
0108:     drive_num                  ; DWORD (4)<br>
010C:     dtime                      ; FILETIME_LE (8)<br>
0114:     file_size                  ; DWORD (4)<br>
0118:     name_uni                   ; raw (520)<br>
<br>
<br>
2) Display the structure, and extract values for a PropertySetStreamHeader in<br>
an OLE compound file.<br>
(blair.doc from http://www.computerbytesman.com/privacy/blair.doc)<br>
<br>
$ python3.1 olecat.py blair.doc 3 | python3.1 recdump.py -r 2 \<br>
lf.win.ole.ps.dtypes.PropertySetStreamHeader -<br>
File: n/a<br>
Module: lf.win.ole.ps.dtypes<br>
Record: PropertySetStreamHeader<br>
Size of record: 48 bytes<br>
Data: 4096 bytes from --stdin--<br>
<br>
0000:     byte_order                 ; WORD (2), data = 0xFFFE<br>
0002:     version                    ; WORD (2), data = 0x0<br>
0004:     sys_id                     ; raw (4)<br>
0008:     clsid                      ; CLSID_LE (16)<br>
0008:       + data1                  ; DWORD (4), data = 0x0<br>
000C:       + data2                  ; WORD (2), data = 0x0<br>
000E:       + data3                  ; WORD (2), data = 0x0<br>
0010:       + data4                  ; BYTE[8] (8)<br>
0010:         + data4[0]             ; BYTE (1), data = 0x0<br>
0011:         + data4[1]             ; BYTE (1), data = 0x0<br>
0012:         + data4[2]             ; BYTE (1), data = 0x0<br>
0013:         + data4[3]             ; BYTE (1), data = 0x0<br>
0014:         + data4[4]             ; BYTE (1), data = 0x0<br>
0015:         + data4[5]             ; BYTE (1), data = 0x0<br>
0016:         + data4[6]             ; BYTE (1), data = 0x0<br>
0017:         + data4[7]             ; BYTE (1), data = 0x0<br>
0018:     property_set_count         ; DWORD (4), data = 0x1<br>
001C:     fmtid0                     ; FMTID (16)<br>
001C:       + data1                  ; DWORD (4), data = 0xF29F85E0<br>
0020:       + data2                  ; WORD (2), data = 0x4FF9<br>
0022:       + data3                  ; WORD (2), data = 0x1068<br>
0024:       + data4                  ; BYTE[8] (8)<br>
0024:         + data4[0]             ; BYTE (1), data = 0xAB<br>
0025:         + data4[1]             ; BYTE (1), data = 0x91<br>
0026:         + data4[2]             ; BYTE (1), data = 0x8<br>
0027:         + data4[3]             ; BYTE (1), data = 0x0<br>
0028:         + data4[4]             ; BYTE (1), data = 0x2B<br>
0029:         + data4[5]             ; BYTE (1), data = 0x27<br>
002A:         + data4[6]             ; BYTE (1), data = 0xB3<br>
002B:         + data4[7]             ; BYTE (1), data = 0xD9<br>
002C:     offset0                    ; DWORD (4), data = 0x30<br>
<br>
<br>
3) Display and extract values for an HRESULT data type (little endian)<br>
<br>
$ echo -ne "\x64\x53\x64\x53" | python3.1 recdump.py lf.win.dtypes.HRESULT_LE -<br>
File: n/a<br>
Module: lf.win.dtypes<br>
Record: HRESULT_LE<br>
Size of record: 4 bytes<br>
Data: 4 bytes from --stdin--<br>
<br>
0000:00:  code                       ; bits (16), data = 0x5364<br>
0002:00:  facility                   ; bits (11), data = 0x364<br>
0003:03:  x                          ; bit (1), data = 0x0<br>
0003:04:  n                          ; bit (1), data = 0x1<br>
0003:05:  c                          ; bit (1), data = 0x0<br>
0003:06:  r                          ; bit (1), data = 0x1<br>
0003:07:  s                          ; bit (1), data = 0x0<br>
</pre>

## lnkinfo.py ##
From demo/README.lnkinfo.txt
<pre>
Displays information about shell link (.lnk) files<br>
<br>
<br>
Usage:<br>
------<br>
<br>
$ python3.1 lnkinfo.py -h<br>
Usage: lnkinfo.py [options] lnkfile<br>
<br>
Displays information from shell link (.lnk) files.  If file is '-' then stdin<br>
is read.<br>
<br>
Options:<br>
--version   show program's version number and exit<br>
-h, --help  show this help message and exit<br>
-f          Display full output for binary attributes<br>
<br>
<br>
Examples:<br>
---------<br>
<br>
1) Display information from shortcut_to_local_exe.lnk (in unittests/data/lnk)<br>
<br>
$ python3.1 lnkinfo.py shortcut_to_local_exe.lnk<br>
File: shortcut_to_local_exe.lnk<br>
<br>
Shell Link Header<br>
=================<br>
Header size: 76<br>
CLSID: 00021401-0000-0000-c000-000000000046<br>
Creation time: 2010-03-17 09:58:19.239000<br>
Access time: 2010-03-17 09:58:19.239000<br>
Modification time: 2006-11-02 09:45:32.330000<br>
Target size: 15360<br>
Icon index: 18<br>
Show command: SW_SHOWMAXIMIZED (0x3)<br>
Hotkey: 7:4B (CTRL + SHIFT + ALT + K)<br>
<br>
Link Flags:<br>
-----------<br>
Has link target idlist: True<br>
Has link info: True<br>
Has name: True<br>
Has relative path: True<br>
Has working directory: True<br>
Has arguments: True<br>
Has icon location: True<br>
Is unicode: True<br>
Force no link info: False<br>
Has exp. string: True<br>
Run in separate process: False<br>
Has logo3 id: False<br>
Has darwin id: False<br>
Run as user: True<br>
Has exp. icon: False<br>
No pidl alias: False<br>
Force UNC name: False<br>
Run with shim layer: False<br>
Force no link track: False<br>
Enable target metadata: True<br>
Disable link path tracking: False<br>
Disable known folder tracking: False<br>
Disable known folder alias: False<br>
Allow link to link: False<br>
Prefer environment path: False<br>
Keep local idlist for UNC target: False<br>
<br>
File Attributes:<br>
----------------<br>
Read only: False<br>
Hidden: False<br>
System: False<br>
Directory: False<br>
Archive: True<br>
Normal: False<br>
Temp: False<br>
Sparse: False<br>
Reparse point: False<br>
Compressed: False<br>
Offline: False<br>
Not content indexed: False<br>
Encrypted: False<br>
<br>
<br>
Link Target IDList<br>
==================<br>
Byte count: 20<br>
Data: b'\x1fP\xe0O\xd0 \xea:i\x10\xa2\xd8\x08\x00+'<br>
<br>
Byte count: 25<br>
Data: b'/C:\\\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'<br>
<br>
Byte count: 78<br>
Data: b'1\x00\x00\x00\x00\x00q<JO\x10\x00Win'<br>
<br>
Byte count: 82<br>
Data: b'2\x00\x00<\x00\x00b5\xb1M \x00PIN'<br>
<br>
Byte count: 0<br>
Data: Not in file<br>
<br>
<br>
Link Info<br>
=========<br>
Size: 66<br>
Header size: 28<br>
Volume ID and local base path: True<br>
CNRL and path suffix: False<br>
Volume ID offset: 28<br>
Local base path offset: 45<br>
CNRL offset: 0<br>
Common path suffix offset: 65<br>
Local base path offset (unicode): None<br>
Common path suffix offset (unicode): None<br>
Local base path: b'C:\\Windows\\PING.EXE'<br>
Local base path (unicode): Not in file<br>
Common path suffix: Not in file<br>
Common path suffix (unicode): Not in file<br>
<br>
Volume ID:<br>
----------<br>
Size: 17<br>
Drive type: Fixed (0x3)<br>
Drive serial number: 0xA0E8D60C<br>
Volume label offset: 16<br>
Volume label offset (unicode): None<br>
Volume label: b''<br>
<br>
Common Network Relative Link:<br>
-----------------------------<br>
Not in file<br>
<br>
<br>
String Data<br>
===========<br>
<br>
Name String:<br>
------------<br>
Character count: 7<br>
String: comment<br>
<br>
Relative Path:<br>
--------------<br>
Character count: 25<br>
String: ..\..\..\Windows\PING.EXE<br>
<br>
Working Directory:<br>
------------------<br>
Character count: 15<br>
String: c:\start-in-dir<br>
<br>
Command Line Arguments:<br>
-----------------------<br>
Character count: 14<br>
String: arg1 arg2 arg3<br>
<br>
Icon Location:<br>
--------------<br>
Character count: 33<br>
String: %SystemRoot%\system32\SHELL32.dll<br>
<br>
<br>
Extra Data<br>
==========<br>
SpecialFolderDataBlock:<br>
-----------------------<br>
Size: 16<br>
Signature: SPECIAL_FOLDER_PROPS (0xA0000005)<br>
Special folder id: WINDOWS (0x24) (CSIDL_WINDOWS)<br>
Offset: 123<br>
<br>
KnownFolderDataBlock:<br>
---------------------<br>
Size: 28<br>
Signature: KNOWN_FOLDER_PROPS (0xA000000B)<br>
Known folder ID: f38bf404-1d43-42f2-9305-67de0b28fc23<br>
Offset: 123<br>
<br>
TrackerDataBlock:<br>
-----------------<br>
Size: 96<br>
Signature: TRACKER_PROPS (0xA0000003)<br>
Length: 88<br>
Version: 0<br>
Machine ID: b'lftest-vista-pc'<br>
<br>
DROID:<br>
------<br>
Volume: 1960e830-83b3-4aae-93a1-9b9319d21e50<br>
Object: 196f4ff5-31a1-11df-a968-000c29c44b38<br>
<br>
DROID Birth:<br>
------------<br>
Volume: 1960e830-83b3-4aae-93a1-9b9319d21e50<br>
Object: 196f4ff5-31a1-11df-a968-000c29c44b38<br>
<br>
ConsoleDataBlock:<br>
-----------------<br>
Size: 204<br>
Signature: CONSOLE_PROPS (0xA0000002)<br>
Screen buffer size (horizontal): 79<br>
Screen buffer size (vertical): 300<br>
Window size (horizontal): 79<br>
Window size (vertical): 23<br>
Window origin: (5, 5)<br>
Font: 0<br>
Input buffer size: 0<br>
Font size: 786448<br>
Font family: Modern (0x30)<br>
Font weight: Regular (400)<br>
Face name: Terminal<br>
Cursor size: Medium (50)<br>
Full screen: True (1)<br>
Insert mode: True (1)<br>
Auto position window: False (0)<br>
History buffer size: 47<br>
Number of history buffers: 6<br>
Remove history duplicates: False (0)<br>
<br>
Fill Attributes:<br>
----------------<br>
Blue (foreground): True<br>
Green (foreground): True<br>
Red (foreground): True<br>
Intensity (foreground): False<br>
Blue (background): False<br>
Green (background): False<br>
Red (background): False<br>
Intensity (background): False<br>
<br>
Popup Fill Attributes:<br>
----------------------<br>
Blue (foreground): True<br>
Green (foreground): False<br>
Red (foreground): True<br>
Intensity (foreground): False<br>
Blue (background): True<br>
Green (background): True<br>
Red (background): False<br>
Intensity (background): True<br>
<br>
Color Table:<br>
------------<br>
0x00000000, 0x00800000, 0x00008000, 0x00808000<br>
0x00000080, 0x00800080, 0x00008080, 0x00C0C0C0<br>
0x00808080, 0x00FF0000, 0x0000FF00, 0x00FFFF00<br>
0x000000FF, 0x00FF00FF, 0x0000FFFF, 0x00FFFFFF<br>
<br>
EnvironmentVariableDataBlock:<br>
------------------------------<br>
Size: 788<br>
Signature: ENVIRONMENT_PROPS (0xA0000001)<br>
Target ANSI: b'%windir%\\PING.EXE'<br>
Target unicode: %windir%\PING.EXE<br>
<br>
<br>
<br>
2) Display full information (all binary data) from<br>
"Temp on m1200 (4.12.220.154).lnk"<br>
(from CFReDS hacking case at http://www.cfreds.nist.gov/Hacking_Case.html)<br>
<br>
$ python3.1 lnkinfo.py -f Temp\ on\ m1200\ \(4.12.220.254\).lnk<br>
File: CFReDS-hacking/Temp on m1200 (4.12.220.254).lnk<br>
<br>
Shell Link Header<br>
=================<br>
Header size: 76<br>
CLSID: 00021401-0000-0000-c000-000000000046<br>
Creation time: 2004-08-02 06:51:49.881000<br>
Access time: 2004-08-26 15:07:06.328000<br>
Modification time: 2004-08-26 13:49:28.611000<br>
Target size: 0<br>
Icon index: 0<br>
Show command: SW_SHOWNORMAL (0x1)<br>
Hotkey: 0:0<br>
<br>
Link Flags:<br>
-----------<br>
Has link target idlist: True<br>
Has link info: True<br>
Has name: False<br>
Has relative path: False<br>
Has working directory: False<br>
Has arguments: False<br>
Has icon location: False<br>
Is unicode: True<br>
Force no link info: False<br>
Has exp. string: False<br>
Run in separate process: False<br>
Has logo3 id: False<br>
Has darwin id: False<br>
Run as user: False<br>
Has exp. icon: False<br>
No pidl alias: False<br>
Force UNC name: False<br>
Run with shim layer: False<br>
Force no link track: False<br>
Enable target metadata: False<br>
Disable link path tracking: False<br>
Disable known folder tracking: False<br>
Disable known folder alias: False<br>
Allow link to link: False<br>
Prefer environment path: False<br>
Keep local idlist for UNC target: False<br>
<br>
File Attributes:<br>
----------------<br>
Read only: False<br>
Hidden: False<br>
System: False<br>
Directory: True<br>
Archive: False<br>
Normal: False<br>
Temp: False<br>
Sparse: False<br>
Reparse point: False<br>
Compressed: False<br>
Offline: False<br>
Not content indexed: False<br>
Encrypted: False<br>
<br>
<br>
Link Target IDList<br>
==================<br>
Byte count: 20<br>
Data:<br>
b'\x1fX`,\x8d \xea:i\x10\xa2\xd7\x08\x00+00\x9d'<br>
<br>
Byte count: 20<br>
Data:<br>
b'G\x00\x02Entire Network\x00'<br>
<br>
Byte count: 51<br>
Data:<br>
b'F\x00\x82Microsoft Windows Network\x00Microsoft Network\x00\x02\x00'<br>
<br>
Byte count: 28<br>
Data:<br>
b'A\x00\x821a\x00Microsoft Network\x00\x02\x00'<br>
<br>
Byte count: 46<br>
Data:<br>
b'B\x00\xc2\\\\4.12.220.254\x00Microsoft Network\x00m1200\x00\x02\x00'<br>
<br>
Byte count: 46<br>
Data:<br>
b'\xc3\x01\xc1\\\\4.12.220.254\\Temp\x00Microsoft Network\x00\x00\x02\x00'<br>
<br>
Byte count: 0<br>
Data: Not in file<br>
<br>
<br>
Link Info<br>
=========<br>
Size: 69<br>
Header size: 28<br>
Volume ID and local base path: False<br>
CNRL and path suffix: True<br>
Volume ID offset: 0<br>
Local base path offset: 0<br>
CNRL offset: 28<br>
Common path suffix offset: 68<br>
Local base path offset (unicode): None<br>
Common path suffix offset (unicode): None<br>
Local base path: Not in file<br>
Local base path (unicode): Not in file<br>
Common path suffix: Not in file<br>
Common path suffix (unicode): Not in file<br>
<br>
Volume ID:<br>
----------<br>
Not in file<br>
<br>
Common Network Relative Link:<br>
-----------------------------<br>
Size: 40<br>
Valid device: False<br>
Valid net type: True<br>
Net name offset: 20<br>
Device name offset: 0<br>
Network provider type: WNNC_NET_LANMAN (0x20000)<br>
Net name offset (unicode): None<br>
Device name offset (unicode): None<br>
Net name: b'\\\\4.12.220.254\\TEMP'<br>
Device name: Not in file<br>
Net name (unicode): Not in file<br>
Device name (unicode): Not in file<br>
<br>
<br>
String Data<br>
===========<br>
<br>
Name String:<br>
------------<br>
Not in file<br>
<br>
Relative Path:<br>
--------------<br>
Not in file<br>
<br>
Working Directory:<br>
------------------<br>
Not in file<br>
<br>
Command Line Arguments:<br>
-----------------------<br>
Not in file<br>
<br>
Icon Location:<br>
--------------<br>
Not in file<br>
<br>
<br>
Extra Data<br>
==========<br>
TrackerDataBlock:<br>
-----------------<br>
Size: 96<br>
Signature: TRACKER_PROPS (0xA0000003)<br>
Length: 88<br>
Version: 0<br>
Machine ID: b''<br>
<br>
DROID:<br>
------<br>
Volume: 09b7eb60-3056-483a-afb8-4ccac688960b<br>
Object: 0a009e41-e49a-11d8-8ba3-00023fb3e570<br>
<br>
DROID Birth:<br>
------------<br>
Volume: 09b7eb60-3056-483a-afb8-4ccac688960b<br>
Object: 0a009e41-e49a-11d8-8ba3-00023fb3e570<br>
</pre>