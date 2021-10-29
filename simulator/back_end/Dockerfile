FROM quay.io/centos7/python-38-centos7

# Add application sources to a directory that the assemble script expects them
# and set permissions so that the container runs without root access
USER 0

RUN INSTALL_PKGS="centos-release-scl cmake gflags snappy-devel zlib-devel bzip2-devel lz4-devel" && \
    yum -y --setopt=tsflags=nodocs install $INSTALL_PKGS && \
    rpm -V $INSTALL_PKGS && \
    yum -y clean all --enablerepo='*' && \
    yum -y install devtoolset-7-gcc*

#RUN git clone https://github.com/gflags/gflags.git && \
#    cd gflags && \
#    git checkout v2.0 && \
#    ./configure && \
#    make && \
#    make install

ADD . /tmp/src
RUN /usr/bin/fix-permissions /tmp/src


# Install the dependencies
SHELL [ "/usr/bin/scl", "enable", "devtoolset-7"]
RUN gcc --version
USER 1001
RUN gcc --version
RUN /usr/libexec/s2i/assemble

# Set the default command for the resulting image
CMD /usr/libexec/s2i/run