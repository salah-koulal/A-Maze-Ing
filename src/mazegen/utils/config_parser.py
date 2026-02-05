from typing import Dict, Any, Optional, Tuple


class ConfigParser:
    """Parse and validate maze configuration files."""
    REQUIRED_KEYS = [
        "WIDTH",
        "HEIGHT",
        "ENTRY",
        "EXIT",
        "OUTPUT_FILE",
        "PERFECT"
    ]

    def __init__(self, filepath: str) -> None:
        """
        Initialize the config parser.

        Args:
            filepath: Path to the configuration file
        """
        self.filepath = filepath
        self.config: Dict[str, Any] = {}

    def _parse_line(self, line: str) -> Optional[Tuple[str, str]]:
        """
        Parse a single line from the config file.

        Args:
            line: A single line from the file

        Returns:
            Tuple of (key, value) or None if line should be ignored
        """
        line = line.strip()
        if not line or line.startswith("#"):
            return None
        values = line.split("=")
        if len(values) != 2:
            return None
        return (values[0].strip(), values[1].strip())

    def _validate_config(self) -> None:
        for required_key in self.REQUIRED_KEYS:
            if required_key not in self.config:
                raise ValueError(f"Missing required key: {required_key}")
        return None

    def _convert_types(self) -> None:
        self.config["WIDTH"] = int(self.config["WIDTH"])
        self.config["HEIGHT"] = int(self.config["HEIGHT"])
        entry_parts = self.config["ENTRY"].split(",")
        if len(entry_parts) != 2:
            raise ValueError("Entry must be in format 'x,y'")
        self.config["ENTRY"] = (int(entry_parts[0]), int(entry_parts[1]))

        exit_parts = self.config["EXIT"].split(",")
        if len(exit_parts) != 2:
            raise ValueError("Exit must be in format 'x,y'")
        self.config["EXIT"] = (int(exit_parts[0]), int(exit_parts[1]))

        self.config["PERFECT"] = self.config["PERFECT"] == "True"

        if "SEED" in self.config:
            self.config["SEED"] = int(self.config["SEED"])

    def _validate_values(self) -> None:
        if self.config["WIDTH"] <= 8 or self.config["HEIGHT"] <= 8:
            raise ValueError("Maze too small for '42' pattern!")
        entry_x, entry_y = self.config["ENTRY"]

        if not (0 <= entry_x < self.config["WIDTH"] and
                0 <= entry_y < self.config["HEIGHT"]):
            raise ValueError("ENTRY coordinates out of bounds")
        exit_x, exit_y = self.config["EXIT"]

        if not (0 <= exit_x < self.config["WIDTH"] and
                0 <= exit_y < self.config["HEIGHT"]):
            raise ValueError("EXIT coordinates out of bounds")

        if self.config["ENTRY"] == self.config["EXIT"]:
            raise ValueError("ENTRY and EXIT must be different")

    def parse(self) -> Dict[str, Any]:
        """
        Parse the configuration file.

        Returns:
            Dictionary containing parsed configuration
        """
        with open(self.filepath) as f:
            for line in f:
                result = self._parse_line(line)
                if result:
                    key, value = result
                    self.config[key] = value

        self._validate_config()
        self._convert_types()
        self._validate_values()
        return self.config


def get_default_config() -> Dict[str, Any]:
    """Return a default configuration."""
    return {
        "WIDTH": 21,
        "HEIGHT": 15,
        "ENTRY": (0, 0),
        "EXIT": (20, 14),
        "OUTPUT_FILE": "maze_output.txt",
        "PERFECT": True,
        "SEED": 42
    }


def load_config(filepath: Optional[str] = None) -> Dict[str, Any]:
    """
    Load and parse a configuration file or return defaults.

    Args:
        filepath: Path to the configuration file (optional)

    Returns:
        Dictionary containing parsed configuration
    """
    if filepath is None:
        return get_default_config()

    parser = ConfigParser(filepath)
    return parser.parse()
