from front_end import SimpleAlgo
from back_end import BackendPod
from simulator.region_creation.fixed_region import hex_string_to_int


def main():
    pod = BackendPod()
    simple = SimpleAlgo()
    stream = simple.get_input_stream()
    performance_metrics = map(simple.route_region, simple.create_regions)


if __name__ == "__main__":
    print(hex_string_to_int("3f:8d:1a:35:a8:ff"))
