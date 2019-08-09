# Reporting assay results: hits and activity

The end point of most experimental analyses at
[Ginkgo](https://www.ginkgobioworks.com/) is a ranked list of biological strains
based on their performance during the assay. Strain design and the type of
screens depend on the organism, pathway and end goal of the
campaign. The custom nature of biological design makes it difficult to
standardize the analyses, but we'd like to retrieve the results of the analysis
in a standard way to facilitate large scale interpretation of results across
multiple campaigns.

To capture analysis of an experiment where we've carefully [labeled measurement intent](https://github.com/ginkgobioworks/ontology-clean/blob/master/docs/experimental_plate_labels.md)
and [defined controls](https://github.com/ginkgobioworks/ontology-clean/blob/master/docs/representing_controls.md)
we need a structured way to represent the outputs. We attempt to capture two
sets of information, grouped under the
[response-endpoint](https://www.ebi.ac.uk/ols/ontologies/bao/terms?iri=http%3A%2F%2Fwww.bioassayontology.org%2Fbao%23BAO_0000181)
namespace.

## Defining assay hits

To identify top strains from a experimental screen we mark selected hits and
define the selection criteria:

- [hit-selection](https://www.ebi.ac.uk/ols/ontologies/stato/terms?iri=http%3A%2F%2Fpurl.obolibrary.org%2Fobo%2FSTATO_0000277) -- Mark a strain with a positive outcome from an experimental screen.
  - `winner` -- Top strains that move on to additional analyses or delivery
  - `active` -- Strains that appear to have activity for the measured function
    and are above the limit of detection. A larger group than the categorized
    winners and useful when reusing or analyzing strains in different contexts.
- [selection-criterion](https://www.ebi.ac.uk/ols/ontologies/obi/terms?iri=http%3A%2F%2Fpurl.obolibrary.org%2Fobo%2FOBI_0001755)
  -- The logic behind classifying the strain with a positive hit. This is a
  logic function of one or more specifications of a metric, comparison approach
  and threshold. For now, we capture as free text but would like to move to a
  structured approach after collecting examples.

## Reporting standardized activity measurements

We also want to capture the analyzed and normalized activity measurement used in
making the hit selection. Often this will not be a direct measure of activity,
but some proxy that is easier to assay at scale.

- [z-score](https://www.ebi.ac.uk/ols/ontologies/stato/terms?iri=http%3A%2F%2Fpurl.obolibrary.org%2Fobo%2FSTATO_0000104)
  -- Score after normalization against experimental controls and statistical
  normalization based on standard deviation.
- [fold-change](https://www.ebi.ac.uk/ols/ontologies/stato/terms?iri=http%3A%2F%2Fpurl.obolibrary.org%2Fobo%2FSTATO_0000169)
  -- A relative change in activity based on experimental controls and initial
  baseline values.
- [percent-response](https://www.ebi.ac.uk/ols/ontologies/bao/terms?iri=http%3A%2F%2Fwww.bioassayontology.org%2Fbao%23BAO_0000082)
  -- The percentage change of response relative to a baseline. (TODO: redundant
  with fold-change or useful distinction?)

TODO: Other commonly reported activity measures to include?
