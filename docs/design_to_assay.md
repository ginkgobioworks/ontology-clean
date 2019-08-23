# Represent design information for assay screens

Organizing and performing assay screens requires knowing decisions that went
into the design of the constructs. To ease the transfer of information, we
provide useful sample level information that helps inform assay design and
evaluation. Some of these are components of the DNA design, while others are
expected properties based on prior knowledge.

## Selection markers

We define the selection strategy for identifying transformed clones using
one or more [selection-marker](https://www.ebi.ac.uk/ols/ontologies/bao/terms?iri=http%3A%2F%2Fwww.bioassayontology.org%2Fbao%23BAO_0003068)
specifications that depend on the strategies used:

- [antibiotic-resistance](https://www.ebi.ac.uk/ols/ontologies/bao/terms?iri=http%3A%2F%2Fwww.bioassayontology.org%2Fbao%23BAO_0000099) -- Antibiotic resistance markers.
- [prototrophy](https://www.ebi.ac.uk/ols/ontologies/fypo/terms?iri=http%3A%2F%2Fpurl.obolibrary.org%2Fobo%2FFYPO_0000128) -- Selection based on inability to make a particular compound. The desired transformation backbone supplements an [auxotroph](https://en.wikipedia.org/wiki/Auxotrophy) unable to make the compound.
- nuclease -- Provide selection with removal of destructive nuclease, [like X-cutter](https://patents.google.com/patent/WO2017201311A2/en)

## Localization

Define expected protein localization and also protein sequence motifs that
contribute to secretion:

- [macromolecule-localization](https://www.ebi.ac.uk/ols/ontologies/go/terms?iri=http%3A%2F%2Fpurl.obolibrary.org%2Fobo%2FGO_0033036) -- Expected cellular location of the protein.
  - membrane
  - cytosol
  - er
  - other
- [signal-peptide](https://www.ebi.ac.uk/ols/ontologies/so/terms?iri=http%3A%2F%2Fpurl.obolibrary.org%2Fobo%2FSO_0000418) -- An N-terminal peptide sequence providing localization

## Copy number

- [copy-number](https://www.ebi.ac.uk/ols/ontologies/ncit/terms?iri=http%3A%2F%2Fpurl.obolibrary.org%2Fobo%2FNCIT_C49142) -- Description of the expected copy number of the plasmid. TODO: could this be a list of choices (high, medium, low)?
