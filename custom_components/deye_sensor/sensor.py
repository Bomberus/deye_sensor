"""Sensor platform for deye_sensor."""
from __future__ import annotations

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription
from homeassistant.const import (
    DEVICE_CLASS_POWER,
    DEVICE_CLASS_ENERGY
)

from .const import DOMAIN, GENERATED_TODAY, ALARMS, CURRENT_POWER, GENERATED_TOTAL
from .coordinator import DeyeDataUpdateCoordinator
from .entity import DeyeIntegrationEntity

ENTITY_DESCRIPTIONS = (
    SensorEntityDescription(
        key=ALARMS,
        name="Operation Alarms",
        icon="mdi:alarm-light",
    ),
    SensorEntityDescription(
        key=CURRENT_POWER,
        device_class=DEVICE_CLASS_ENERGY,
        name="Operation Power",
        icon="mdi:power-plug",
    ),
    SensorEntityDescription(
        key=GENERATED_TODAY,
        device_class=DEVICE_CLASS_POWER,
        name="Operation Production (Today)",
        icon="mdi:solar-power",
    ),
    SensorEntityDescription(
        key=GENERATED_TOTAL,
        device_class=DEVICE_CLASS_POWER,
        name="Operation Production (Total)",
        icon="mdi:solar-power",
    ),
)


async def async_setup_entry(hass, entry, async_add_devices):
    """Set up the sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_devices(
        DeyeIntegrationSensor(
            coordinator=coordinator,
            entity_description=entity_description,
        )
        for entity_description in ENTITY_DESCRIPTIONS
    )


class DeyeIntegrationSensor(DeyeIntegrationEntity, SensorEntity):
    """deye_sensor Sensor class."""

    def __init__(
        self,
        coordinator: DeyeDataUpdateCoordinator,
        entity_description: SensorEntityDescription,
    ) -> None:
        """Initialize the sensor class."""
        super().__init__(coordinator)
        self.entity_description = entity_description

        self._attr_unique_id = (
            f"{coordinator.config_entry.entry_id}_{self.entity_description.key}"
        )

        # The name of the entity
        self._attr_name = f"deye_sensor {self.entity_description.key}"

    @property
    def native_value(self) -> float:
        """Return the native value of the sensor."""
        if self.coordinator.data.get(self.entity_description.key) is None:
            return 0.0

        return float(self.coordinator.data.get(self.entity_description.key))
