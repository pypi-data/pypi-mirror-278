import inspect
import json
from dataclasses import asdict, dataclass, field

READ_ONLY_FIELDS = set(["id"])


@dataclass
class TurbineModelSpecs:
    id: int = field(default=None)
    name: str = field(default=None)
    hub_height: float = field(default=None)
    rotor_diameter: float = field(default=None)
    rated_power: float = field(default=None)
    reference_density: float = field(default=None)
    reference_turbulence_intensity: float = field(default=None)
    reference_windspeed: list[float] = field(default=None)
    thrust_coefficient: list[float] = field(default=None)
    power: list[float] = field(default=None)
    public: bool = field(default_factory=bool)

    @classmethod
    def from_dict(cls, env):
        return cls(
            **{k: v for k, v in env.items() if k in inspect.signature(cls).parameters}
        )

    def _get_api_params(self):
        params = asdict(self)
        _ = [params.pop(key, None) for key in READ_ONLY_FIELDS]
        return params

    def __str__(self) -> str:
        return f"{self.__class__}:\n{json.dumps(asdict(self), indent=4)}"

    def __repr__(self) -> str:
        return json.dumps(asdict(self))
