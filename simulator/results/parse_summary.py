import pandas as pd
import numpy as np
from matplotlib import pyplot as plt


def plot_reversed(ax, save, show, title):
    # ax.set_xticklabels(df.run_combo, rotation = 90)
    ax.yaxis.tick_right()
    ax.yaxis.set_label_position("right")
    ax.invert_xaxis()
    plt.gcf().subplots_adjust(right=0.5)
    # plt.tight_layout()
    if save:
        plt.savefig(f'{title}.svg', format='svg')
    if show:
        plt.show()


def plot_times(df, dataset: int, save, show):
    df['run_combo'] = df['run_combo'].str[20:]
    ax = df[(df['dataset'] == dataset) & (df['domains_per_pod'] == 32)] \
        .sort_values(['region_size', 'duration'], ascending=False) \
        .plot.barh(x='run_combo', y='duration', figsize=(12, 10))
    ax.set_title(f'Dataset {dataset} Processing Time')
    ax.set_xlabel('Minutes')
    ax.get_legend().remove()
    plot_reversed(ax, save, show, f'dataset{dataset}_duration')


def plot_regions(df, save, show):
    df['run_combo'] = 'Data' + df['dataset'].astype(str) + ', ' + df['region_size'].astype(str) + 'MB ' + df['region_algo']
    ax = df[(df['assign_algo'] == 'MIN_FINGERPRINT') & (df['domains_per_pod'] == 32)] \
        .sort_values(['mean_region_bytes'], ascending=False) \
        .plot.barh(x='run_combo',
                   y=['min_region_bytes', 'max_region_bytes', 'mean_region_bytes', 'std_region_bytes'],
                   figsize=(10, 4))
    ax.set_title(f'Region Creation')
    ax.axvline(x=4*1024*1024)
    ax.axvline(x=8*1024*1024)
    ax.set_xticks([n*1024*1024 for n in range(0, 13, 2)])
    ax.set_xticklabels([f'{n}MB' for n in range(0, 13, 2)])
    plot_reversed(ax, save, show, 'region_creation_stats')


def plot_dedup(df, dataset: int, save, show):
    ax = df[(df['dataset'] == dataset)] \
        .sort_values(['overall_dedup'], ascending=False) \
        .plot.barh(x='run_combo', y='overall_dedup', figsize=(12, 20))
    ax.set_title(f'Dataset {dataset} Overall De-duplication')
    # ax.set_xlabel('Minutes')
    # ax.get_legend().remove()
    plot_reversed(ax, save, show, f'dataset{dataset}_deduplication')


def plot_skew(df, dataset: int, save, show):
    df['q_label'] = 'Data' + df['dataset'].astype(str) + ', ' + (df['domains_per_pod'] * df['num_pods']).astype(
        str) + ' domains, ' + df['region_algo'] + ', ' + df['assign_algo']
    df['run_combo'] = df['run_combo'].str[:-18]
    ax = df[(df['dataset'] == dataset) & (df['assign_algo'] == 'MAX_FINGERPRINT') & (df['q_learning'] != 'w/Q')] \
        .sort_values(['domains_per_pod'], ascending=False).set_index('q_label') \
        .plot.barh(x='run_combo', y='std_pod_phys', figsize=(10, 5))
    ax.set_title(f'Dataset {dataset} Pod Physical Skew 4MB vs 8MB')
    ax.set_xlabel('Bytes')
    ax.get_legend().remove()
    plot_reversed(ax, save, show, f'dataset{dataset}_pod_phys_skew')


