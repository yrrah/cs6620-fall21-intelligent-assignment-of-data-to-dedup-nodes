# Copyright 2015 gRPC authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""The Python implementation of the GRPC helloworld.Greeter client."""

from __future__ import print_function

import logging
import os
import grpc
import pyrocksdb

from back_end.grpc.hello_world_demo import helloworld_pb2, helloworld_pb2_grpc


def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    server_ip = os.environ['SERVER_IP']
    with grpc.insecure_channel(f'{server_ip}:50051') as channel:
        stub = helloworld_pb2_grpc.GreeterStub(channel)
        response = stub.SayHello(helloworld_pb2.HelloRequest(name='you'))
    print("Greeter client received: " + response.message)
    db_test()


def db_test():
    db = pyrocksdb.DB()
    opts = pyrocksdb.Options()
    # for multi-thread
    # opts.IncreaseParallelism()
    # opts.OptimizeLevelStyleCompaction()
    opts.create_if_missing = True
    s = db.open(opts, 'db_files')
    print(s.code())
    assert (s.ok())
    # put
    opts = pyrocksdb.WriteOptions()
    s = db.put(opts, b"key1", b"value1")
    assert (s.ok())
    # get
    opts = pyrocksdb.ReadOptions()
    blob = db.get(opts, b"key1")
    print(blob.data)  # b"value1"
    print(blob.status.ok())  # true
    # delete
    opts = pyrocksdb.WriteOptions()
    s = db.delete(opts, b"key1")
    assert (s.ok())
    db.close()


if __name__ == '__main__':
    os.environ['SERVER_IP'] = 'localhost'
    logging.basicConfig()
    run()
