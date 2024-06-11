from dataclasses import dataclass, field

from whiffle_client.wind.components.turbine import Turbine


@dataclass
class Windfarm:
    name: str = field(default=None)
    turbines: list[Turbine] = field(default=None)
    include_in_les: bool = field(default=True)
    thrust: bool = field(default=True)
    turbine_model_name: str = field(default=None)
