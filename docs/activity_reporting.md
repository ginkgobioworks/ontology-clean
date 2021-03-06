# Reporting assay results: hits and activity

The end point of most experimental analyses at
[Ginkgo](https://www.ginkgobioworks.com/) is a ranked list of biological strains
based on their performance during assessment assays. Strain design and the
details of an assay screen depend on the organism, pathway and end goal of the
campaign. The custom nature of biological design makes it difficult to
standardize analyses, but we'd like to retrieve the results of the analysis
in a standard way to facilitate large scale interpretation of results across
multiple campaigns.

Results on a strain are relative to the context of the assay:
strain + condition = result. Condition specifications include reagents and
media, timepoints, and other varied experimental inputs that help explain the
result.

To capture analysis of an experiment where we've carefully [labeled measurement
intent](https://github.com/ginkgobioworks/ontology-clean/blob/master/docs/experimental_plate_labels.md),
[defined
controls](https://github.com/ginkgobioworks/ontology-clean/blob/master/docs/representing_controls.md)
and enumerated the assay conditions, we need a structured way to represent the
outputs. We capture information at two levels:

- Task level: describe the different responses, data transformation and
  selection logic as a [response-endpoint](https://www.ebi.ac.uk/ols/ontologies/bao/terms?iri=http%3A%2F%2Fwww.bioassayontology.org%2Fbao%23BAO_0000181):

  - Data transformation -- Transform the raw data by background correction,
    application of a standard curve, normalization, and calculating a standardized
    score for each sample. This process produces one or more response values for
    each sample which is then used for determine experimental outcomes: calling
    hits and advancing molecules/samples/strains to the next round.
  - Logic for hit selection  -- Define the logic used to make the hit classifications.


- Test level: For a strain, condition and response-endpoint specify the
  response-measure:

  - Hit selection -- Indicate whether a sample is active, and whether it will be
    advanced to the next round in the project.
  - Activity measurements -- The processed measurement value that contributes to the
    hit selection logic.

Data transformation produces a `response` measure, corresponding to a column name
of values in the output analysis data frame.  Data transformation steps, hit
selection logic and calculated activity measurements refer to this `response`
label.

## Data upload approach

An important component is making entering this information easy to enter and
upload from the typical analysis methods of choice: table-like objects from
Jupyter, Excel or R analyses:

- Prepare an output analysis table starting with a structured input data frame.
  This analysis table has a column for both `advance` and `active`, as well as
  and columns for all of the `response` values used in `selection-criterion` or
  `data-transformation`. This will translate into the `hit-response` and
  `response-measure` for each aggregated sample and `reponse` column in the data
  frame.
- Prepare a data table mapping `response` columns to statistical methods
  and formula used in defining `selection-criterion`.
- Prepare a data table mapping `response` columns to the statistical methods
  used in `data-transformation`.

### Example

Prepare a data table with transformed `response` data, `active` and `advance`
linked to the original aggregated samples and conditions in the experiment. This
table is your final processed data frame, with additional columns to support the
hit classification:

| other columns | strain  | condition/media | myscore | myprocessed | active | advance |
| ---           | ---     | ---             | ---     | ---         | ---    | ---     |
| ...           | 15      | media A         | 0.8     | 5.6         | yes    | yes     |
| ...           | 15      | media B         | 0.2     | 1.2         | no     | no      |
| ...           | 28      | media A         | 0.0     | 0.2         | no     | no      |
| ...           | 28      | media B         | 0.0     | 0.2         | no     | no      |

Prepare a data table mapping `response` columns to `selection-criterion`:

| response | hit-selection-type | hit-selection-value | formula                             |
| ---      | ---                | ---                 | ---                                 |
| myscore  | active             | yes                 | myscore > 0.7                       |
| myscore  | advance            | yes                 | myscore > 0.9 or container='c12345' |

Prepare a data table mapping `response` to statistical methods used in
`data-transformation`:

| response    | background-adjustment | standard-curve            | normalization        | standardized-score | replicate-analysis  |
| ---         | ---                   | ---                       | ---                  | ---                | ---                 |
| myscore     | negative              | [compound] = m[OD520] + b | [compound] / [OD600] | z-score            | median              |
| myprocessed | negative              |                           | per-plate-mean       |                    |                     |

### Complex selection criterion examples

In the most straightforward case, a decision on `response` and `hit-selection`
is based on a simple formula; a single calculated score with a
cutoff.

However, there are a number of common cases where the decision making is more
complex and we'd like to capture these. We give up some computability on the
formula by making it free text to handle these cases. Take this example data
frame with two calculated scores:

| other columns | strain | myscore | myscore2    | active | advance |
| ---           | ---    | ---     | ---         | ---    | ---     |
| ...           | 15     | 0.8     | 5.6         | yes    | yes     |
| ...           | 28     | 0.6     | 6.0         | no     | no      |

To represent a case where you pass a hit based on logic from two scores
combined, represent as two rows in the `selection-criterion` data frame so that
we know to pull both myscore and myscore2 from the final data frame:

| response  | hit-selection | hit-selection-value | formula                                |
| ---       | ---           | ---                 | ---                                    |
| myscore   | active        | yes                 | myscore > 0.7 and myscore2 < 7.0       |
| myscore2  | active        | yes                 | myscore > 0.7 and myscore2 < 7.0       |

For cases where you pass due to external factors, encode this in as much detail
as necessary in the formula:

| response  | hit-selection | hit-selection-value | formula                                |
| ---       | ---           | ---                 | ---                                    |
| myscore   | advance       | yes                 | myscore > 0.7 or design-controls or (container = [c12345, c23456] and well = [A1, B1])  |

## Response representation details

To enable re-usability of data, the underlying representation categorizes all of
the response, data transformation and selection criteria in a standardized way.

### Data transformation

- [data-transformation](https://www.ebi.ac.uk/ols/ontologies/stato/terms?iri=http%3A%2F%2Fpurl.obolibrary.org%2Fobo%2FOBI_0200166) -- Perform mathematical transformations on the raw data to obtain one or more `response` values used to determine the experimental outcomes.

  - [background-correction](https://www.ebi.ac.uk/ols/ontologies/obi/terms?iri=http%3A%2F%2Fpurl.obolibrary.org%2Fobo%2FOBI_0000666) -- Remove irrelevant contributions from the measured signal, e.g. those due to instrument noise or sample preparation, based on [specified controls](https://github.com/ginkgobioworks/ontology-clean/blob/master/docs/representing_controls.md#approaches-for-modeling-controls-and-requests-for-discussion):
     - negative
     - blank
     - parent
     - standard
     - spike-in
     - positive
  
  - `standard-curve` -- Apply a standard curve to convert a raw or background-corrected response into a response with units of interest.
     - Free text capturing the equation used in conversion: `y = mx + b`,
       specify y and x. For instance `[out] = m[col] + b` where `col=abs600
       out=your-compound in ug/ml`

  - [normalization](https://www.ebi.ac.uk/ols/ontologies/obi/terms?iri=http%3A%2F%2Fpurl.obolibrary.org%2Fobo%2FOBI_0200169) -- Combine multiple response values to create a new response to put the data on equal footing in order to create a common base for comparisons. For example, normalize titer by biomass to estimate per-cell productivity.
     - Free text column name specifying the operation used for normalization (`BCA / OD`) (`activity - negative control`)

  - [standardized-score](https://www.ebi.ac.uk/ols/ontologies/so/terms?iri=http%3A%2F%2Fpurl.obolibrary.org%2Fobo%2FSO_0001685) -- Statistical approach for standardizing scores for ranking candidates.
     - [z-score](https://www.ebi.ac.uk/ols/ontologies/stato/terms?iri=http%3A%2F%2Fpurl.obolibrary.org%2Fobo%2FSTATO_0000104)
       -- Score after statistical normalization based on mean and standard deviations.
     - [mad-score](https://www.ebi.ac.uk/ols/ontologies/bao/terms?iri=http%3A%2F%2Fwww.bioassayontology.org%2Fbao%23BAO_0002127)
       -- Score after statistical normalization based on median and median absolute
       deviations, which can be more resilient to outliers.
     - [percent-response](https://www.ebi.ac.uk/ols/ontologies/bao/terms?iri=http%3A%2F%2Fwww.bioassayontology.org%2Fbao%23BAO_0000082)
       -- Signal normalized to positive and negative controls.
     - [fold-change](https://www.ebi.ac.uk/ols/ontologies/stato/terms?iri=http%3A%2F%2Fpurl.obolibrary.org%2Fobo%2FSTATO_0000169)
       -- A relative change in activity based on experimental controls.
     - [strictly-standardized-mean-difference](https://www.ebi.ac.uk/ols/ontologies/stato/terms?iri=http%3A%2F%2Fpurl.obolibrary.org%2Fobo%2FSTATO_0000135)
       -- SSMD; standardized mean based on difference between multiple groups.

  - [replicate-analysis](https://www.ebi.ac.uk/ols/ontologies/obi/terms?iri=http%3A%2F%2Fpurl.obolibrary.org%2Fobo%2FOBI_0200057) -- Statistical method applied to the `response` values for grouping replicates. Outcomes are determined on the group of replicates.
     - mean
     - median
     - min
     - max
     - majority-rule -- An approach like 2 out of 3

### Logic for hit selection

- [selection-criterion](https://www.ebi.ac.uk/ols/ontologies/obi/terms?iri=http%3A%2F%2Fpurl.obolibrary.org%2Fobo%2FOBI_0001755)
  -- The logic behind a hit selection decision linked to the normalized response
  measurement used in selections. One or more specifications of:
 
  - `hit-selection-type` -- Type of hit selection
     - [`active`, `advance`]
  - `hit-selection-value` -- The hit selection decision
     - [`yes`, `no`, `maybe`, `invalid`]
  - `formula` -- Free text describing the relationship between the `response` and the `hit-selection` decision:
     - Example: `myscore > 4.0 or container-id='c12345'`

### Activity response score

We also want to capture the calculated activity score used in making the
hit selection. These correspond to calculated values in a `response` column in
your final output analysis:

- `response-measure`
  - `response-endpoint` -- A pointer to the response name, containing `data-transformation`
    and `selection-criterion` logic.
  - [measurement](https://www.ebi.ac.uk/ols/ontologies/stato/terms?iri=http%3A%2F%2Fpurl.obolibrary.org%2Fobo%2FIAO_0000109) -- The measurement value

### Hit classifications

- [hit-selection](https://www.ebi.ac.uk/ols/ontologies/stato/terms?iri=http%3A%2F%2Fpurl.obolibrary.org%2Fobo%2FSTATO_0000277) -- Mark the outcome from an experimental screen, categorizing at two levels:

  - [active](https://www.ebi.ac.uk/ols/ontologies/bao/terms?iri=http%3A%2F%2Fpurl.obolibrary.org%2Fobo%2FPATO_0002354) Strains that appear to have activity for the measured function and are above the limit of detection. 
    - `yes`
    - `no`
    - `maybe` -- Not enough confidence to decide whether to move forward.
    - `invalid` -- Experimental error

  - `advance` -- Strains that advance to additional experimental rounds or
    client delivery. Can be either the top hits from the screen selected
    automatically by applying a logic function to the responses, or manually
    curated strains that are of interest for any number of reasons.
    - [`yes`, `no`]
