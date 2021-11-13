import matplotlib.pyplot as plt
import pandas as pd


def nondupe_vs_total_count_by_domain(df):
    selected = df[['domain', ' non-dupe fp count']].copy()
    selected['total region fp count'] = df[' region fp count'] - selected[' non-dupe fp count']
    selected = selected.groupby(['domain']).sum()
    selected.index = selected.index.astype(int)
    ax = selected.plot.bar(stacked=True, logy=True)
    ax.set_xticks(ax.get_xticks()[::50])
    plt.show()


def nondupe_vs_total_count_by_pod(df, group_by_func):
    selected = df[['domain', ' non-dupe fp count']].copy()
    selected['total region fp count'] = df[' region fp count'] - selected[' non-dupe fp count']
    selected = selected.groupby(lambda x: group_by_func(selected, x, 'domain')).sum()
    ax = selected[[' non-dupe fp count', 'total region fp count']].plot.bar(stacked=True)
    plt.show()


def nondupe_vs_total_bytes_by_domain(df):
    selected = df[['domain', ' non-dupe bytes']].copy()
    selected['total region bytes'] = df[' region bytes'] - selected[' non-dupe bytes']
    selected = selected.groupby(['domain']).sum()
    selected.index = selected.index.astype(int)
    ax = selected.plot.bar(stacked=True, logy=True)
    ax.set_xticks(ax.get_xticks()[::50])
    plt.show()


def nondupe_vs_total_bytes_by_pod(df, group_by_func):
    selected = df[['domain', ' non-dupe bytes']].copy()
    selected['total region bytes'] = df[' region bytes'] - selected[' non-dupe bytes']
    selected = selected.groupby(lambda x: group_by_func(selected, x, 'domain')).sum()
    ax = selected[[' non-dupe bytes', 'total region bytes']].plot.bar(stacked=True)
    plt.show()


def parse_file(file_name, outlier=None):
    with open(file_name, 'r') as f:
        env_var = f.readline()
        num_domains = int(env_var.split("SIMULATOR_DOMAINS")[1].split(',')[0].split(':')[1])

    def group_by_pod(df, ind, col):
        return int(int(df[col].loc[ind]) / num_domains)

    whole_log = pd.read_csv(file_name, skiprows=8)
    nondupe_vs_total_count_by_domain(whole_log)
    nondupe_vs_total_bytes_by_domain(whole_log)
    if outlier is not None:
        whole_log = whole_log[whole_log['domain'] != outlier]
    nondupe_vs_total_count_by_pod(whole_log, group_by_pod)
    nondupe_vs_total_bytes_by_pod(whole_log, group_by_pod)


def main():
    parse_file('./sample_results.csv', outlier=375)


if __name__ == "__main__":
    main()
