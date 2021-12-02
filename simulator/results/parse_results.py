import csv
import os

import pandas as pd

from simulator.results.plots import nondupe_vs_total_bytes_by_domain, nondupe_vs_total_bytes_by_pod, \
    hashes_per_user_per_day, nondupe_vs_total_count_by_domain, nondupe_vs_total_count_by_pod, region_count_by_domain, \
    region_size_stats


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
    whole_log = whole_log.rename(columns={"omain": "domain"})
    return whole_log, environment_vars


def filter_outlier_domain(log_df, outlier):
    return log_df[log_df['domain'] != outlier]


def process_directory(logs_path: str, save_plots: bool, show_plots: bool):
    files = set(next(os.walk(logs_path), (None, None, []))[2])

    summary_results = [
        ['run_name', 'duration', 'min_region_bytes', 'max_region_bytes', 'mean_region_bytes', 'std_region_bytes',
         'overall_dedup', 'mean_domain_phys', 'std_domain_phys', 'min_domain_phys', 'max_domain_phys',
         'mean_domain_logical', 'std_domain_logical', 'min_domain_logical', 'max_domain_logical',
         'mean_pod_phys', 'std_pod_phys', 'min_pod_phys', 'max_pod_phys',
         'mean_pod_logical', 'std_pod_logical', 'min_pod_logical', 'max_pod_logical',
         'pod1 dedup', 'pod2 dedup', 'pod3 dedup', 'pod4 dedup',
         'pod5 dedup', 'pod6 dedup', 'pod7 dedup', 'pod8 dedup']]

    for file_name in files:
        log_dataframe, env_vars = parse_file(logs_path + file_name)

        title = env_vars['SIMULATOR_RUN_NAME']
        num_pods = len(env_vars['SIMULATOR_BACKEND_IPS'].split(','))
        domains_per_pod = int(env_vars['SIMULATOR_DOMAINS'])
        num_domains = num_pods * domains_per_pod

        def group_by_pod(df, ind, col):
            return int(int(df[col].loc[ind]) / domains_per_pod)

        print(file_name)
        duration = (float(env_vars['STOP_TIME']) - float(env_vars['START_TIME'])) / 60
        stats = [title, duration]
        stats.extend(region_size_stats(log_dataframe, title, save_plots, show_plots))
        # hashes_per_user_per_day(log_dataframe, title, save_plots, show_plots)
        # region_count_by_domain(log_dataframe, num_domains, num_pods, title, save_plots, show_plots)
        # # nondupe_vs_total_count_by_domain(log_dataframe, title, save_plots, show_plots)
        # # nondupe_vs_total_count_by_pod(log_dataframe, group_by_pod, title, save_plots, show_plots)
        # domain_stats = nondupe_vs_total_bytes_by_domain(log_dataframe, title, save_plots, show_plots)
        # pod_stats = nondupe_vs_total_bytes_by_pod(log_dataframe, group_by_pod, title, save_plots, show_plots)
        # stats.extend(domain_stats)
        # stats.extend(pod_stats)
        summary_results.append(stats)

    with open("summary.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(summary_results)


def main():
    process_directory('./ex0/', save_plots=False, show_plots=True)


if __name__ == "__main__":
    main()
