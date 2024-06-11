# MTDL

A multi-thread based python downloader.

# Usage

1. install: `pip install mtdl`
2. Choose use API or command-line-interface mode

# CMD-Line interface

After installed, just type command like format below:
`mtdl [-h | --help]` to get usage

# API

Create a `MultiThreadDownloader` instance and call its `start` method


`from mtdl import MultiThreadDownloader`<br>
`p = MultiThreadDownloader(<Your url>, (chunk_size, filename))`<br>
`p.start()`


# LICENSE AND NOTICES

See <a href=https://github.com/BillLoic/mtdl/blob/main/LICENSE-en>license file</a>.
