from abc import ABC, abstractmethod
from typing import Dict

class AppSettings(ABC):
    """Base class for chat settings history storage."""

    @abstractmethod
    def get_settings(self) -> Dict:
        """Retrieve the settings."""
        pass

    @abstractmethod
    def update_settings(self, settings: Dict) -> None:
        """Update the settings."""
        pass

    @abstractmethod
    def clear_settings(self) -> None:
        """Clear the settings."""
        pass

    @abstractmethod
    def set_setting(self) -> None:
        """Set the a settings."""
        pass