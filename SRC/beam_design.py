"""Beam design module for reinforced concrete beams.

This module provides a BeamDesign class that encapsulates the design procedures
for reinforced concrete beams. It handles flexural, shear, and sideface
reinforcement calculations based on given beam properties and design
requirements.

The module integrates with other components (beam, flexure, shear, and sideface)
to perform comprehensive beam design calculations.

Classes:
    BeamDesign: Main class for performing beam design calculations.
    BeamQuantities: Class for calculating material quantities
    of a designed beam.

Typical usage example:
    beam_data = beam.Beam(...)  # Create a Beam object with necessary properties
    design = BeamDesign(beam_data)
    design.calculate_flexural_design()
    design.calculate_shear_design()
    design.calculate_sideface_design()

    quantities = BeamQuantities(design)
    concrete_volume = quantities.conc_volume
    total_rebar_volume = quantities.total_rebar_volume
"""

import beam
import flexure
import shear
import sideface


class BeamDesign:
    """Inherit the Beam dataclass object and undertake design procedures.

    Attributes:
    flexural_design: Object encompassing flexural schedule attributes.
    shear_design: Object encompassing shear schedule attributes.
    sideface_design: Object encompassing shear schedule attributes.
    """

    def __init__(self, beam: beam.Beam) -> None:
        """Initialises the beam design object and inherits the beam dataclass.

        Args:
            beam (beam): Beam dataclass object.
        """
        self.beam = beam
        self.flexural_design: flexure.Flexure = flexure.Flexure(self.beam)
        self.shear_design: shear.Shear = shear.Shear(
            self.beam, self.flexural_design
        )
        self.sideface_design: sideface.Sideface = sideface.Sideface(
            self.beam, self.flexural_design, self.shear_design
        )

    def calculate_flexural_design(self) -> None:
        """Undertake flexural design.

        The order of operations for calculating the flexural rebar are as
        follows:
        1) The longitudinal rebar count is calculated based on the width (n-1)
        2) The flexural torsion requirement is split to the top and bottom
        flexural requirement if the depth is <= 700mm.
        3) The optimal flexural rebar schedule is derived.
        4) The flexural rebar feasibility is assessed based on span.
        5) The residual flexural rebar is derived to subtract from sideface
        requirements.
        """
        # Get the longitudinal rebar count.
        self.flexural_design.get_long_count()
        # Split the torsion reinforcement to the top and bottom rebar
        # if the depth <= 700mm.
        self.flexural_design.flex_torsion_splitting()
        # Obtain the required top and bottom flexural reinforcement.
        self.flexural_design.get_flex_rebar()
        # Check if the calculated rebar is feasible and alter it if not.
        self.flexural_design.assess_feasibility()
        # Calculate the residual rebar obtained from the provided rebar.
        self.flexural_design.get_residual_rebar()

    def calculate_shear_design(self) -> None:
        """Undertake shear design.

        The order of operations for calculating shear links are as
        follows:
        1) The shear links count is calculated based on the allowable codal
        transverse shear spacing.
        2) Total shear requirement is calculated based on codal requirements.
        3) The minimum longitudinal shear spacing is obtained based on codal
        requirements.
        4) The optimal shear links schedule is obtained.
        """
        # Calculate the required shear links count.
        self.shear_design.get_shear_links_count()
        # Get the total required shear reinforcement.
        self.shear_design.get_total_shear_req()
        # Get the minimum codal longitudinal shear spacing.
        self.shear_design.get_min_shear_spacing()
        # Obtain the shear links reinforcement.
        self.shear_design.get_shear_links()

    def calculate_sideface_design(self) -> None:
        """Undertake sideface design.

        The order of operations for calculating sideface rebar are as follows:
        1) The flexural torsion requirement is derived by subtracting the
        requirement by the flexural residual.
        2) The sideface clear space is calculated based on the maximum provided
        flexural and shear diameters.
        3) The optimal sideface schedule is obtained.
        """
        # Calculate the total required torsion reinforcement after residual.
        self.sideface_design.get_required_reinforcement()
        # Get the sideface clear space.
        self.sideface_design.get_sideface_clear_space()
        # Obtain the sideface reinforcement.
        self.sideface_design.get_sideface_rebar()


