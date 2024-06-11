import datetime
import inspect
import json
from dataclasses import asdict, dataclass, field

from whiffle_client.wind.components import Domain, Geometries, Metmast, Windfarm
from whiffle_client.wind.components.dates import Dates
from whiffle_client.wind.components.turbine import Turbine

READ_ONLY_FIELDS = set(
    [
        "id",
        "status",
        "messages",
        "creator",
        "created",
        "updated",
        "finished",
        "test_run",
        "price",
        "price_overview",
        "reference_number",
        "configuration_valid",
        "geometries",
        "domain",
        "progress",
    ]
)


@dataclass
class WindSimulationTask:
    # Metadata attributes
    id: str = field(default=None)
    status: str = field(default=None)
    messages: list[dict] = field(default=None)
    creator: dict = field(default=None)

    created: datetime.datetime = field(default=None)
    updated: datetime.datetime = field(default=None)
    finished: datetime.datetime = field(default=None)

    price: float = field(default=None)
    price_overview: dict = field(default=None)

    reference_number: str = field(default=None)
    reference_code: str = field(default=None)
    name: str = field(default=None)
    configuration_valid: bool = field(default=None)
    test_run: bool = field(default=None)

    # Time attributes
    dates: Dates = field(default=None)

    # Domain/object/geolocated elements attributes
    windfarms: list[Windfarm] = field(default_factory=list)
    geometries: Geometries = field(default=None)
    domain: Domain = field(default=None)
    metmasts: list[Metmast] = field(default_factory=list)
    metmasts_heights: list[float] = field(default_factory=list)

    # Output attributes
    wind_resource_grid_heights: list[float] = field(default_factory=list)
    fields_heights: list[float] = field(default_factory=list)

    progress: dict = field(default=None)

    @classmethod
    def from_dict(cls, env):
        return cls(
            **{k: v for k, v in env.items() if k in inspect.signature(cls).parameters}
        )

    def __post_init__(self):

        if isinstance(self.metmasts, list):
            self.metmasts = [
                Metmast(
                    name=metmast["name"],
                    longitude=metmast["longitude"],
                    latitude=metmast["latitude"],
                )
                for metmast in self.metmasts
            ]
        elif isinstance(self.metmasts, dict):
            self.metmasts = [
                Metmast(name=name, latitude=latitude, longitude=longitude)
                for name, (longitude, latitude) in zip(
                    self.metmasts["name"], self.metmasts["location"]
                )
            ]

        if isinstance(self.windfarms, list):
            self.windfarms = [Windfarm(**windfarm) for windfarm in self.windfarms]
        elif isinstance(self.windfarms, dict):
            self.windfarms = [
                Windfarm(
                    name=windfarm_name,
                    include_in_les=windfarm["include_in_les"],
                    thrust=windfarm["thrust"],
                    turbine_model_name=windfarm["turbine_model_name"],
                    turbines=[
                        Turbine(
                            name=name,
                            longitude=longitude,
                            latitude=latitude,
                        )
                        for name, (longitude, latitude) in zip(
                            windfarm["name"], windfarm["location"]
                        )
                    ],
                )
                for windfarm_name, windfarm in self.windfarms.items()
            ]

    def _get_api_params(self):
        params = asdict(self)
        _ = [params.pop(key, None) for key in READ_ONLY_FIELDS]

        if self.metmasts:
            params["metmasts"] = [
                {
                    "name": metmast.name,
                    "longitude": metmast.longitude,
                    "latitude": metmast.latitude,
                }
                for metmast in self.metmasts
            ]

        if self.windfarms:
            params["windfarms"] = [
                {
                    "name": windfarm.name,
                    "include_in_les": windfarm.include_in_les,
                    "thrust": windfarm.thrust,
                    "turbine_model_name": windfarm.turbine_model_name,
                    "turbines": [
                        {
                            "name": turbine.name,
                            "longitude": turbine.longitude,
                            "latitude": turbine.latitude,
                        }
                        for turbine in windfarm.turbines
                    ],
                }
                for windfarm in self.windfarms
            ]

        return params

    def __str__(self) -> str:
        return f"{self.__class__}:\n{json.dumps(asdict(self), indent=4)}"

    def __repr__(self) -> str:
        return json.dumps(asdict(self))
