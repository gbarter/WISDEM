"""
Jake Nunemaker
National Renewable Energy Lab
07/11/2019

This module contains default vessel process times.
"""


process_times = {
    # Export Cable Installation
    "onshore_construction_time": 48,  # hr
    "trench_dig_speed": 0.1,  # km/hr
    "pull_winch_speed": 5,  # km/hr
    "tow_plow_speed": 5,  # km/hr
    # Array Cable Installation
    # General Cable Installation
    "plgr_speed": 1,  # km/hr
    "cable_load_time": 6,  # hr
    "cable_prep_time": 1,  # hr
    "cable_lower_time": 1,  # hr
    "cable_pull_in_time": 5.5,  # hr
    "cable_termination_time": 5.5,  # hr
    "cable_lay_speed": 1,  # km/hr
    "cable_lay_bury_speed": 0.3,  # km/hr
    "cable_bury_speed": 0.5,  # km/hr
    "cable_splice_time": 48,  # hr
    "cable_raise_time": 0.5,  # hr
    # Offshore Substation
    "topside_fasten_time": 2,  # hr
    "topside_release_time": 2,  # hr
    "topside_attach_time": 6,  # hr
    # Monopiles
    "mono_embed_len": 30,  # m
    "mono_drive_rate": 20,  # m/hr
    "mono_fasten_time": 12,  # hr
    "mono_release_time": 3,  # hr
    "tp_fasten_time": 8,  # hr
    "tp_release_time": 2,  # hr
    "tp_bolt_time": 4,  # hr
    "grout_cure_time": 24,  # hr
    "grout_pump_time": 2,  # hr
    # Scour Protection
    "drop_rocks_time": 10,  # hr
    "load_rocks_time": 4,  # hr
    # Turbines
    "tower_section_fasten_time": 4,  # hr, applies to all sections
    "tower_section_release_time": 3,  # hr, applies to all sections
    "tower_section_attach_time": 6,  # hr, applies to all sections
    "nacelle_fasten_time": 4,  # hr
    "nacelle_release_time": 3,  # hr
    "nacelle_attach_time": 6,  # hr
    "blade_fasten_time": 1.5,  # hr
    "blade_release_time": 1,  # hr
    "blade_attach_time": 3.5,  # hr
    # Misc.
    "site_position_time": 2,  # hr
    "rov_survey_time": 1,  # hr
    "crane_reequip_time": 1,  # hr
}
