import json
from dataclasses import InitVar, asdict, dataclass, field
from pathlib import Path

import pandas as pd


def csv_loader_constructor(base_dir=None):
    def csv_loader(loader, node):
        path = loader.construct_scalar(node)
        if base_dir is not None:
            path = f"{Path(base_dir).resolve()}/{path}"
        return asdict(CSVLoader(path_to_csv=path))

    return csv_loader


@dataclass
class CSVLoader:
    # Init attributes
    path_to_csv: InitVar[str] = ""

    # Postinit attributes
    name: str = field(default=None)
    location: list[list[float]] = field(default=None)
    turbine_model_name: str = field(default=None)
    include_in_les: bool = field(default=True)
    thrust: bool = field(default=True)

    def __post_init__(self, path_to_csv: str = ""):
        self.data = pd.read_csv(path_to_csv).to_dict(orient="list")
        self.name = self.data["name"]
        self.location = list(zip(self.data["lon"], self.data["lat"]))
        self.turbine_model_name = self.data["type"][0]

    def __repr__(self):
        return_data = {
            "name": self.name,
            "location": self.location,
        }
        if self.turbine_model_name != "metmast":
            return_data.update({"turbine_model_name": self.turbine_model_name})

        return json.dumps(return_data)

    def __getitem__(self, item):
        return getattr(self, item)
