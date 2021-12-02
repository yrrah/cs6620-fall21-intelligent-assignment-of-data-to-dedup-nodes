import os
import csv
import matplotlib.pyplot as plt
import pandas as pd


def nondupe_vs_total_count_by_domain(df, title, save, show):
    selected = df[['domain', ' non-dupe fp count']].copy()
    selected['total region fp count'] = df[' region fp count'] - selected[' non-dupe fp count']
    selected = selected.groupby(['domain']).sum()
    selected.index = selected.index.astype(int)
    if save or show:
        ax = selected.plot.bar(stacked=True)
        ax.set_title(title)
        ax.set_ylabel('Count of Fingerprints per Domain')
        ax.set_xticks(ax.get_xticks()[::50])
        # ax.set_ylim(10, 2500000000)
    if save:
        plt.savefig(f'{title}_nondupe_vs_total_count_by_domain.png')
    if show:
        plt.show()


def nondupe_vs_total_bytes_by_domain(df, title, save, show) -> [float]:
    selected = df[['domain', ' non-dupe bytes']].copy()
    selected['total region bytes'] = df[' region bytes'] - selected[' non-dupe bytes']
    by_domain = selected.groupby(['domain']).sum()
    by_domain[' region bytes'] = by_domain['total region bytes'] + by_domain[' non-dupe bytes']
    by_domain.index = by_domain.index.astype(int)
    if save or show:
        ax = by_domain[[' non-dupe bytes', 'total region bytes']].plot.bar(stacked=True)
        ax.set_title(title)
        ax.set_ylabel('Total Bytes sent to Domain')
        ax.set_xticks(ax.get_xticks()[::50])
    if save:
        plt.savefig(f'{title}_nondupe_vs_total_bytes_by_domain.png')
    if show:
        plt.show()
    mean_domain_phys = by_domain[' non-dupe bytes'].mean()
    std_domain_phys = by_domain[' non-dupe bytes'].std()
    mean_domain_logical = by_domain[' region bytes'].mean()
    std_domain_logical = by_domain[' region bytes'].std()
    overall_dedup = (by_domain[' region bytes'].sum() / selected[' non-dupe bytes'].sum()).round(1)
    stats = [overall_dedup, mean_domain_phys, std_domain_phys, mean_domain_logical, std_domain_logical]
    return stats


def nondupe_vs_total_count_by_pod(df, group_by_func, title, save, show):
    selected = df[['domain', ' non-dupe fp count']].copy()
    selected['total region fp count'] = df[' region fp count'] - selected[' non-dupe fp count']
    selected = selected.groupby(lambda x: group_by_func(selected, x, 'domain')).sum()
    selected['ratio'] = ((selected['total region fp count'] + selected[' non-dupe fp count'])
                         / selected[' non-dupe fp count']).round(1)
    if save or show:
        ax = selected[[' non-dupe fp count', 'total region fp count']].plot.bar(stacked=True)
        ax.set_title(title)
        ax.set_xlabel('Pod')
        ax.set_ylabel('Total Fingerprints sent to Pod')
        for i, v in enumerate(selected['ratio']):
            ax.annotate(f'{v}X', (i - 0.1, 1000), fontsize=20)
    if save:
        plt.savefig(f'{title}_nondupe_vs_total_count_by_pod.png')
    if show:
        plt.show()
    return selected['ratio'].values


