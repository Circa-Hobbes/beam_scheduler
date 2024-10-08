"""Module for creating and manipulating beam schedule dataframes.

This module provides functionality to generate a structured DataFrame
representing a beam schedule with various properties and reinforcement details.
"""

import pandas as pd


def get_beam_table() -> tuple[pd.DataFrame, pd.DataFrame]:
    """Create and return an empty DataFrame for a beam schedule.

    The DataFrame is structured with a MultiIndex column setup to represent
    various beam properties including dimensions, reinforcement details,
    and design criteria.

    Returns:
        pd.DataFrame: An empty DataFrame with a predefined column structure
        for a beam schedule.
    """
    # Create dataframe to fill data with.
    columns = pd.MultiIndex.from_tuples(
        [
            ("Storey", ""),
            ("Etabs ID", ""),
            ("Span (mm)", ""),
            ("Dimensions", "Width (mm)"),
            ("Dimensions", "Depth (mm)"),
            ("Bottom Reinforcement", "Left (BL)"),
            ("Bottom Reinforcement", "Middle (B)"),
            ("Bottom Reinforcement", "Right (BR)"),
            ("Top Reinforcement", "Left (TL)"),
            ("Top Reinforcement", "Middle (T)"),
            ("Top Reinforcement", "Right (TR)"),
            ("Side Face Reinforcement", ""),
            ("Shear links", "Left (H)"),
            ("Shear links", "Middle (J)"),
            ("Shear links", "Right (K)"),
            ("Flexural BL Criteria", "Required (mm^2)"),
            ("Flexural BL Criteria", "Provided (mm^2)"),
            ("Flexural BL Criteria", "Utilization (%)"),
            ("Flexural BM Criteria", "Required (mm^2)"),
            ("Flexural BM Criteria", "Provided (mm^2)"),
            ("Flexural BM Criteria", "Utilization (%)"),
            ("Flexural BR Criteria", "Required (mm^2)"),
            ("Flexural BR Criteria", "Provided (mm^2)"),
            ("Flexural BR Criteria", "Utilization (%)"),
            ("Flexural TL Criteria", "Required (mm^2)"),
            ("Flexural TL Criteria", "Provided (mm^2)"),
            ("Flexural TL Criteria", "Utilization (%)"),
            ("Flexural TM Criteria", "Required (mm^2)"),
            ("Flexural TM Criteria", "Provided (mm^2)"),
            ("Flexural TM Criteria", "Utilization (%)"),
            ("Flexural TR Criteria", "Required (mm^2)"),
            ("Flexural TR Criteria", "Provided (mm^2)"),
            ("Flexural TR Criteria", "Utilization (%)"),
            ("Sideface Criteria", "Required (mm^2)"),
            ("Sideface Criteria", "Provided (mm^2)"),
            ("Sideface Criteria", "Utilization (%)"),
            ("Shear L Criteria", "Required (mm^2)"),
            ("Shear L Criteria", "Provided (mm^2)"),
            ("Shear L Criteria", "Utilization (%)"),
            ("Shear M Criteria", "Required (mm^2)"),
            ("Shear M Criteria", "Provided (mm^2)"),
            ("Shear M Criteria", "Utilization (%)"),
            ("Shear R Criteria", "Required (mm^2)"),
            ("Shear R Criteria", "Provided (mm^2)"),
            ("Shear R Criteria", "Utilization (%)"),
        ]
    )
    quantities = {
        "Storey": None,
        "Etabs ID": None,
        "Span (mm)": None,
        "Width (mm)": None,
        "Depth (mm)": None,
        "Concrete Area (m^2)": None,
        "Concrete Volume (m^3)": None,
        "Flexural Rebar Area (m^2)": None,
        "Flexural Rebar Volume (m^3)": None,
        "Shear Rebar Area (m^2)": None,
        "Shear Rebar Volume (m^3)": None,
        "Sideface Rebar Area (m^2)": None,
        "Sideface Rebar Volume (m^3)": None,
        "Total Rebar Area (m^2)": None,
        "Total Rebar Volume (m^3)": None,
    }
    beam_schedule_df = pd.DataFrame(columns=columns)
    quantities_schedule_df = pd.DataFrame(quantities, index=[0])
    return beam_schedule_df, quantities_schedule_df
