import os
import ssl
import tarfile
import urllib.request as urlrq

import certifi


def download_file(working_dir: str, web_dir: str, name: str) -> None:
    """
    Download a single trace file [name] to [working_dir] from [web_dir]
    @param working_dir:
    @param web_dir:
    @param name:
    """
    # strip file type
    name, _, suffix = name.partition('.')
    suffix = '.' + suffix

    # download the tar archive
    file = urlrq.urlopen(web_dir + name + '.tar.bz2', context=ssl.create_default_context(cafile=certifi.where()))
    tar_name = os.path.join(working_dir, name + '.tar.bz2')
    with open(tar_name, 'wb') as output:
        output.write(file.read())

    # extract hash file from archive
    tar = tarfile.open(tar_name, "r:bz2")
    hash_files = [m for m in tar.getmembers() if m.name.endswith(suffix)]
    for file in hash_files:
        # get just the file without directory structure
        file.name = os.path.basename(file.name)
    tar.extractall(path=working_dir, members=hash_files)
    tar.close()

    # remove the tar archive
    os.remove(tar_name)


def download_files(working_dir: str, web_dir: str, names: [str]):
    print(f'downloading from {web_dir} to {working_dir}')
    print('.' * len(names))
    for name in names:
        download_file(working_dir, web_dir, name)
        print('.', end='', flush=True)
    print()
