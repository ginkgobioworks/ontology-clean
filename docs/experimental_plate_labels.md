# Establishing experimental context with plate labels

When analyzing experimental data, we need ways to provide context on
measurements. An experimental workflow consists of multiple steps, many of which
may have similar measurements. For example, we often check for cell growth by
measuring OD600 absorbance using a plate reader after each transfer step. This
allows us to identify growth issues and loss of clones at each step. During
analysis, we automatically aggregate all these measurements on the same original
samples and need a way to distinguish them.

To handle this, we provide labels on measurement steps to establish the context
and aid in interpretation. These mirror the steps in an analysis workflow:

- pellet
- glycerol
- induced
- preculture
- culture
- production
- aliquot
- dilution
- reaction -- A terminal reaction plate, often containing multiple assay
  specific measurements.

Additional labels identify specific plate relationships:

- replicate -- A duplicate of an identically labeled measurement.
- redo -- Distinguish a new measurement replacing a previous with the same
  label.
