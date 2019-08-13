# Representing measurements

Mirroring the diversity of design techniques for synthetic biology constructs,
there are numerous approaches for measuring and comparing the outputs of assays
to evaluate them. The measurement approaches are custom to the compound being
evaluated; they can range from proxy measures of enzyme activity based on
fluorescence to identification of output compounds. We aim to capture these
measurement outputs in a lightweight way, tying the ontology definitions back
with those describing the 
[experimental measurement intent](https://github.com/ginkgobioworks/ontology-clean/blob/master/docs/experimental_plate_labels.md),
[controls for normalization and standardization](https://github.com/ginkgobioworks/ontology-clean/blob/master/docs/representing_controls.md)
and [output activity reporting](https://github.com/ginkgobioworks/ontology-clean/blob/master/docs/activity_reporting.md).

## Compounds

Methods like
[GC-MS](https://en.wikipedia.org/wiki/Gas_chromatography%E2%80%93mass_spectrometry)
and
[LabChip](https://perkinelmer-appliedgenomics.com/home/nucleic_acid_analysis_protein_characterization/microfluidic-protein-characterization-analysis/labchip-gxii-touch-protein-characterization-system/)
provide direct assessment of chemicals of interest in an assay. Processing the
raw data from these into peak calls for compound measures requires
custom analyses we'll represent separately, and here focus on the output
measures.  We represent these as a set of enumerated compound names,
measurements and units:

- [compound](https://www.ebi.ac.uk/ols/ontologies/sbo/terms?iri=http%3A%2F%2Fbiomodels.net%2FSBO%2FSBO_0000240)
  -- The compound measured by the assay. Ideally this is linked to a defined set
  of [chemical terms like ChEBI](https://www.ebi.ac.uk/chebi/) with full
  [InChi](https://en.wikipedia.org/wiki/International_Chemical_Identifier) and 
  [IUPAC](https://en.wikipedia.org/wiki/IUPAC_nomenclature_of_organic_chemistry) chemical names along with common aliases.
- [measurement](https://www.ebi.ac.uk/ols/ontologies/iao/terms?iri=http%3A%2F%2Fpurl.obolibrary.org%2Fobo%2FIAO_0000109) -- The measurement value
- [unit](https://www.ebi.ac.uk/ols/ontologies/iao/terms?iri=http%3A%2F%2Fpurl.obolibrary.org%2Fobo%2FIAO_0000003) -- Unit for the measurement

Often a sample will have multiple compounds and measures
associated with an assay, potentially using different normalization techniques.

## Absorbance

Plate reader absorbance measurements have a readout value and the measured
wavelength:

- [absorbance](https://www.ebi.ac.uk/ols/ontologies/bao/terms?iri=http%3A%2F%2Fwww.bioassayontology.org%2Fbao%23BAO_0000070) -- The absorbance readout measurement
- [absorbance-wavelength](https://www.ebi.ac.uk/ols/ontologies/bao/terms?iri=http%3A%2F%2Fwww.bioassayontology.org%2Fbao%23BAO_0000568) -- The wavelength measured at (e.g. 600, 480)

## Fluorescence

Similarly, plate reader fluorescent measurements include the readout measurement
value along with the setting parameters for excitation and emission:

- [fluorescence-intensity](https://www.ebi.ac.uk/ols/ontologies/bao/terms?iri=http%3A%2F%2Fwww.bioassayontology.org%2Fbao%23BAO_0000363) -- the fluorescence intensity measurement value
- [excitation-wavelength](https://www.ebi.ac.uk/ols/ontologies/bao/terms?iri=http%3A%2F%2Fwww.bioassayontology.org%2Fbao%23BAO_0000566) -- The excitation wavelength for the measure
- [emission-wavelength](https://www.ebi.ac.uk/ols/ontologies/bao/terms?iri=http%3A%2F%2Fwww.bioassayontology.org%2Fbao%23BAO_0000567) -- The emission wavelength for the measure

## Shared context

These measurement methods often contain additional context that help with
interpretation and are not specific to any measurement approach. We handle these
similarly across multiple measurement types.

### Normalization

- [data-transformation](https://www.ebi.ac.uk/ols/ontologies/obi/terms?iri=http%3A%2F%2Fpurl.obolibrary.org%2Fobo%2FOBI_0200169) -- Describe the normalization or transformation method used for the data.

### Time Series

- [time-stamp](https://www.ebi.ac.uk/ols/ontologies/iao/terms?iri=http%3A%2F%2Fpurl.obolibrary.org%2Fobo%2FIAO_0000582) -- A date and time a measurement was taken in [ISO 8601 format](https://en.wikipedia.org/wiki/ISO_8601)
- [timepoint](https://www.ebi.ac.uk/ols/ontologies/iao/terms?iri=http%3A%2F%2Fpurl.obolibrary.org%2Fobo%2FIAO_0000416) -- An interval in a timepoint experiment, relative to some starting base time (e.g. 10 min, 1 hour)

### Labeling plate intent

- intent-label -- Provide a [experimental intent label](https://github.com/ginkgobioworks/ontology-clean/blob/master/docs/experimental_plate_labels.md) for the measurement.
