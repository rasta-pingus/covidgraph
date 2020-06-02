# covidgraph
Graph generator for COVID data

![asciicast](man/demo.svg)

Input data formated as:
```json
{
    'date': date,
    'suspected': suspected,
    'discarded': discarded,
    'discarded_tested': discarded_tested,
    'confirmed': confirmed,
    'uti': uti,
    'healed': healed,
    'deaths': deaths
}
```
Data derived from input:
```
notifications = suspected + discarded + confirmed
tests = confirmed + discarded_tested
```