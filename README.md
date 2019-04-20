## Clean and organize metadata with ontologies

In progress work to use NLP and [SciGraph](https://github.com/SciGraph/SciGraph)
for mapping unstructured metadata key value pairs to ontologies.

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

### Specify input key values

Contextual information nested in the keys:
```
ex485em528_raw
```

Multiple grouped keys:
```
Emission: ideal (nanometer)
Excitation: ideal (nanometer)
Value
Timepoint (second)
```

### Specify rules for mapping to ontologies

```
{:pat "^ex(?P<excitation>\d{3})em(?P<emission>\d{3})$" :search "fluorescence intensity" :type "float"}
{:pat "excitation" :ontology "BAO_0000566"}
{:pat "emission" :ontology "BAO_0000567"}
```

```
{:pat "excitation" :ontology "BAO_0000566" :ns "fluorescence"}
{:pat "emission" :ontology "BAO_0000567" :ns "fluorescence"}
{:pat "^value" :custom "value" :type "string" :ns "fluorescence"}
{:pat "^time(point)?$" :search "time measurement" :type "long" :ns "fluorescence"}
```

### Input ontologies

- [BioAssay Ontology (BAO)](http://bioassayontology.org/) -- screening assays
  and results
- [Sequence Ontology (SO)](http://www.sequenceontology.org/) -- description of
  sequence features in annotations

### Ideas to do

- Explore if [OpenRefine](https://github.com/OpenRefine/OpenRefine) helps
  over standard SciGraph queries
