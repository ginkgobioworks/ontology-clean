# Identifying assay control samples

At [Ginkgo](https://www.ginkgobioworks.com/), we're working on
representing and tracking high level information about experimental design and
outcomes. Our data capture is fabulous at representing the who, what, when and
where about what happens during experimental processes, but accurately
representing the more subtle question of why is more difficult. This post explores one
aspect of this, how to succinctly represent control samples for an experiment.

Accurately capturing metadata about experiments and samples is a challenge many
research efforts face. Analyses need to take into account replicates and batching
alongside baseline controls and standards used for normalization. Because these
relationships can be complex, they often get specified in custom ways as part of
the analysis process and require additional structure to retrospectively
analyze and build automated tools around.

Here we'll describe existing ontologies for representing analysis controls and
an initial approach to using them. Structured representation of experimental
design enables data sharing and large scale analyses across multiple
experiments. We welcome feedback on the representation, and would appreciate
collaborations and pointers to how other communities represent controls in
standard ways.

## Ontology choices

To enable interoperability and standardization, we're using community efforts around
naming and representation on ontologies.
[The Open Biological and Biomedical Ontology (OBO) Foundry](http://www.obofoundry.org/)
coordinates a large number of interoperable ontology development efforts. In our
space, we need to bring in multiple ontologies and the OBO
re-uses terms between multiple ontology development efforts to create a cohesive
whole. We also hope to interoperate with [Synthetic Biology Open Language (SBOL)](http://sbolstandard.org/)
development efforts, especially around establishing [SBOL Experiment context](https://github.com/SynBioDex/SEPs/blob/master/sep_024.md), 
and make ontology choices overlapping with their efforts.

To find and explore ontology terms, the [EMBL-EBI Ontology Lookup Service](https://www.ebi.ac.uk/ols/index)
is a fantastic resource that enables both searching and browsing ontologies. We
used terms from multiple ontologies:

- [Ontology for Biomedical Investigations (OBI)](http://obi-ontology.org/) --
  The OBO ontology for describing experimental studies.
- [Systems Biology Ontology (SBO)](http://www.ebi.ac.uk/sbo/main/) -- An
  ontology for describing biological systems, tightly linked with SBOL.
- [BioAssay Ontology (BAO)](http://bioassayontology.org/) -- An ontology for
  describing biological assays. This does not currently link to OBO terms but
  contains a number of useful descriptors for the type of experimental assays we
  do at Ginkgo.

## Approaches for modeling controls and requests for discussion

For practical top level structure, we group our descriptions of the experimental
design under the
[study-design](https://www.ebi.ac.uk/ols/ontologies/obi/terms?iri=http%3A%2F%2Fpurl.obolibrary.org%2Fobo%2FOBI_0500000)
term. This provides a place for controls and other stratifications like
biological and technical replicates. Under `study-design` the
control definition has 2 different components:

- [control](https://www.ebi.ac.uk/ols/ontologies/bao/terms?iri=http%3A%2F%2Fwww.bioassayontology.org%2Fbao%23BAO_0000072)
  -- A controlled vocabulary of terms grouping controls by purpose. We'd
  like to consistently refer to things like positive and negative controls and
  currently subdivide into these categories:

   - `positive`
   - `negative`
   - `blank`
   - `parent` -- Identifying the control as derived from the original starting strain
   - `standard` -- Two or more samples of an analytical standard of known
     concentration from which we generate a curve for converting instrument
     response into units of the standard
   - `spike-in` -- A sample of known composition added to the plate during the
     assay process to control for assay quality and handling errors

- `control-context` -- Controls require specific experimental context to
  establish how to interpret them. We didn't find a specific ontology term to
  represent this (hence the `control` plus `context` extension), so are
  curious how others name and establish this type of context. They fall roughly
  into a couple of categories:

  - Expected detection amounts relative to other controls: [`very-high`, `high`,
    `medium-high`, `medium`, `medium-low`, `low`, `very-low`]
  - Defining interpretation of the control: [`growth`, `expression`, `background`, `activity`, `inhibition`]

Our goal is to provide constrained lists of choices covering the wide variety
of work we do, while retaining enough flexibility to define exactly what the
goal and use of a control is. To maintain restricted lists of choices, this required
breaking into 3 components and sourcing the options for those choices.
We'll continue to iterate on this as we model more experiments. For readers, how 
do these categories and choices reflect your experiences defining controls?

We welcome feedback and pointers to how other groups define and model biological
controls. Ideally we can define community standards that link directly to SBOL
experimental definition work. In the future, we'll continue to share
other ontology models we use, how we store and query them and how this enables
scientists to ask questions with our data.
