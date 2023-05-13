class Strategy:
    def __init__(self, strategy_data: dict, file_path: str = "strategy.yaml") -> None:
        self.file = file_path
        self.strategy_data = strategy_data
        self.countries = []
        self.keywords = []
        self.sheet_id = None
        self.sheet_name = None
        self.limit = 50
        self.request_period = 2
        self.cooldown = 15

    def __enter__(self):
        if self.strategy_data:
            self.__load_startegy_data(data=self.strategy_data)
            return self
        return self

    def __exit__(self, exc_type, exc, tb):
        pass

    def __load_startegy_data(self, data: dict):
        configuration = data.get("configuration", {})
        self.sheet_id = configuration.get("sheet_id")
        self.sheet_name = configuration.get("sheet_name", "Linkedin_data")
        self.cooldown = configuration.get("cooldown")
        self.request_period = configuration.get("request_period")
        mapping = data.get("mapping", {})
        self.limit = mapping.get("limit")
        self.countries = mapping.get("countries", [])
        self.keywords = mapping.get("keywords", [])

    def generate_params_combo(self):
        for country in self.countries:
            for keyword in self.keywords:
                yield {"keywords": keyword, "location": country}
