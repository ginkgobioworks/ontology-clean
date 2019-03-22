## Clean and organize metadata with ontologies

In progress work to use [SciGraph](https://github.com/SciGraph/SciGraph) and
[OpenRefine](https://github.com/OpenRefine/OpenRefine) for mapping unstructured
metadata key value pairs to ontologies.

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

### Input ontologies

- [BioAssay Ontology (BAO)](http://bioassayontology.org/) -- screening assays
  and results
- [Sequence Ontology (SO)](http://www.sequenceontology.org/) -- description of
  sequence features in annotations