class BeamQuantities:
    """Calculate material quantities for a designed reinforced concrete beam.

    This class provides methods to calculate various quantities such as
    concrete volume, reinforcement areas, and volumes for a designed beam.

    Attributes:
        designed_beam (BeamDesign): The designed beam object.
        storey (str): The storey where the beam is located.
        etabs_id (str): The ETABS ID of the beam.
        span (float): The span of the beam.
        width (float): The width of the beam.
        depth (float): The depth of the beam.
    """

    def __init__(self, designed_beam: BeamDesign) -> None:
        """Initialize the BeamQuantities object.

        Args:
            designed_beam: A BeamDesign object representing the designed beam.
        """
        self.designed_beam: BeamDesign = designed_beam
        self.storey: str = self.designed_beam.beam.storey
        self.etabs_id: str = self.designed_beam.beam.etabs_id
        self.span: float = self.designed_beam.beam.span
        self.width: float = self.designed_beam.beam.width
        self.depth: float = self.designed_beam.beam.depth

    @property
    def conc_area(self) -> float:
        """Calculate the concrete cross-sectional area of the beam.

        Returns:
            The concrete cross-sectional area in square meters.
        """
        return (self.width * self.depth) * 10**-6

    @property
    def conc_volume(self) -> float:
        """Calculate the concrete volume of the beam.

        Returns:
            The concrete volume in cubic meters.
        """
        return round((self.conc_area * self.span) * 10**-3, 3)

    @property
    def flex_area(self) -> float:
        """Calculate the total flexural reinforcement area.

        Returns:
            The total flexural reinforcement area in square meters.
        """
        return round(
            (
                self.designed_beam.flexural_design.top_flex_rebar["left"][
                    "provided_reinf"
                ]
                + self.designed_beam.flexural_design.top_flex_rebar["middle"][
                    "provided_reinf"
                ]
                + self.designed_beam.flexural_design.top_flex_rebar["right"][
                    "provided_reinf"
                ]
                + self.designed_beam.flexural_design.bot_flex_rebar["left"][
                    "provided_reinf"
                ]
                + self.designed_beam.flexural_design.bot_flex_rebar["middle"][
                    "provided_reinf"
                ]
                + self.designed_beam.flexural_design.bot_flex_rebar["right"][
                    "provided_reinf"
                ]
            )
            * 10**-6,
            3,
        )

    @property
    def flex_volume(self) -> float:
        """Calculate the total flexural reinforcement volume.

        Returns:
            The total flexural reinforcement volume in cubic meters.
        """
        return round((self.flex_area * self.span) * 10**-3, 3)

    # TODO: Correct shear area.
    @property
    def shear_area(self) -> float:
        """Calculate the total shear reinforcement area.

        Returns:
            The total shear reinforcement area in square meters.
        """
        return round(
            (
                self.designed_beam.shear_design.shear_links["left"][
                    "provided_reinf"
                ]
                + self.designed_beam.shear_design.shear_links["middle"][
                    "provided_reinf"
                ]
                + self.designed_beam.shear_design.shear_links["right"][
                    "provided_reinf"
                ]
            )
            * 10**-6,
            3,
        )

    # TODO: Correct shear volume.
    @property
    def shear_volume(self) -> float:
        """Calculate the total shear reinforcement volume.

        Returns:
            The total shear reinforcement volume in cubic meters.
        """
        try:
            return round(
                (
                    self.designed_beam.shear_design.shear_links["left"][
                        "provided_reinf"
                    ]
                    * (self.span / 1000)
                    + self.designed_beam.shear_design.shear_links["middle"][
                        "provided_reinf"
                    ]
                    * (self.span / 1000)
                    + self.designed_beam.shear_design.shear_links["right"][
                        "provided_reinf"
                    ]
                    * (self.span / 1000)
                )
                * 10**-6,
                3,
            )
        except ZeroDivisionError:
            return 0

    @property
    def sideface_area(self) -> float:
        """Calculate the total sideface reinforcement area.

        Returns:
            The total sideface reinforcement area in square meters.
        """
        return (
            self.designed_beam.sideface_design.sideface_rebar["provided_reinf"]
            * 10**-6
        )

    @property
    def sideface_volume(self) -> float:
        """Calculate the total sideface reinforcement volume.

        Returns:
            The total sideface reinforcement volume in cubic meters.
        """
        return round((self.sideface_area * self.span) * 10**-3, 3)

    @property
    def total_rebar_area(self) -> float:
        """Calculate the total reinforcement area.

        Returns:
            The total reinforcement area in square meters.
        """
        return round(self.flex_area + self.shear_area + self.sideface_area, 3)

    @property
    def total_rebar_volume(self) -> float:
        """Calculate the total reinforcement volume.

        Returns:
            The total reinforcement volume in cubic meters.
        """
        return round(
            self.flex_volume + self.shear_volume + self.sideface_volume, 3
        )
