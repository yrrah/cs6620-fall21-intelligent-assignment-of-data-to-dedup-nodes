# Adapted from C code hf-stat.c, libhashfile.h, libhashfile.c from fs-hasher-0.9.5
# from https://tracer.filesystems.org/ with the following original licence
#  * Copyright (c) 2011-2014 Vasily Tarasov
#  * Copyright (c) 2011       Will Buik
#  * Copyright (c) 2011-2014 Philip Shilane
#  * Copyright (c) 2011-2014 Erez Zadok
#  * Copyright (c) 2011-2014 Geoff Kuenning
#  * Copyright (c) 2011-2014 Stony Brook University
#  * Copyright (c) 2011-2014 Harvey Mudd College
#  * Copyright (c) 2011-2014 The Research Foundation of the State University of New York
#  *
#  * This program is free software; you can redistribute it and/or modify
#  * it under the terms of the GNU General Public License version 3 as
#  * published by the Free Software Foundation.

from enum import IntEnum
from struct import unpack, calcsize
from typing import BinaryIO

HASH_FILE_MAGIC = int(0xDEADDEAD)
MAX_PATH_SIZE = 4096
MAX_SYSID_LEN = 4096


class HashFileVersion(IntEnum):
    V1 = 1
    V2 = 2
    V3 = 3
    V4 = 4
    V5 = 5
    V6 = 6
    V7 = 7


class HashingMethod(IntEnum):
    MD5_HASH = 1,
    SHA256_HASH = 2,
    MD5_48BIT_HASH = 3,
    MURMUR_HASH = 4,
    MD5_64BIT_HASH = 5,
    SHA1_HASH = 6,


class CompareMethod(IntEnum):
    NONE = 0,
    ZLIB_DEF = 1


class Chunking:
    class Method(IntEnum):
        FIXED = 1,
        VARIABLE = 2

    class VariableAlgo(IntEnum):
        RANDOM = 1,
        SIMPLE_MATCH = 2,
        RABIN = 3

    def __init__(self, file: BinaryIO):
        self.file = file
        self.chunking_method = 0

        # fixed chunking
        self.fixed_chunk_size = -1

        # variable random chunking
        self.probability = -1

        # variable simple/rabin chunking
        self.bits_to_compare = -1
        self.pattern = -1
        self.window_size = -1
        self.prime = -1
        self.module = -1
        self.bits_to_compare = -1
        self.pattern = -1

        self._set_algo()

    def _set_algo(self):
        self.chunking_method, chunking_option = unpack("ii", self.file.read(calcsize("ii")))

        if self.chunking_method == self.Method.FIXED:
            self.fixed_chunk_size = chunking_option

        elif self.chunking_method == self.Method.VARIABLE:
            if chunking_option == self.VariableAlgo.RANDOM:
                params = "l"
                # probability to chunk a stream
                self.probability = unpack(params, self.file.read(calcsize(params)))

            elif chunking_option == self.VariableAlgo.SIMPLE_MATCH:
                params = "il"
                self.bits_to_compare, self.pattern = unpack(params, self.file.read(calcsize(params)))

            elif chunking_option == self.VariableAlgo.RABIN:
                params = "illil"
                # window size is in bytes
                self.window_size, self.prime, self.module, self.bits_to_compare, self.pattern \
                    = unpack(params, self.file.read(calcsize(params)))

            else:
                raise ValueError('Invalid variable chunking algorithm.')

        else:
            raise ValueError('Invalid chunking method.')


#  struct hashfile_handle {
#     int                 fd;
#     enum openmode            omode;
#     struct header_v4        header;
#     struct abstract_file_header     current_file;
#     /* offset of current file's header. Used only when we write a file. */
#     off_t                current_file_header_offset;
#     struct chunk_info        current_chunk_info;
#     uint64_t            num_files_processed;
#     uint64_t            num_hashes_processed_current_file;
# };

