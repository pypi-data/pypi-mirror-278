#! /usr/bin/env python

"""File containing various necessary definitions, such as abbreviations for each
pipeline step
"""

# Abbreviations for pipeline steps. These are the values used in the JWST calibration
# pipeline, and are also the values that must be used in jwst_reffiles input configuration
# files
PIPE_STEPS = ['group_scale', 'dq_init', 'saturation', 'ipc', 'firstframe', 'lastframe',
              'superbias', 'refpix', 'linearity', 'persistence', 'rscd', 'dark_current',
              'jump', 'rate']

# Define the fits header keyword that accompanies each step
PIPE_KEYWORDS = {'S_GRPSCL': 'group_scale', 'S_DQINIT': 'dq_init', 'S_SATURA': 'saturation',
                 'S_REFPIX': 'refpix', 'S_SUPERB': 'superbias', 'S_IPC': 'ipc', 'S_PERSIS': 'persistence',
                 'S_DARK': 'dark_current', 'S_LINEAR': 'linearity', 'S_FRSTFR': 'firstframe',
                 'S_LASTFR': 'lastframe', 'S_RSCD': 'rscd', 'S_JUMP': 'jump',  'S_RAMP': 'rate'}

# List of available instruments
INSTRUMENTS = ['nircam', 'niriss', 'nirspec', 'miri', 'fgs']

# List of pipeline configuration files used by calwebb_detector1 pipeline
CALDETECTOR1_CFG_FILES = ['group_scale.cfg', 'dq_init.cfg', 'saturation.cfg', 'ipc.cfg', 'firstframe.cfg',
                          'lastframe.cfg', 'superbias.cfg', 'refpix.cfg', 'linearity.cfg', 'persistence.cfg',
                          'rscd.cfg', 'dark_current.cfg', 'jump.cfg', 'ramp_fit.cfg', 'gain_scale.cfg',
                          'calwebb_detector1.cfg']