def nondupe_vs_total_bytes_by_pod(df, group_by_func, title, save, show) -> [float]:
    selected = df[['domain', ' non-dupe bytes']].copy()
    selected['total region bytes'] = df[' region bytes'] - selected[' non-dupe bytes']
    by_pod = selected.groupby(lambda x: group_by_func(selected, x, 'domain')).sum()
    by_pod[' region bytes'] = by_pod['total region bytes'] + by_pod[' non-dupe bytes']
    by_pod['ratio'] = (by_pod[' region bytes'] / by_pod[' non-dupe bytes']).round(1)
    if save or show:
        ax = by_pod[[' non-dupe bytes', 'total region bytes']].plot.bar(stacked=True)
        ax.set_title(title)
        ax.set_xlabel('Pod')
        ax.set_ylabel('Total Bytes sent to Pod')
        for i, v in enumerate(by_pod['ratio']):
            ax.annotate(f'{v}X', (i - 0.1, 1000), fontsize=20)
    if save:
        plt.savefig(f'{title}_nondupe_vs_total_bytes_by_pod.png')
    if show:
        plt.show()

    mean_pod_phys = by_pod[' non-dupe bytes'].mean()
    std_pod_phys = by_pod[' non-dupe bytes'].std()
    mean_pod_logical = by_pod[' region bytes'].mean()
    std_pod_logical = by_pod[' region bytes'].std()
    stats = [mean_pod_phys, std_pod_phys, mean_pod_logical, std_pod_logical]
    num_pods = 8
    for dedup in by_pod['ratio']:
        stats.append(dedup)
        num_pods -= 1
    for _ in range(num_pods):
        stats.append(0)
    return stats


def hashes_per_user_per_day(df, title, save, show):
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
    # print(df.index)
    if save or show:
        ax = selected.plot(linestyle='none', marker='o')
        ax.set_ylabel('4MB Regions per Day')
        ax.set_xlabel(None)
        ax.set_title(f'Total 4MB Regions = {df.shape[0]}')
        # ax.set_xticks(ax.get_xticks()[::50])
        plt.tight_layout()
    if save:
        plt.savefig(f'{title}_hashes_per_user_per_day.png')
    if show:
        plt.show()


def parse_file(file_name):
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
    # print(col_index)

    whole_log = pd.read_csv(file_name,
                            skiprows=len(environment_vars),
                            parse_dates=[' hash date'])
    whole_log.rename(columns={"omain": "domain"})
    return whole_log, environment_vars


def filter_outlier_domain(log_df, outlier):
    return log_df[log_df['domain'] != outlier]


def process_directory(logs_path: str, save_plots: bool, show_plots: bool):
    files = set(next(os.walk(logs_path), (None, None, []))[2])

    summary_results = []
    summary_results.append(['run_name', 'duration', 'overall_dedup',
                            'mean_domain_phys', 'std_domain_phys', 'mean_domain_logical', 'std_domain_logical',
                            'mean_pod_phys', 'std_pod_phys', 'mean_pod_logical', 'std_pod_logical',
                            'pod1 dedup', 'pod2 dedup', 'pod3 dedup', 'pod4 dedup',
                            'pod5 dedup', 'pod6 dedup', 'pod7 dedup', 'pod8 dedup'])

    for file_name in files:
        log_dataframe, env_vars = parse_file(logs_path + file_name)

        title = env_vars['SIMULATOR_RUN_NAME']
        num_domains = int(env_vars['SIMULATOR_DOMAINS'])

        def group_by_pod(df, ind, col):
            return int(int(df[col].loc[ind]) / num_domains)

        print(file_name)
        duration = (float(env_vars['STOP_TIME']) - float(env_vars['START_TIME'])) / 60
        stats = [title, duration]
        # hashes_per_user_per_day(log_dataframe, title, save_plots, show_plots)
        # nondupe_vs_total_count_by_domain(log_dataframe, title, save_plots, show_plots)
        # nondupe_vs_total_count_by_pod(log_dataframe, group_by_pod, title, save_plots, show_plots)
        domain_stats = nondupe_vs_total_bytes_by_domain(log_dataframe, title, save_plots, show_plots)
        pod_stats = nondupe_vs_total_bytes_by_pod(log_dataframe, group_by_pod, title, save_plots, show_plots)
        stats.extend(domain_stats)
        stats.extend(pod_stats)
        summary_results.append(stats)

    with open("summary.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(summary_results)


def main():
    process_directory('./ex0/', save_plots=False, show_plots=True)


if __name__ == "__main__":
    main()