class HashFile:
    def __init__(self, file_path: str) -> None:
        # header info
        self.file = open(file_path, "rb")
        self.version = 0
        self.total_files = 0
        self.path_root = ""
        self.total_chunks = 0
        self.chunking_params: Chunking
        self.hashing_method = 0
        self.hash_size = 0
        self.sysid = ""
        self.start_time = 0
        self.end_time = 0
        self.total_bytes = 0

        # state to keep track of reading chunks
        self.current_chunk_size = 0
        self.current_chunk_hash = 0
        self.current_chunk_compression_ratio = 0
        self.current_file_total_size = 0
        self.current_file_total_chunks = 0
        self.num_hashes_processed_current_file = 0
        self.num_files_processed = 0

        self._read_header()

    def _read_header(self):
        """
        Assumes we are reading a v7 formatted trace file
        """
        header_v4 = f"Iil{MAX_PATH_SIZE}sl"
        header = unpack(header_v4, self.file.read(calcsize(header_v4)))
        magic, self.version, self.total_files, path_root, self.total_chunks = header

        if magic != HASH_FILE_MAGIC:
            raise ValueError("Wrong file type.")

        self.path_root = path_root.decode('ascii').split('\x00', 1)[0]
        self.chunking_params = Chunking(self.file)

        header_v4 = f"ii{MAX_SYSID_LEN}slll"
        header = unpack(header_v4, self.file.read(calcsize(header_v4)))
        self.hashing_method, self.hash_size, sysid, self.start_time, self.end_time, self.total_bytes = header

        self.sysid = sysid.decode('ascii').split('\x00', 1)[0]

    # /* This function gets the next file information from hash file into
    #  * current_file field of hashfile_handle. Prepares the abstract_file_header
    #  * for the same. The return values from this function are little different.
    #  * 0 indicates EOF, 1 indicates success and < 0 indicates error -- typical
    #  * cases of read system call.
    #  */
    def hashfile_next_file(self):
        # /* EOF Condition */
        assert (self.num_files_processed < self.total_files)

        #
        # /* Setting this because in case user retries for EAGAIN error, the
        #  * file pointer should not really move. We are doing it only when
        #  * lseek is successful
        #  */
        self.num_hashes_processed_current_file = self.current_file_total_chunks

        if self.version > HashFileVersion.V1:
            self.current_file_total_size = int.from_bytes(self.file.read(8), "little")
            if self.version > HashFileVersion.V4:
                blocks = int.from_bytes(self.file.read(8), "little")

            if self.version > HashFileVersion.V3:
                file_header = f"iillllllllii"
                header = unpack(file_header, self.file.read(calcsize(file_header)))
                uid, gid, perm, atime, mtime, ctime, hardlinks, deviceid, inodenum \
                    , self.current_file_total_chunks, pathlen, target_pathlen = header
                file_header = f"{pathlen}s{target_pathlen}s"
                path, target_path = unpack(file_header, self.file.read(calcsize(file_header)))

            else:
                file_header_v2 = f"li{MAX_PATH_SIZE}s"
                self.current_file_total_chunks, pathlen = unpack(file_header_v2,
                                                                 self.file.read(calcsize(file_header_v2)))
                file_header_v2 = f"{pathlen}s"
                path = unpack(file_header_v2, self.file.read(calcsize(file_header_v2)))

        elif self.version == HashFileVersion.V1:
            file_header = f"{MAX_PATH_SIZE}sll"
            header = unpack(file_header, self.file.read(calcsize(file_header)))
            path, self.current_file_total_size, self.current_file_total_chunks = header

        else:
            raise ValueError('Invalid file header.')

        path = path.decode('ascii')
        # print(path)

        self.num_files_processed += 1
        self.num_hashes_processed_current_file = 0

    def hashfile_next_chunk(self):
        assert (self.num_hashes_processed_current_file < self.current_file_total_chunks)

        if self.version >= HashFileVersion.V7 and self.chunking_params.chunking_method == Chunking.Method.VARIABLE:
            self.current_chunk_size = unpack("i", self.file.read(calcsize("i")))

        elif (self.version >= HashFileVersion.V3 and
              self.chunking_params.chunking_method == Chunking.Method.VARIABLE):
            self.current_chunk_size = unpack("l", self.file.read(calcsize("l")))
        elif self.chunking_params.chunking_method == Chunking.Method.FIXED:
            if self.current_file_total_chunks - 1 == self.num_hashes_processed_current_file:
                # /* Last chunk */
                self.current_chunk_size = self.current_file_total_size - (
                    self.current_file_total_chunks - 1) * self.chunking_params.fixed_chunk_size
                # /* Detect if tail was on or off */
                if self.current_chunk_size > self.chunking_params.fixed_chunk_size:
                    self.current_chunk_size = self.chunking_params.fixed_chunk_size
            else:
                self.current_chunk_size = self.chunking_params.fixed_chunk_size
        else:
            # /*
            #  * Hashfile version 2 does not have chunk size for
            #  * variable chunking. So, just report 0.
            #  */
            self.current_chunk_size = 0

        hash_bytes = self.hash_size // 8
        self.current_chunk_hash = unpack(f"{hash_bytes}s", self.file.read(hash_bytes))[0]

        if self.version >= HashFileVersion.V6:
            self.current_chunk_compression_ratio = int.from_bytes(self.file.read(1), "little")
        else:
            # /*
            #  * If cratio is not available (old hashfiles), set it to zero.
            #  */
            self.current_chunk_compression_ratio = 0

        self.num_hashes_processed_current_file += 1

        return self.current_chunk_hash, self.current_chunk_compression_ratio, self.current_chunk_size[0]


