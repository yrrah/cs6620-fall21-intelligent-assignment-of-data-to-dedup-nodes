import numpy as np
from matplotlib import pyplot as plt


def region_count_by_domain(df, num_domains, num_pods, title, save, show):
    domains_per_pod = int(num_domains/num_pods)
    selected = df[['domain', ' non-dupe fp count']].copy()
    selected = selected.groupby(['domain']).count()
    domain_counts = np.zeros(num_domains)
    for domain in selected.index:
        domain_counts[domain] = selected[' non-dupe fp count'][domain]

    domain_grid = domain_counts.reshape((num_pods, domains_per_pod))
    domain_grid = np.repeat(domain_grid, int(domains_per_pod/num_pods), axis=0)
    fig, ax = plt.subplots()
    im = ax.imshow(domain_grid, cmap='nipy_spectral')
    fig.colorbar(im, ax=ax)
    ax.set_yticklabels([])
    ax.set_ylabel('Pods')
    ax.set_xlabel('Domains per Pod')
    ax.set_title(f'Total Regions sent to each Domain ({title})')
    # selected.index = selected.index.astype(int)
    # if save or show:
    #     ax = selected.plot.bar(stacked=True)
    #     ax.set_title(title)
    #     ax.set_ylabel('Count of Fingerprints per Domain')
    #     ax.set_xticks(ax.get_xticks()[::64])
    #     # ax.set_ylim(10, 2500000000)
    if save:
        plt.savefig(f'{title}_region_count_by_domain.png')
    if show:
        plt.show()
    pass


def nondupe_vs_total_count_by_domain(df, title, save, show):
    selected = df[['domain', ' non-dupe fp count']].copy()
    selected['total region fp count'] = df[' region fp count'] - selected[' non-dupe fp count']
    selected = selected.groupby(['domain']).sum()
    selected.index = selected.index.astype(int)
    if save or show:
        ax = selected.plot.bar(stacked=True)
        ax.set_title(title)
        ax.set_ylabel('Count of Fingerprints per Domain')
        ax.set_xticks(ax.get_xticks()[::64])
        # ax.set_ylim(10, 2500000000)
    if save:
        plt.savefig(f'{title}_nondupe_vs_total_count_by_domain.png')
    if show:
        plt.show()


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


def nondupe_vs_total_bytes_by_domain(df, title, save, show) -> [float]:
    selected = df[['domain', ' non-dupe bytes']].copy()
    selected['total region bytes'] = df[' region bytes'] - selected[' non-dupe bytes']
    by_domain = selected.groupby(['domain']).sum()
    by_domain[' region bytes'] = by_domain['total region bytes'] + by_domain[' non-dupe bytes']
    by_domain.index = by_domain.index.astype(int)
    max_value = by_domain[' region bytes'].max()
    if save or show:
        ax = by_domain[[' non-dupe bytes', 'total region bytes']].plot.bar(stacked=True, logy=True)
        ax.set_title(title)
        ax.set_ylabel('Total Bytes sent to Domain')
        ax.set_xticks(ax.get_xticks()[::64])
        ax.set_ylim(0, max_value)
    print(f"{title} {by_domain['total region bytes'].min()}")
    if save:
        plt.savefig(f'{title}_nondupe_vs_total_bytes_by_domain.png')
    if show:
        plt.show()
    mean_domain_phys = by_domain[' non-dupe bytes'].mean()
    std_domain_phys = by_domain[' non-dupe bytes'].std()
    min_domain_phys = by_domain[' non-dupe bytes'].min()
    max_domain_phys = by_domain[' non-dupe bytes'].max()
    mean_domain_logical = by_domain[' region bytes'].mean()
    std_domain_logical = by_domain[' region bytes'].std()
    min_domain_logical = by_domain[' region bytes'].min()
    max_domain_logical = by_domain[' region bytes'].max()
    overall_dedup = (by_domain[' region bytes'].sum() / selected[' non-dupe bytes'].sum()).round(1)
    stats = [overall_dedup, mean_domain_phys, std_domain_phys, min_domain_phys, max_domain_phys,
             mean_domain_logical, std_domain_logical, min_domain_logical, max_domain_logical]
    return stats


def nondupe_vs_total_bytes_by_pod(df, group_by_func, title, save, show) -> [float]:
    selected = df[['domain', ' non-dupe bytes']].copy()
    selected['total region bytes'] = df[' region bytes'] - selected[' non-dupe bytes']
    by_pod = selected.groupby(lambda x: group_by_func(selected, x, 'domain')).sum()
    by_pod[' region bytes'] = by_pod['total region bytes'] + by_pod[' non-dupe bytes']
    by_pod['ratio'] = (by_pod[' region bytes'] / by_pod[' non-dupe bytes']).round(1)
    max_value = by_pod[' region bytes'].max()
    if save or show:
        ax = by_pod[[' non-dupe bytes', 'total region bytes']].plot.bar(stacked=True)
        ax.set_title(title)
        ax.set_xlabel('Pod')
        ax.set_ylabel('Total Bytes sent to Pod')
        ax.set_ylim(0, max_value)
        for i, v in enumerate(by_pod['ratio']):
            ax.annotate(f'{v}X', (i - 0.2, max_value/2), fontsize=10)
    if save:
        plt.savefig(f'{title}_nondupe_vs_total_bytes_by_pod.png')
    if show:
        plt.show()

    mean_pod_phys = by_pod[' non-dupe bytes'].mean()
    std_pod_phys = by_pod[' non-dupe bytes'].std()
    min_pod_phys = by_pod[' non-dupe bytes'].min()
    max_pod_phys = by_pod[' non-dupe bytes'].max()
    mean_pod_logical = by_pod[' region bytes'].mean()
    std_pod_logical = by_pod[' region bytes'].std()
    min_pod_logical = by_pod[' region bytes'].min()
    max_pod_logical = by_pod[' region bytes'].max()
    stats = [mean_pod_phys, std_pod_phys, min_pod_phys, max_pod_phys,
             mean_pod_logical, std_pod_logical, min_pod_logical, max_pod_logical]
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