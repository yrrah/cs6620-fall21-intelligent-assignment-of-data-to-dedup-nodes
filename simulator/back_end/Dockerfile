FROM image-registry.openshift-image-registry.svc:5000/cs6620-fall21-intelligentassignment-dedupnodes/cs6620-fall21-dedup-nodes-back-end-dependencies:latest

# Add application sources to a directory that the assemble script expects them
# and set permissions so that the container runs without root access
USER 0

ADD . /tmp/src
RUN /usr/bin/fix-permissions /tmp/src

USER 1001

RUN /usr/libexec/s2i/assemble

# Set the default command for the resulting image
CMD /usr/libexec/s2i/run