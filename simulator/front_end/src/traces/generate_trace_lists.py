from datetime import datetime

import htmllistparse


def get_web_dir_list(web_dir: str, user_nums: [str], chunk_size: str = '8kb', limit=None) -> [[str], int]:
    """
    Get a list of trace files from a directory on https://tracer.filesystems.org/traces/
    @param user_nums: List of 3-zeros-padded [###, ###] user number strings
    @param chunk_size:
    @param web_dir: URL of the html directory list
    @param limit: (int) Max number of files to list
    @return: the file list, total size in bytes
    """
    cwd, listing = htmllistparse.fetch_listing(web_dir, timeout=30)
    prefix = set()
    for nnn in user_nums:
        prefix.add(f'fslhomes-user{nnn}')

    names = []
    total_bytes = 0
    for f in listing:
        if f.name.endswith('.tar.bz2') and f.name[:16] in prefix:
            names.append(f"{f.name.split('.')[0]}.{chunk_size}.hash.anon")
            total_bytes += f.size

        if limit is not None and len(names) == limit:
            break

    return names, total_bytes


def sort_by_date(trace_list: [str]):
    trace_list.sort(key=lambda x: datetime.strptime(x[17:27], '%Y-%m-%d').timestamp())


def generate_user_list(user_nums: [str], sub_dir: str) -> int:
    """
    Creates a list of trace files with filename like 'fslhomes_2011-8kb-only_user006011.txt'.
    The list is sorted by date.
    @param user_nums: List of 3-zeros-padded [###, ###] user number strings
    @param sub_dir: directory on traces website to download from
    @return: generates a file and returns (int) total bytes for trace files listed in the file
    """
    trace_files, total_size = get_web_dir_list("https://tracer.filesystems.org/traces/" + sub_dir, user_nums=user_nums)
    if total_size > 0:
        sort_by_date(trace_files)
        filename = sub_dir.replace('/', '_')
        for u in user_nums:
            filename = filename + u
        with open(filename, 'w') as fh:
            fh.writelines("%s\n" % line for line in trace_files[:-1])
            fh.write(trace_files[-1])
        with open('output.txt', 'a') as fh:
            fh.write(f'{round(total_size/1024/1024/1024, 2)} GiB : {filename}\n')
    return total_size


def generate_user_list_all_subdirs(user_nums: [str]):
    """
    Runs generate_user_list for all sub-directories of traces website
    @param user_nums:
    @return:
    """
    total_size = 0
    for sub_dir in ["2011-8kb-only/", "2012-8kb-only/", "2012/", "2013/", "2014/", "2015/"]:
        size = generate_user_list(user_nums, "fslhomes/" + sub_dir)
        print(f'bytes:{size} subdir: {sub_dir}')
        total_size += size
    print(f'total bytes:{total_size}')


if __name__ == "__main__":
    generate_user_list_all_subdirs(["018"])
