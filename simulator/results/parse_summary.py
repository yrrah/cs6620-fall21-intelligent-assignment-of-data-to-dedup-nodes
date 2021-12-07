import pandas as pd
import numpy as np
from matplotlib import pyplot as plt


def plot_reversed(ax):
    # ax.set_xticklabels(df.run_combo, rotation = 90)
    ax.yaxis.tick_right()
    ax.yaxis.set_label_position("right")
    ax.invert_xaxis()
    plt.gcf().subplots_adjust(right=0.5)
    # plt.tight_layout()
    plt.show()


def plot_times(df, dataset: int):
    df['run_combo'] = df['run_combo'].str[20:]
    ax = df[(df['dataset'] == dataset) & (df['domains_per_pod'] == 32)] \
        .sort_values(['region_size', 'duration'], ascending=False) \
        .plot.barh(x='run_combo', y='duration', figsize=(12, 10))
    ax.set_title(f'Dataset {dataset} Processing Time')
    ax.set_xlabel('Minutes')
    ax.get_legend().remove()
    plot_reversed(ax)


def plot_regions(df):
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
    plot_reversed(ax)


def summary_plots(file_name: str):
    df = pd.read_csv(file_name)
    df['q_learning'] = np.where(df['q_learning'] == 'True', 'w/Q', '')
    df['q_penalty'] = np.where(df['q_penalty'] == 'True', '+penalty', '')
    df['eps'] = np.where(df['epsilon'] == '1', '+random', '')
    df['run_combo'] = 'Data' + df['dataset'].astype(str) + ', ' + (df['domains_per_pod'] * df['num_pods']).astype(
        str) + ' domains, ' + df['region_size'].astype(str) + 'MB ' + df['region_algo'] + ', ' + \
        df['assign_algo'] + ' ' + df['q_learning'] + df['eps'] + df['q_penalty']

    # plot_times(df.copy(), 1)
    # plot_times(df.copy(), 2)
    # plot_times(df.copy(), 3)
    # plot_regions(df)


def main():
    summary_plots('combined_summary_stats.csv')


if __name__ == "__main__":
    main()
