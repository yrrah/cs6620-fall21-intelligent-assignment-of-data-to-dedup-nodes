import matplotlib.pyplot as plt
import pandas as pd


def nondupe_vs_total_count_by_domain(df, title):
    selected = df[['domain', ' non-dupe fp count']].copy()
    selected['total region fp count'] = df[' region fp count'] - selected[' non-dupe fp count']
    selected = selected.groupby(['domain']).sum()
    selected.index = selected.index.astype(int)
    ax = selected.plot.bar(stacked=True, logy=True)
    ax.set_title(title)
    ax.set_ylabel('Count of Fingerprints per Domain')
    ax.set_xticks(ax.get_xticks()[::50])
    ax.set_ylim(10, 2500000000)
    plt.show()


def nondupe_vs_total_count_by_pod(df, group_by_func, title):
    selected = df[['domain', ' non-dupe fp count']].copy()
    selected['total region fp count'] = df[' region fp count'] - selected[' non-dupe fp count']
    selected = selected.groupby(lambda x: group_by_func(selected, x, 'domain')).sum()
    ax = selected[[' non-dupe fp count', 'total region fp count']].plot.bar(stacked=True, logy=True)
    ax.set_title(title)
    ax.set_xlabel('Pod')
    ax.set_ylabel('Count of Fingerprints per Pod')
    ax.set_ylim(10, 2500000000)
    selected['ratio'] = (selected[' non-dupe fp count'] / (selected['total region fp count'] +
                                                           selected[' non-dupe fp count'])
                         ).round(3)
    for i, v in enumerate(selected['ratio']):
        ax.annotate(str(v), (i-0.1, 1000), fontsize=20)
    plt.show()


def nondupe_vs_total_bytes_by_domain(df, title):
    selected = df[['domain', ' non-dupe bytes']].copy()
    selected['total region bytes'] = df[' region bytes'] - selected[' non-dupe bytes']
    selected = selected.groupby(['domain']).sum()
    selected.index = selected.index.astype(int)
    ax = selected.plot.bar(stacked=True, logy=True)
    ax.set_title(title)
    ax.set_xticks(ax.get_xticks()[::50])
    plt.show()


def nondupe_vs_total_bytes_by_pod(df, group_by_func, title):
    selected = df[['domain', ' non-dupe bytes']].copy()
    selected['total region bytes'] = df[' region bytes'] - selected[' non-dupe bytes']
    selected = selected.groupby(lambda x: group_by_func(selected, x, 'domain')).sum()
    ax = selected[[' non-dupe bytes', 'total region bytes']].plot.bar(stacked=True, logy=True)
    ax.set_title(title)
    ax.set_xlabel('Pod')
    plt.show()


def hashes_per_user_per_day(df, title):
    # df = df[(df[' hash date'] > '2011-01-01') & (df[' hash date'] < '2012-03-01')]
    selected = df[[' user', ' hash date']].copy()
    selected['User'] = 1
    selected = selected.groupby([' hash date', ' user']).count()
    selected = selected.unstack(fill_value=0)
    table = str.maketrans(dict.fromkeys('\', ()'))
    selected.columns = [' '.join(str(col)).translate(table) for col in selected.columns.values]
    # selected = selected.reset_index()
    # selected = selected.set_index(' hash date', ' user').reset_index()
    # selected = selected.groupby(' hash date').max()
    print(df.index)
    ax = selected.plot(linestyle='none', marker='o', logy=True)
    ax.set_ylabel('4MB Regions per Day')
    ax.set_xlabel(None)
    ax.set_title(f'Total 4MB Regions = {df.shape[0]}')
    # ax.set_xticks(ax.get_xticks()[::50])
    plt.tight_layout()
    plt.show()


def parse_file(file_name, title=None, outlier=None):
    environment_vars = {}
    col_index = {}
    with open(file_name, 'r') as f:
        line = f.readline()
        env_column = line.index("SIMULATOR_")
        while line[0] == ',':
            key, val = line[env_column:-1].split(':')
            environment_vars[key] = val
            line = f.readline()

        for i, heading in enumerate(line[:-1].split(',')):
            col_index[heading] = i

    print(environment_vars)
    print(col_index)
    duration = float(environment_vars['STOP_TIME']) - float(environment_vars['START_TIME'])
    print(f'Duration was: {duration / 60} min')

    if title is None:
        title = environment_vars['SIMULATOR_RUN_NAME']
    num_domains = int(environment_vars['SIMULATOR_DOMAINS'])

    def group_by_pod(df, ind, col):
        return int(int(df[col].loc[ind]) / num_domains)

    whole_log = pd.read_csv(file_name,
                            skiprows=len(environment_vars),
                            parse_dates=[' hash date'])
    if outlier is not None:
        whole_log = whole_log[whole_log['domain'] != outlier]
        title += f'without outlier domain {outlier}'

    hashes_per_user_per_day(whole_log, title)
    nondupe_vs_total_count_by_domain(whole_log, title)
    # nondupe_vs_total_bytes_by_domain(whole_log, title)
    nondupe_vs_total_count_by_pod(whole_log, group_by_pod, title)
    # nondupe_vs_total_bytes_by_pod(whole_log, group_by_pod, title)


def main():
    parse_file('1637860767.csv')


if __name__ == "__main__":
    main()
