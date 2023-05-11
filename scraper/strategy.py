from yaml import safe_dump, safe_load


class Strategy:
    def __init__(self, file_path: str = "strategy.yaml") -> None:
        self.file = file_path
        self.countries = []
        self.keywords = []
        self.sheet_id = None
        self.limit = 50
        self.request_period = 2
        self.cooldown = 15

    def __import_startegy(self):
        with open(self.file, "r") as strat_file:
            strategy: dict = safe_load(strat_file)
        # verify valid input
        self.sheet_id = strategy.get("sheet_id")
        mapping = strategy.get("mapping", {})
        self.countries = mapping.get("countries", [])
        self.keywords = mapping.get("keywords", [])

    def _update_startegy_file(self):
        with open(self.file, "w") as strat_file:
            mapping = dict(
                countries=self.countries,
                keywords=self.keywords,
            )
            config = dict(google_sheet_id=self.sheet_id)
            safe_dump({"mapping": mapping, "configuration": config}, strat_file)

    def generate_params_combo(self):
        self.__import_startegy()
        for country in self.countries:
            for keyword in self.keywords:
                yield {"keywords": keyword, "location": country}