def plot_skew_scatter(df, dataset: int, column: str, cv=False):
    std_col = f'std_{column}'
    mean_col = f'mean_{column}'
    if cv:
        std_col_cv = f'{std_col}_cv'
        df[std_col_cv] = df[std_col] / df[mean_col]
        std_col = std_col_cv
    df['color'] = np.where(df['q_learning'] == 'w/Q', 'red', 'blue')
    df['q_label'] = 'Data' + df['dataset'].astype(str) + ', ' + (df['domains_per_pod'] * df['num_pods']).astype(
        str) + ' domains, ' + df['region_size'].astype(str) + 'MB ' + df['region_algo'] + ', ' + \
        df['assign_algo']
    filtered = df[(df['dataset'] == dataset) & (df['region_size'] == 4)]
    filtered = filtered.groupby('q_label').filter(lambda x: len(x) >= 2)
    filtered = filtered.sort_values(['run_combo'], ascending=False)
    ax = filtered.plot.scatter(x='overall_dedup', y=std_col, figsize=(12, 8), color=filtered['color'])
    # annotate points in axis
    for idx, row in filtered.iterrows():
        ax.annotate((str(row['run_num']) + row['q_learning'] + row['eps'] + row['q_penalty']), (row['overall_dedup'], row[std_col]))

    grouped = filtered.groupby('q_label')
    for label, df in grouped:
        df.plot(x='overall_dedup', y=std_col, ax=ax, label=label)
    return ax


def plot_pod_skew_logical_scatter(df, dataset: int, save, show):
    ax = plot_skew_scatter(df, dataset, 'pod_logical')
    ax.set_title(f'Dataset {dataset} Overall Pod Logical Skew')
    ax.set_xlabel('Overall Deduplication (----> More is Better)')
    ax.set_ylabel('(<---- Less is Better) Standard Deviation of Total Pod Logical Bytes')
    if save:
        plt.savefig(f'dataset{dataset}_pod_skew_logical_scatter.svg', format='svg')
    if show:
        plt.show()


def plot_pod_skew_physical_scatter(df, dataset: int, save, show):
    ax = plot_skew_scatter(df, dataset, 'pod_phys')
    ax.set_title(f'Dataset {dataset} Overall Pod Physical Skew')
    ax.set_xlabel('Overall Deduplication (----> More is Better)')
    ax.set_ylabel('(<---- Less is Better) Standard Deviation of Total Pod Physical Bytes')
    if save:
        plt.savefig(f'dataset{dataset}_pod_skew_physical_scatter.svg', format='svg')
    if show:
        plt.show()


def summary_plots(file_name: str, save, show):
    df = pd.read_csv(file_name)
    df['q_learning'] = np.where(df['q_learning'] == 'True', 'w/Q', '')
    df['q_penalty'] = np.where(df['q_penalty'] == 'True', '+penalty', '')
    df['eps'] = np.where(df['epsilon'] == '1', '+random', '')
    df['run_combo'] = 'Data' + df['dataset'].astype(str) + ', ' + (df['domains_per_pod'] * df['num_pods']).astype(
        str) + ' domains, ' + df['region_size'].astype(str) + 'MB ' + df['region_algo'] + ', ' + \
        df['assign_algo'] + ' ' + df['q_learning'] + df['eps'] + df['q_penalty']

    # plot_times(df.copy(), 1, save, show)
    # plot_times(df.copy(), 2, save, show)
    # plot_times(df.copy(), 3, save, show)
    # plot_regions(df.copy(), save, show)
    # plot_dedup(df.copy(), 1, save, show)
    # plot_dedup(df.copy(), 1, save, show)
    # plot_dedup(df.copy(), 3, save, show)
    # plot_pod_skew_logical_scatter(df.copy(), 1, save, show)
    # plot_pod_skew_logical_scatter(df.copy(), 2, save, show)
    # plot_pod_skew_logical_scatter(df.copy(), 3, save, show)
    # plot_pod_skew_physical_scatter(df.copy(), 1, save, show)
    # plot_pod_skew_physical_scatter(df.copy(), 2, save, show)
    # plot_pod_skew_physical_scatter(df.copy(), 3, save, show)
    plot_skew(df.copy(), 1, save, show)


def main():
    summary_plots('./summary/combined_summary_stats.csv', save=False, show=True)


if __name__ == "__main__":
    main()
