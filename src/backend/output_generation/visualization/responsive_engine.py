"""Responsive visualization engine."""

from __future__ import annotations

from .enums import ViewportBreakpoint
from .responsive import ResponsiveBreakpoint, ResponsiveConfiguration


class ResponsiveEngine:
    """Build responsive breakpoint configuration for visualization surfaces."""

    def default_configuration(self) -> ResponsiveConfiguration:
        return ResponsiveConfiguration(
            breakpoints={
                "desktop": ResponsiveBreakpoint(breakpoint=ViewportBreakpoint.DESKTOP, max_width=1440),
                "tablet": ResponsiveBreakpoint(breakpoint=ViewportBreakpoint.TABLET, max_width=1024),
                "mobile": ResponsiveBreakpoint(breakpoint=ViewportBreakpoint.MOBILE, max_width=640),
            }
        )


__all__ = ["ResponsiveEngine"]
