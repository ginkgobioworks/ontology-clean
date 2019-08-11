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
we need a structured way to represent the outputs. We attempt to capture three
sets of information, grouped under the
[response-endpoint](https://www.ebi.ac.uk/ols/ontologies/bao/terms?iri=http%3A%2F%2Fwww.bioassayontology.org%2Fbao%23BAO_0000181)
namespace: the hit classification, how it was selected, and the normalized
activity calculations going into this score.

## Assay hits

To identify top strains from a experimental screen we mark selected hits and
define the selection criteria:

- [hit-selection](https://www.ebi.ac.uk/ols/ontologies/stato/terms?iri=http%3A%2F%2Fpurl.obolibrary.org%2Fobo%2FSTATO_0000277) -- Mark a strain with a positive outcome from an experimental screen.
  - `winner` -- Top strains that move on to additional analyses or delivery
  - `active` -- Strains that appear to have activity for the measured function
    and are above the limit of detection. A larger group than the categorized
    winners and useful when reusing or analyzing strains in different contexts.
  - `low-confidence` -- Potentially good strain but without good confidence to
    declare as another category.
  - `inactive` -- An inactive strain based on the screen results (nicer than
    calling strains losers)

## Logic for selecting hits

- [selection-criterion](https://www.ebi.ac.uk/ols/ontologies/obi/terms?iri=http%3A%2F%2Fpurl.obolibrary.org%2Fobo%2FOBI_0001755)
  -- The logic behind classifying the strain with the hit category. This is one
  logic function of one or more specifications of:
 
  - `response` -- A label for the normalized response measurement.
  - `comparison` -- `[=, !=, >, >=, <, <=, custom]`
  - `threshold` -- The cutoff value for classifying the response.
  - [data-transformation](https://www.ebi.ac.uk/ols/ontologies/stato/terms?iri=http%3A%2F%2Fpurl.obolibrary.org%2Fobo%2FOBI_0200166)
    -- Method used to prepare the `response` value. Often this will not be a
    direct measure of activity, but some proxy that is easier to assay at scale.

    - [z-score](https://www.ebi.ac.uk/ols/ontologies/stato/terms?iri=http%3A%2F%2Fpurl.obolibrary.org%2Fobo%2FSTATO_0000104)
      -- Score after statistical normalization based on mean and standard deviations.
    - [mad-score](https://www.ebi.ac.uk/ols/ontologies/bao/terms?iri=http%3A%2F%2Fwww.bioassayontology.org%2Fbao%23BAO_0002127)
      -- Score after statistical normalization based on median and median absolute
      deviations, which can be more resilient to outliers.
    - [percent-response](https://www.ebi.ac.uk/ols/ontologies/bao/terms?iri=http%3A%2F%2Fwww.bioassayontology.org%2Fbao%23BAO_0000082)
      -- Signal normalized to positive and negative controls.
    - [fold-change](https://www.ebi.ac.uk/ols/ontologies/stato/terms?iri=http%3A%2F%2Fpurl.obolibrary.org%2Fobo%2FSTATO_0000169)
      -- A relative change in activity based on experimental controls, based on more
      complicated criteria.
    - [strictly standardized mean difference](https://www.ebi.ac.uk/ols/ontologies/stato/terms?iri=http%3A%2F%2Fpurl.obolibrary.org%2Fobo%2FSTATO_0000135
      -- SSMD; standardized mean based on difference between multiple groups.
    - [background-correction](https://www.ebi.ac.uk/ols/ontologies/obi/terms?iri=http%3A%2F%2Fpurl.obolibrary.org%2Fobo%2FOBI_0000666) -- Substraction of background based on control samples
    - `raw` -- non-normalized data
    - `custom` -- Other non-categorized method.

## Reporting standardized activity measurements

We also want to capture the analyzed and normalized activity measurement used in
making the hit selection and do this using a list of `reponse-measure` groups,
each of which captures the value of the activity response linked to a normalized
value contributing to the `selection-criterion`

- `response-measure`
  - `response` -- A label for the normalized response measurement, matching the
    specification in the `selection-criterion`
  - [measurement](https://www.ebi.ac.uk/ols/ontologies/stato/terms?iri=http%3A%2F%2Fpurl.obolibrary.org%2Fobo%2FIAO_0000109) -- The measurement value

## Data upload approach

An important component is making entering this information easy to enter and
upload from the typical analysis methods of choice: table-like objects from
pandas in Jupyter, Excel or R analyses. The plan for a workflow to
upload and specify these:

- Prepare an analyzed table with a column for `hit-selection` and columns for all of the
  `response` values used in the `selection-criterion`. This will translate into
  the `hit-response` and `response-measure` for each aggregated sample and `reponse` column
  in the data frame.
- Provide a list of `selection-criteriion` with the corresponding `response`
  reference to the data frame columns.

## Example

Prepare a data table with calculations and `hit-selection`:

| strain | root sample | myspecial Z-Score | raw activity | hit-selection |
| --- | --- | --- | --- | --- | --- |
| 123 | 15 | 0.8 | 5.6 | winner |
| 124 | 28 | 0.0 | 0.2 | inactive |

Define `selection-criteria`:
```
myspecial Z-Score > 0.7 z-score
raw activity > 4.0 raw
```
which gets transformed into:
```
hts-assay-sample:
  lims-reference:
    root-sample: 15
    strain: 123
  response-endpoint:
    hit-selection: winner
    selection-criteria:
      [{response: myspecial Z-Score, comparison: > threshold: 0.7, data-transformation: z-score},
       {response: raw activity, comparison: > threshold: 4.0, data-transformation: raw}]
    response-measure:
      [{response: myspecial Z-score, measurement: 0.8}
       {response: raw activity, measurement: 5.6}]

hts-assay-sample:
  lims-reference:
    root-sample: 28
    strain: 124
  response-endpoint:
    hit-selection: inactive
    selection-criteria:
      [{response: myspecial Z-Score, comparison: > threshold: 0.7, data-transformation: z-score},
       {response: raw activity, comparison: > threshold: 4.0, data-transformation: raw}]
    response-measure:
      [{response: myspecial Z-score, measurement: 0.0}
       {response: raw activity, measurement: 0.1}]
```
