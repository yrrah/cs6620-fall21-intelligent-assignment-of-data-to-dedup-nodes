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
            names.append(f.name)
            # names.append(f"{f.name.split('.')[0]}.{chunk_size}.hash.anon")
            total_bytes += f.size

        if limit is not None and len(names) == limit:
            break

    return names, total_bytes


def sort_by_date(trace_list: [str]):
    trace_list.sort(key=lambda x: datetime.strptime(x[17:27], '%Y-%m-%d').timestamp())


def slice_between_dates(sorted_trace_list: [str], start_date: str, end_date: str):
    """
    slice the list including traces on start_date, excluding traces on end_date
    both dates must exist in the list
    @param sorted_trace_list:
    @param start_date:
    @param end_date:
    @return:
    """
    start_index = next(i for i, x in enumerate(sorted_trace_list) if x[17:27] == start_date)
    end_index = next(i for i, x in enumerate(sorted_trace_list) if x[17:27] == end_date)
    return sorted_trace_list[start_index:end_index]


def filter_dates(trace_list: [str], date_set: {str}):
    """

    @param trace_list:
    @param date_set:
    @return:
    """
    return [trace for trace in trace_list if trace[17:27] in date_set]


def generate_user_list(user_nums: [str], sub_dir: str, start_date: str or None, end_date: str or None,
                       date_set: {str} or None) -> int:
    """
    Creates a list of trace files with filename like 'fslhomes_2011-8kb-only_user006011.txt'.
    The list is sorted by date.
    @param date_set:
    @param end_date:
    @param start_date:
    @param user_nums: List of 3-zeros-padded [###, ###] user number strings
    @param sub_dir: directory on traces website to download from
    @return: generates a file and returns (int) total bytes for trace files listed in the file
    """
    trace_files, total_size = get_web_dir_list("https://tracer.filesystems.org/traces/" + sub_dir, user_nums=user_nums)
    if total_size > 0:
        sort_by_date(trace_files)
        if date_set is not None:
            trace_files = filter_dates(trace_files, date_set)
        elif start_date is not None and end_date is not None:
            trace_files = slice_between_dates(trace_files, start_date, end_date)
        filename = sub_dir.replace('/', '_')
        for u in user_nums:
            filename = filename + u
        with open(filename, 'w') as fh:
            fh.writelines("%s\n" % line for line in trace_files[:-1])
            fh.write(trace_files[-1])
        with open('output.txt', 'a') as fh:
            fh.write(f'{round(total_size / 1024 / 1024 / 1024, 2)} GiB : {filename}\n')
    return total_size


def generate_user_list_all_subdirs(user_nums: [str], start_date=None, end_date=None, date_set=None):
    """
    Runs generate_user_list for all sub-directories of traces website
    @param date_set:
    @param end_date:
    @param start_date:
    @param user_nums:
    @return:
    """
    total_size = 0
    # for sub_dir in ["2011-8kb-only/", "2012-8kb-only/", "2012/", "2013/", "2014/", "2015/"]:
    for sub_dir in ["2011-8kb-only/", "2012-8kb-only/"]:
        size = generate_user_list(user_nums, "fslhomes/" + sub_dir, start_date, end_date, date_set)
        print(f'bytes:{size} subdir: {sub_dir}')
        total_size += size
    print(f'total bytes:{total_size}')


if __name__ == "__main__":
    # generate_user_list_all_subdirs(["025"], '2011-09-16', '2011-10-01')  # 2011
    # generate_user_list_all_subdirs(["014", "018", "019"], start_date='2011-09-16', end_date='2011-10-01')  # 2011
    # every_5 = {'2012-08-29', '2012-09-03', '2012-09-09', '2012-09-18', '2012-09-23',
    #            '2012-10-02', '2012-10-19', '2012-10-27', '2012-11-14', '2012-11-19'}
    # every_5 = {'2011-09-30', '2011-10-05', '2011-10-10', '2011-10-15', '2011-10-20',
    #            '2011-10-25', '2011-10-30', '2011-11-04', '2011-11-09', '2011-12-02',
    #            '2011-12-07', '2011-12-12', '2011-12-17', '2011-12-22', '2011-12-29',
    #            '2012-01-03', '2012-01-08', '2012-01-13', '2012-01-20', '2012-01-25'}
    # every_10 = {'2011-09-16', '2011-09-25', '2011-10-05', '2011-10-15', '2011-10-30', '2011-11-09',
    #             '2011-12-12', '2011-12-22', '2012-01-03', '2012-01-13', '2012-01-25'}
    every_20 = {'2011-09-16', '2011-10-05', '2011-10-30', '2011-12-12', '2012-01-03', '2012-01-25'}
    generate_user_list_all_subdirs(["014", "018", "019", "028"], date_set=every_20)  # 2011
    # generate_user_list_all_subdirs(["014", "017", "018", "019", "028"], date_set=every_5)  # 2011
    # generate_user_list_all_subdirs(["005, 008"])  # 2012
    # generate_user_list_all_subdirs(["026", "022"])  # 2013
