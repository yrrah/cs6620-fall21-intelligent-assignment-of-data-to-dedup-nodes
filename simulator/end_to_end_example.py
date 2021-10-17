import os

from tqdm import tqdm

from simulator.back_end.src.back_end.kv_store.store import KeyValueStore
from simulator.front_end.src.front_end.region_creation.fixed_region import create_fixed_regions
from simulator.front_end.src.front_end.region_creation.input_streams import HashFile
import matplotlib.pyplot as plt

from simulator.front_end.src.front_end.routing.simple_algo import simple_routing


def main():
    num_domains = 10
    max_files = 10
    hash_file_dir = './hash_files/'
    domains = [KeyValueStore() for _ in range(num_domains)]

    hash_files = [file for file in os.listdir(hash_file_dir) if file.endswith(".hash.anon")]
    num_files = len(hash_files)

    domain_total_received = [0 for _ in range(num_domains)]
    total_overall = 0

    for filename in tqdm(hash_files[:min(max_files, num_files)]):
        hash_file = HashFile(hash_file_dir + filename)
        for region in create_fixed_regions(hash_file, size_mib=1):
            destination = simple_routing(region, num_domains)
            unique_bytes, unique_fingerprints = domains[destination].add_region(region)
            domain_total_received[destination] += len(region.fingerprints)
            total_overall += len(region.fingerprints)

    dedup = [0.0 for _ in range(num_domains)]
    counts = [0.0 for _ in range(num_domains)]
    for i in range(num_domains):
        if domain_total_received[i] > 0:
            dedup[i] = domains[i].get_current_count()/domain_total_received[i]
        counts[i] = domain_total_received[i]/total_overall

    # counts = [domain.get_current_count()/total_overall for domain in domains]

    x_pos = [i for i, _ in enumerate(counts)]

    fig, ax = plt.subplots()
    ax.bar(x_pos, counts, color='green')
    ax.set_xlabel("Domains")
    ax.set_ylabel("Percent of Total Fingerprints Assigned")
    ax.set_title("Fingerprint Distribution")
    fig.savefig('end_to_end_example_counts.png')
    plt.close(fig)

    fig, ax = plt.subplots()
    ax.bar(x_pos, dedup, color='green')
    ax.set_xlabel("Domains")
    ax.set_ylabel("Compression Ratio")
    ax.set_title("Stored Fingerprints/Total Fingerprints per Domain")
    fig.savefig('end_to_end_example_dedup.png')
    plt.close(fig)


if __name__ == "__main__":
    main()
