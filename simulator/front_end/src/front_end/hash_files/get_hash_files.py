import glob
import ssl
import tarfile

import certifi
import htmllistparse
import os
import urllib.request as urlrq
from tqdm import tqdm


def get_web_dir_list(web_dir: str, limit: int) -> [str]:
    """
    Get a list of trace files from a directory on https://tracer.filesystems.org/traces/
    @param web_dir: URL of the html directory list
    @param limit: Max number of files to list
    @return: the file list
    """
    cwd, listing = htmllistparse.fetch_listing(web_dir, timeout=30)
    names = [f.name for f in listing if f.name.endswith('.tar.bz2')]
    return names[:limit]


def download_file(working_dir: str, web_dir: str, name: str) -> None:
    """
    Download a single trace file [name] to [working_dir] from [web_dir]
    @param working_dir:
    @param web_dir:
    @param name:
    """
    # strip file type
    name = name.split('.')[0]

    # download the tar archive
    file = urlrq.urlopen(web_dir + name + '.tar.bz2', context=ssl.create_default_context(cafile=certifi.where()))
    tar_name = os.path.join(working_dir, name + '.tar.bz2')
    with open(tar_name, 'wb') as output:
        output.write(file.read())

    # extract hash file from archive
    tar = tarfile.open(tar_name, "r:bz2")
    hash_files = [m for m in tar.getmembers() if m.name.endswith('.hash.anon')]
    for file in hash_files:
        # get just the file without directory structure
        file.name = os.path.basename(file.name)
    tar.extractall(path=working_dir, members=hash_files)
    tar.close()

    # remove the tar archive
    os.remove(tar_name)


def download_files(working_dir: str, web_dir: str, names: [str]):
    for name in tqdm(names):
        name = name.split('.')[0]
        # Download the file if it does not yet exist
        if not glob.glob(os.path.join(working_dir, name + '*.hash.anon')):
            download_file(working_dir, web_dir, name)


def main():
    trace_files = get_web_dir_list("https://tracer.filesystems.org/traces/fslhomes/2011-8kb-only/", limit=15)
    download_files(".", "https://tracer.filesystems.org/traces/fslhomes/2011-8kb-only/", trace_files)


if __name__ == "__main__":
    main()
