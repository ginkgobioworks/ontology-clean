# Reporting assay results: hits and activity

The end point of most experimental analyses at
[Ginkgo](https://www.ginkgobioworks.com/) is a ranked list of biological strains
based on their performance during the assay. Strain design and the detail of a
screen depend on the organism, pathway and end goal of the
campaign. The custom nature of biological design makes it difficult to
standardize the analyses, but we'd like to retrieve the results of the analysis
in a standard way to facilitate large scale interpretation of results across
multiple campaigns.

To capture analysis of an experiment where we've carefully [labeled measurement intent](https://github.com/ginkgobioworks/ontology-clean/blob/master/docs/experimental_plate_labels.md)
and [defined controls](https://github.com/ginkgobioworks/ontology-clean/blob/master/docs/representing_controls.md)
we need a structured way to represent the outputs. We attempt to capture three
sets of information, grouped under the
[response-endpoint](https://www.ebi.ac.uk/ols/ontologies/bao/terms?iri=http%3A%2F%2Fwww.bioassayontology.org%2Fbao%23BAO_0000181)
namespace: the hit classification, the logic for the selection, and the calculated
activity measurements going into the selection.

## Assay hits

- [active](https://www.ebi.ac.uk/ols/ontologies/bao/terms?iri=http%3A%2F%2Fpurl.obolibrary.org%2Fobo%2FPATO_0002354) Strains that appear to have activity for the measured function and are above the limit of detection. 
  - `yes`
  - `no`
  - `maybe` -- Not enough confidence to declare as another category.

- [hit-selection](https://www.ebi.ac.uk/ols/ontologies/stato/terms?iri=http%3A%2F%2Fpurl.obolibrary.org%2Fobo%2FSTATO_0000277) -- Mark a strain with an outcome from an experimental screen.

  - `advance` -- Top strains that move on to additional analyses or delivery
  - `improved`
  - `neutral`
  - `deleterious`

## Logic for selecting hits

- [selection-criterion](https://www.ebi.ac.uk/ols/ontologies/obi/terms?iri=http%3A%2F%2Fpurl.obolibrary.org%2Fobo%2FOBI_0001755)
  -- The logic behind classifying the strain with the hit category, 
  one or more specifications of:
 
  - `response` -- A label for the normalized response measurement.
  - `comparison` -- `[=, !=, >, >=, <, <=, custom]`
  - `threshold` -- The cutoff value for classifying the response.
  - [data-transformation](https://www.ebi.ac.uk/ols/ontologies/stato/terms?iri=http%3A%2F%2Fpurl.obolibrary.org%2Fobo%2FOBI_0200166) -- Statistical methods used to prepare the `response` value, broken into 4 categories of normalization and transformation:

    - [background-correction](https://www.ebi.ac.uk/ols/ontologies/obi/terms?iri=http%3A%2F%2Fpurl.obolibrary.org%2Fobo%2FOBI_0000666) -- Approach used for subtraction of background based on a reference
       - standard-curve
       - od-normalized
       - bca-normalized
       - total-protein
       - `raw` -- non-normalized data
       - custom

    - [normalization-control](https://www.ebi.ac.uk/ols/ontologies/bao/terms?iri=http%3A%2F%2Fwww.bioassayontology.org%2Fbao%23BAO_0002750) -- Control or plate reference used for background correction and normalization
       - positive
       - standard
       - spike-in
       - plate-all
       - plate-per-plate

    - [normalization-method](https://www.ebi.ac.uk/ols/ontologies/obi/terms?iri=http%3A%2F%2Fpurl.obolibrary.org%2Fobo%2FOBI_0200169) -- Statistical method applied to the `normalization-control`
       - standard-deviation
       - mean
       - median

    - [candidate-ranking](https://www.ebi.ac.uk/ols/ontologies/stato/terms?iri=http%3A%2F%2Fpurl.obolibrary.org%2Fobo%2FSTATO_0000118) -- Statistical approach for ranking outcomes to determine candidates
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
       - [strictly standardized mean difference](https://www.ebi.ac.uk/ols/ontologies/stato/terms?iri=http%3A%2F%2Fpurl.obolibrary.org%2Fobo%2FSTATO_0000135)
         -- SSMD; standardized mean based on difference between multiple groups.
       - `custom` -- Other non-categorized method.

## Reporting standardized activity measurements

We also want to capture the calculate activity measurement used in making the
hit selection and do this using a list of `reponse-measure` groups, each of
which captures the value of the activity response linked to a normalized value
contributing to the `selection-criterion`

- `response-measure`
  - `response` -- A label for the normalized response measurement, matching the
    specification in the `selection-criterion`
  - [measurement](https://www.ebi.ac.uk/ols/ontologies/stato/terms?iri=http%3A%2F%2Fpurl.obolibrary.org%2Fobo%2FIAO_0000109) -- The measurement value

## Data upload approach

An important component is making entering this information easy to enter and
upload from the typical analysis methods of choice: table-like objects from
pandas in Jupyter, Excel or R analyses:

- Prepare an output analysis table with a column for `hit-selection`, `active` and columns for all of the
  `response` values used in the `selection-criterion`. This will translate into
  the `hit-response` and `response-measure` for each aggregated sample and `reponse` column
  in the data frame.
- Prepare a data table mapping `response` columns to the statistical methods
  used in `data-transformation`.
- Provide a list of `selection-criteriion` with the corresponding `response`
  reference to the data frame columns.

## Example

Prepare a data table with `response` calculated values, `active` and `hit-selection`
linked to original samples in the experiment:

| strain | root sample | myspecial Z-Score | raw activity | active | hit-selection |
| ---    | ---         | ---               | ---          | ---    | ---           |
| 123    | 15          | 0.8               | 5.6          | yes    | advance       |
| 124    | 28          | 0.0               | 0.2          | no     |               |

Prepare a data table mapping `response` to statistical methods used in
`data-transformation`:

| response          | background-correction | normalization-control | normalization-method | candidate-ranking |
| ---               | ---                   | ---                   | ---                  | ---               |
| myspecial Z-score | standard-curve        | positive              | mean                 | z-score           |
| raw activity      | raw                   |                       |                      |

Define `selection-criteria`:
```
myspecial Z-Score > 0.7
raw activity > 4.0
```
which gets transformed into:
```
hts-assay-sample:
  lims-reference:
    root-sample: 15
    strain: 123
  response-endpoint:
    hit-selection: advance
    active: yes
    selection-criteria:
      [{response: myspecial Z-Score, comparison: > threshold: 0.7,
        data-tranformation: {background-correction: z-score,
                             normalization-control: positive,
                             normalization-method: mean,
                             candidate-ranking: z-score}},
       {response: raw activity, comparison: > threshold: 4.0, 
        data-transformation: {background-correction: raw}}]
    response-measure:
      [{response: myspecial Z-score, measurement: 0.8}
       {response: raw activity, measurement: 5.6}]

hts-assay-sample:
  lims-reference:
    root-sample: 28
    strain: 124
  response-endpoint:
    active: no
    selection-criteria:
      [{response: myspecial Z-Score, comparison: > threshold: 0.7,
        data-tranformation: {background-correction: z-score,
                             normalization-control: positive,
                             normalization-method: mean,
                             candidate-ranking: z-score}},
       {response: raw activity, comparison: > threshold: 4.0,
        data-transformation: {background-correction: raw}}]
    response-measure:
      [{response: myspecial Z-score, measurement: 0.0}
       {response: raw activity, measurement: 0.1}]
```
