# Establishing experimental intent with plate labels

When analyzing experimental data, we need ways to provide intent on
measurements. An experimental workflow consists of multiple steps, many of which
may have similar measurements. For example, we often check for cell growth by
measuring OD600 absorbance using a plate reader after each transfer step. This
allows us to identify growth issues and loss of clones at each step. During
analysis, we automatically aggregate all these measurements on the same original
samples and need a way to distinguish them.

To handle this, we provide labels on measurement steps to establish the intended context
and aid in interpretation. To establish unique labels we have three levels of
classification to define, all of which live in the
[intent-label](https://www.ebi.ac.uk/ols/ontologies/obi/terms?iri=http%3A%2F%2Fpurl.obolibrary.org%2Fobo%2FIAO_0000009)
namespace:

- `label` -- Baseline label defining the step in an analysis workflow
  - cryostock -- Glycerol or other baseline stock plate
  - preculture
  - culture
  - production
  - reaction -- A terminal reaction plate, often containing multiple assay
    specific measurements
  - pellet
  - induced
  - replicate -- A duplicate of an identically labeled measurement
  - redo -- Distinguish a new measurement replacing a previous with the same label

- `label-substep` -- A second level relationship connected with the label,
  defining a sub-step
  - aliquot -- A terminal branch of a preceding sample with a label, on
    which a measurement is being collected
  - timecourse -- A set of timepoint samples from a previous labeled sample
  - dilution

- `label-index` -- A number uniquifying multiple plates at the same step in the
  process.

The unique name for an `intent-label` is the combination of the 3 fields.
`label-substep` and `label-index` are optional and not included in the unique
name if not set. For example, measurements on a plate, or parent plate, with `label-intent`: 
`label: production, label-substep: aliquot, label-index: 2` would be uniquely named
`production aliquot 2` during downstream analysis steps.
