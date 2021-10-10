from front_end import SimpleAlgo
from back_end import BackendPod


def main():
    pod = BackendPod()
    simple = SimpleAlgo()
    stream = simple.get_input_stream()
    performance_metrics = map(simple.route_region, simple.create_regions)


if __name__ == "__main__":
    main()
