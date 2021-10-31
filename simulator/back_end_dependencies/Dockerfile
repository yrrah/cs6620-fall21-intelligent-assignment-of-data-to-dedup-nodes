FROM quay.io/centos7/python-38-centos7
# https://github.com/sclorg/s2i-python-container/blob/generated/3.8/README.md

# Add application sources to a directory that the assemble script expects them
# and set permissions so that the container runs without root access
USER 0

RUN INSTALL_PKGS="centos-release-scl cmake snappy-devel zlib-devel bzip2-devel lz4-devel" && \
    yum -y --setopt=tsflags=nodocs install $INSTALL_PKGS && \
    rpm -V $INSTALL_PKGS && \
    yum -y clean all --enablerepo='*' && \
    yum -y install devtoolset-7-gcc*

RUN git clone https://github.com/gflags/gflags.git && \
    cd gflags && \
    git checkout v2.0 && \
    ./configure && \
    make && \
    make install

USER 1001

# Install the dependencies
SHELL [ "/usr/bin/scl", "enable", "devtoolset-7"]
RUN gcc --version
RUN pip install 'python-rocksdb @ git+https://git@github.com/twmht/python-rocksdb@pybind11#egg=python-rocksdb'