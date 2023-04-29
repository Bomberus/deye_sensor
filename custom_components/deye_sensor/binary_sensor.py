"""Binary sensor platform for deye_sensor."""
from __future__ import annotations

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)

from .const import DOMAIN, POWERED_ON
from .coordinator import DeyeDataUpdateCoordinator
from .entity import DeyeIntegrationEntity

ENTITY_DESCRIPTIONS = (
    BinarySensorEntityDescription(
        key="deye_isproducing_sensor",
        name="Inverter is online",
        device_class=BinarySensorDeviceClass.CONNECTIVITY,
    ),
)


async def async_setup_entry(hass, entry, async_add_devices):
    """Set up the binary_sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_devices(
        DeyeIntegrationBinarySensor(
            coordinator=coordinator,
            entity_description=entity_description,
        )
        for entity_description in ENTITY_DESCRIPTIONS
    )


class DeyeIntegrationBinarySensor(DeyeIntegrationEntity, BinarySensorEntity):
    """deye_sensor binary_sensor class."""

    def __init__(
        self,
        coordinator: DeyeDataUpdateCoordinator,
        entity_description: BinarySensorEntityDescription,
    ) -> None:
        """Initialize the binary_sensor class."""
        super().__init__(coordinator)
        self.entity_description = entity_description

    @property
    def is_on(self) -> bool:
        """Return true if the binary_sensor is on."""
        return self.coordinator.data.get(POWERED_ON)