#  * v.7:
#  *
#  * In the beginning:
#  * HEADER (struct header_v4)
#  *
#  * Then, if FIXED size chunking:
#  * FILE_HEADER 1 (struct file_header_v4)
#  * <hash1><cratio1><hash2><cratio2>...<hashN_1><cratioN_1>
#  * FILE_HEADER 2 (struct file_header_v4)
#  * <hash1><cratio1><hash2><cratio2>...<hashN_1><cratioN_2>
#  * ...
#  * FILE_HEADER M (struct file_header_v4)
#  * <hash1><cratio1><hash2><cratio2>...<hashN_M><cratioN_M>
#  *
#  * And if VARIABLE size chunking (chunk size added):
#  * FILE_HEADER 1 (struct file_header_v4)
#  * <chunk_size1><hash1><cratio1><chunk_size2><hash2><cratio2>...<chunk_sizeN_1><hashN_1><cratioN_1>
#
#  * FILE_HEADER 2 (struct file_header_v4)
#  * <chunk_size1><hash1><cratio1><chunk_size2><hash2><cratio2>...<chunk_sizeN_2><hashN_1><cratioN_2>
#  * ...
#  * FILE_HEADER M (struct file_header_v4)
#  * <chunk_size1><hash1><cratio1><chunk_size2><hash2><cratio2>...<chunk_sizeN_M><hashN_M><cratioN_M>
#  *
#  * chunk_size is uint32_t
#  * cratio is uint8_t

def joinit(iterable, delimiter):
    it = iter(iterable)
    count = 0
    for x in it:
        if count % 2 == 0 and count > 0:
            yield delimiter
        yield x
        count += 1


def main():
    file_name = input("Please enter the hash file name to read: ")
    read_file = HashFile(file_name)

    while read_file.num_files_processed < 10:
        read_file.hashfile_next_file()
        while read_file.num_hashes_processed_current_file < read_file.current_file_total_chunks:
            fingerprint, compression = read_file.hashfile_next_chunk()
            print(''.join(list(joinit(str(fingerprint.hex()), ':'))))


if __name__ == "__main__":
    main()
