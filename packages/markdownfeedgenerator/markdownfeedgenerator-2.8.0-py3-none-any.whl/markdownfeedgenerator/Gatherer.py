from concurrent.futures import ThreadPoolExecutor


class Gatherer:
    """
    Wrapper class to group feeds and run them in parallel.
    """

    def __init__(
        self,
        generators: list = None
    ):
        """
        Provide a list of feed generators.
        """
        if generators is None:
            generators = []

        self.generators = generators

    def generate(
        self
    ):
        """
        Generate all the feeds in parallel.
        """
        with ThreadPoolExecutor() as ex:
            futures = [ex.submit(generator.run_standalone) for generator in self.generators]

        [future.result() for future in futures]
