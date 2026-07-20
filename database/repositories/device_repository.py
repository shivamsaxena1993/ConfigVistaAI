"""
====================================================================
File: device_repository.py

Project : ConfigVista AI

Purpose
-------
Repository for Device-specific database operations.

====================================================================
"""

from typing import List, Optional

from sqlalchemy import or_

from database.models import Device
from database.repositories.base_repository import BaseRepository


class DeviceRepository(BaseRepository[Device]):

    def __init__(self, session):
        super().__init__(session, Device)

    # ----------------------------------------------------------
    # Get Device by Hostname
    # ----------------------------------------------------------

    def get_by_hostname(self, hostname: str) -> Optional[Device]:

        return (
            self.session.query(Device)
            .filter(Device.hostname == hostname)
            .first()
        )

    # ----------------------------------------------------------
    # Get Devices by Site
    # ----------------------------------------------------------

    def get_by_site(self, site: str) -> List[Device]:

        return (
            self.session.query(Device)
            .filter(Device.site == site)
            .all()
        )

    # ----------------------------------------------------------
    # Get Devices by Vendor
    # ----------------------------------------------------------

    def get_by_vendor(self, vendor: str) -> List[Device]:

        return (
            self.session.query(Device)
            .filter(Device.vendor == vendor)
            .all()
        )

    # ----------------------------------------------------------
    # Get Devices by Environment
    # ----------------------------------------------------------

    def get_by_environment(self, environment: str) -> List[Device]:

        return (
            self.session.query(Device)
            .filter(Device.environment == environment)
            .all()
        )

    # ----------------------------------------------------------
    # Get Active Devices
    # ----------------------------------------------------------

    def get_active_devices(self) -> List[Device]:

        return (
            self.session.query(Device)
            .filter(Device.status == "Active")
            .all()
        )

    # ----------------------------------------------------------
    # Get Critical Devices
    # ----------------------------------------------------------

    def get_critical_devices(self) -> List[Device]:

        return (
            self.session.query(Device)
            .filter(Device.criticality == "High")
            .all()
        )

    # ----------------------------------------------------------
    # Search Devices
    # ----------------------------------------------------------

    def search_devices(self, keyword: str) -> List[Device]:

        keyword = f"%{keyword}%"

        return (
            self.session.query(Device)
            .filter(
                or_(
                    Device.hostname.like(keyword),
                    Device.vendor.like(keyword),
                    Device.model.like(keyword),
                    Device.site.like(keyword),
                    Device.environment.like(keyword)
                )
            )
            .all()
        )

    # ----------------------------------------------------------
    # Check Hostname Exists
    # ----------------------------------------------------------

    def hostname_exists(self, hostname: str) -> bool:

        return self.get_by_hostname(hostname) is not None