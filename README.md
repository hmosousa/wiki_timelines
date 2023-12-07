# Wiki Timelines 

[<img src="https://huggingface.co/datasets/huggingface/brand-assets/resolve/main/hf-logo.png" alt="drawing" width="30"/>](https://huggingface.co/datasets/hugosousa/WikiTimelines)

## Overview

Wiki Timelines is a dataset that contains paragraphs of text along with annotation of the timeline of (some) events. This was accomplished by extracting sentences from Wikipedia that reference events with corresponding entries on WikiData that are anchored in time, *i.e.*, have start or end time. The resulting dataset is available in HuggingFace  

### Example

Consider the sentence from the [Russo-Ukrainian War article](https://en.wikipedia.org/wiki/Russo-Ukrainian_War):

> Following Ukraine's [Revolution of Dignity](https://en.wikipedia.org/wiki/Revolution_of_Dignity), Russia [annexed Crimea](https://en.wikipedia.org/wiki/Annexation_of_Crimea_by_the_Russian_Federation) from Ukraine and supported pro-Russian separatists fighting the Ukrainian military in the [Donbas war](https://en.wikipedia.org/wiki/War_in_Donbas).

This sentence mentions three WikiData entries: [Revolution of Dignity](https://www.wikidata.org/wiki/Q15733401), [Annexation of Crimea](https://www.wikidata.org/wiki/Q15920546), and [Donbas war](https://www.wikidata.org/wiki/Q16335075) that have a start an end time in WikiData (denoted by the property IDs `P580` and `P582`), allowing us to deduce a timeline of events, such as the one presented bellow:

> start Dignity < start Annexed < end Dignity < end Annexed < start War < end War  

As illustrated in the timeline above, in this dataset we represent each event into `start` and `end` points and annotate the timelines with the point relations between them. Between time points can only be three type of relations, namely: before (`<`), after (`>`), or equal (`=`).
 
 
By querying the count of entities with start dates (`P580`) yields 753,524, and end dates (`P582`) yields 655,013 using the query: 

```sparql
SELECT (COUNT(DISTINCT ?item) AS ?count) WHERE {?item wdt:P580 [].}
```

Therefore one can (expect to) automatically produce a large amount of timelines from  Wikipedia. This timelines can then be used to train or access the ability of models to generate timelines of events.  

## How to Use


1. **Create and activate a virtual environment**: To create, run: `python -m venv .venv`.  Then activate the environment: `source .venv/bin/activate`.

2. **Install dependencies**: `pip install . -e` and `pip install -r requirements.txt`    

3. **Entities Extraction**: Run the [scripts/scrape.py](scripts/scrape.py) script to extract all the entities and associated webpages from Wikidata:  `python scripts/scrape.py`

4. **Build Timelines**: Given the entities one can then run the [scripts/build_timelines.py](scripts/build_timeline.py) to deduce the timelines: `python scripts/build_timelines.py`


## License

This project is licensed under the [MIT License](LICENSE) - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

Special thanks to the Wikidata community for maintaining a valuable resource that enables projects like Wiki Timelines to flourish. 

![Powered by WikiData](https://upload.wikimedia.org/wikipedia/commons/thumb/a/ae/Wikidata_Stamp_Rec_Dark.svg/240px-Wikidata_Stamp_Rec_Dark.svg.png)
