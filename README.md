## Clean and organize metadata with ontologies

In progress work to use NLP and [SciGraph](https://github.com/SciGraph/SciGraph)
for mapping unstructured metadata key value pairs to ontologies.

### Specify input key values

With free text non-ontology keys, users can represent information in multiple
ways. For instance, a key can have contextual information on the experiment
nested within the keys:
```
ex485em528_raw,0.95
```
Or multiple keys representing the same information, with users needing to infer
grouping based on their knowledge of the experiment:
```
Emission: ideal (nanometer),528
Excitation: ideal (nanometer),485
Value,0.95
Timepoint (second),10
```

### Specify rules for mapping keys to ontologies

To map keys to ontologies, specify a set of rules which define the inputs
and ontology terms. The input is `pat`, a regular expression that matches
to the existing key/value pair. The regular expression can include references
to other patterns to help retrieve embedded information in a key. To map to
ontologies, either specify a search term which SciGraph uses to retrieve
the ontology or a specific ontology reference. You can also specify a type
where it is difficult to infer from the input values themselves. The first
key value example above maps with these rules:
```
{:pat "^ex(?P<excitation>\d{3})em(?P<emission>\d{3})$" :search "fluorescence intensity" :type "float"}
{:pat "excitation" :ontology "BAO_0000566"}
{:pat "emission" :ontology "BAO_0000567"}
```
For the second multi-key example, group together separate keys using a 
shared namespace, with the `ns` tag:
```
{:pat "excitation" :ontology "BAO_0000566" :ns "fluorescence"}
{:pat "emission" :ontology "BAO_0000567" :ns "fluorescence"}
{:pat "^value" :custom "value" :type "string" :ns "fluorescence"}
{:pat "^time(point)?$" :search "time measurement" :type "long" :ns "fluorescence"}
```

### Input ontologies

We ideally use [OBO Foundry](http://www.obofoundry.org/) ontologies:

- [Sequence Ontology (SO)](http://www.sequenceontology.org/) -- description of
  sequence features in annotations
- [Systems Biology Ontology (SBO)](http://www.ebi.ac.uk/sbo/main/)
- [BioAssay Ontology (BAO)](http://bioassayontology.org/) -- screening assays
  and results, not OBO but slimmer than NCIT
- The [Ontology for Biomedical Investigations (OBI)](http://purl.obolibrary.org/obo/obi)
- [Statistical Methods Ontology (STATO)](http://stato-ontology.org/)
- [Chemical Entities of Biological Interest ChEBI](http://www.ebi.ac.uk/chebi)

Other useful supplementary ontologies:

- [NCI Thesaurus (NCIT)](https://github.com/NCI-Thesaurus/thesaurus-obo-edition)
- [Semanticscience Integrated Ontology (SIO)](https://github.com/MaastrichtU-IDS/semanticscience)

Useful tools:

- [EBI Ontology Lookup Service (OLS)](https://www.ebi.ac.uk/ols/index)

## Usage

### Setup

Install data and tools:
```
bash get_data.sh
bash get_tools.sh
```
Load ontologies and run SciGraph server:
```
bash run_load.sh
bash run_service.sh
```


### Ideas to do

- Explore if [OpenRefine](https://github.com/OpenRefine/OpenRefine) helps
  over standard SciGraph queries
