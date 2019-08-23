# Reporting assay results: hits and activity

The end point of most experimental analyses at
[Ginkgo](https://www.ginkgobioworks.com/) is a ranked list of biological strains
based on their performance during assessment assays. Strain design and the
details of an assay screen depend on the organism, pathway and end goal of the
campaign. The custom nature of biological design makes it difficult to
standardize the analyses, but we'd like to retrieve the results of the analysis
in a standard way to facilitate large scale interpretation of results across
multiple campaigns.

To capture analysis of an experiment where we've carefully [labeled measurement intent](https://github.com/ginkgobioworks/ontology-clean/blob/master/docs/experimental_plate_labels.md)
and [defined controls](https://github.com/ginkgobioworks/ontology-clean/blob/master/docs/representing_controls.md)
we need a structured way to represent the outputs. We attempt to capture three
sets of information, grouped under the
[response-endpoint](https://www.ebi.ac.uk/ols/ontologies/bao/terms?iri=http%3A%2F%2Fwww.bioassayontology.org%2Fbao%23BAO_0000181)
namespace: the logic for data processing and hit selection, the final classifications, and the calculated
activity measurements.

## Logic for selecting hits

- [selection-criterion](https://www.ebi.ac.uk/ols/ontologies/obi/terms?iri=http%3A%2F%2Fpurl.obolibrary.org%2Fobo%2FOBI_0001755)
  -- The logic behind classifying a strain, one or more specifications of:
 
  - `response` -- A label for the normalized response measurement.
  - [replicate-analysis](https://www.ebi.ac.uk/ols/ontologies/obi/terms?iri=http%3A%2F%2Fpurl.obolibrary.org%2Fobo%2FOBI_0200057) -- Statistical method applied to the `response` for grouping replicates:
     - mean
     - median
     - min
     - max
     - majority-rule -- An approach like 2 out of 3
     - custom
  - `comparison` -- `[=, !=, >, >=, <, <=, custom]`
  - `threshold` -- The cutoff value for classifying the response.

  - [data-transformation](https://www.ebi.ac.uk/ols/ontologies/stato/terms?iri=http%3A%2F%2Fpurl.obolibrary.org%2Fobo%2FOBI_0200166) -- Capture approaches used to prepare the `response` value, broken into processing (background-correction, standard-curve, normalization-transformation) and standardization (standardize-score):

     - [background-correction](https://www.ebi.ac.uk/ols/ontologies/obi/terms?iri=http%3A%2F%2Fpurl.obolibrary.org%2Fobo%2FOBI_0000666) -- [Control specification](https://github.com/ginkgobioworks/ontology-clean/blob/master/docs/representing_controls.md#approaches-for-modeling-controls-and-requests-for-discussion) for background correction of raw data:
       - positive
       - negative
       - blank
       - parent
       - standard
       - spike-in

     - standard-curve -- Application of a standard curve to convert response values into measures of interest.
        - Free text capturing the equation used in conversion: `y = mx + b`, specify y and x. For instance `[out] = m[col] + b` where `col=abs600 out=your-compound in ug/ml`

     - [normalization-transformation](https://www.ebi.ac.uk/ols/ontologies/obi/terms?iri=http%3A%2F%2Fpurl.obolibrary.org%2Fobo%2FOBI_0200169) -- Define methods used to normalize data prior to standardization
        - Free text column name specifying the operation used for normalization (`BCA / OD`)

    - [standardized-score](https://www.ebi.ac.uk/ols/ontologies/so/terms?iri=http%3A%2F%2Fpurl.obolibrary.org%2Fobo%2FSO_0001685) -- Statistical approach for standardizing scores for ranking candidates
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

## Assay hits

- [hit-selection](https://www.ebi.ac.uk/ols/ontologies/stato/terms?iri=http%3A%2F%2Fpurl.obolibrary.org%2Fobo%2FSTATO_0000277) -- Mark a strain with an outcome from an experimental screen, categorizing at two levels:

  - [active](https://www.ebi.ac.uk/ols/ontologies/bao/terms?iri=http%3A%2F%2Fpurl.obolibrary.org%2Fobo%2FPATO_0002354) Strains that appear to have activity for the measured function and are above the limit of detection. 
    - `yes`
    - `no`
    - `maybe` -- Not enough confidence to decide whether to move forward.
    - `invalid` -- Experimental error

  - `advance` -- Top strains that move on to additional analyses or delivery. A
    boolean true/false value

## Reporting standardized activity measurements

We also want to capture the calculated activity measurement used in making the
hit selection. These are lists of `reponse-measure` groups, each of
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

- Prepare an output analysis table with a column for `advance`, `active` and columns for all of the
  `response` values used in the `selection-criterion`. This will translate into
  the `hit-response` and `response-measure` for each aggregated sample and `reponse` column
  in the data frame.
- Prepare a data table mapping `response` columns to the statistical methods
  used in `data-transformation` and `selection-criterion`

## Example

Prepare a data table with `response` calculated values, `active` and `advance`
linked to original samples in the experiment. This example has a score used for
selection and processed column of interest to include:

| strain | root sample | myscore | myprocessed | active | advance |
| ---    | ---         | ---     | ---         | ---    | ---     |
| 123    | 15          | 0.8     | 5.6         | yes    | true    |
| 124    | 28          | 0.0     | 0.2         | no     | false   |

Prepare a data table mapping `response` to statistical methods used in
`data-transformation` and `selection-criteria`:

| response    | background-correction | standard-curve            | normalization-transformation | standardized-score | replicate-analysis | comparison | threshold |
| ---         | ---                   | ---                       | ---                          | ---                | ---                | ---        | ---       |
| myscore     | negative              | [compound] = m[OD520] + b | [compound] / [OD600]         | z-score            | median             | >          | 0.7       |
| myprocessed | negative              |                           | per-plate-mean               |                    |                    |            |           |

which gets transformed into an underlying representation:
```
hts-assay-sample:
  lims-reference:
    root-sample: 15
    strain: 123
  response-endpoint:
    hit-selection: {advance: true, active: yes}
    selection-criteria:
      [{response: myscore, replicate-analysis: median, comparison: >, threshold: 0.7,
        data-tranformation: {background-correction: negative,
                             standard-curve: '[compound] = m[OD520] + b',
                             normalization-transformation: '[compound] / [OD600]',
                             standardized-score: z-score}},
       {response: myprocessed,
        data-transformation: {background-correction: negative, normalization-transformation: per-plate-mean}}]
    response-measure:
      [{response: myscore, measurement: 0.8}
       {response: myprocessed, measurement: 5.6}]

hts-assay-sample:
  lims-reference:
    root-sample: 28
    strain: 124
  response-endpoint:
    hit-selection: {advance: false, active: no}
    selection-criteria:
      [{response: myscore, replicate-analysis: median, comparison: >, threshold: 0.7,
        data-tranformation: {background-correction: negative,
                             standard-curve: '[compound] = m[OD520] + b',
                             normalization-transformation: '[compound] / [OD600]',
                             standardized-score: z-score}},
       {response: myprocessed,
        data-transformation: {background-correction: negative, normalization-transformation: per-plate-mean}}]
    response-measure:
      [{response: myscore, measurement: 0.0}
       {response: myprocessed, measurement: 0.1}]
```
