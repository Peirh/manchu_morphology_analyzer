# manchu_morphology_analyzer
A simple rule-based morphological analyzer/morpheme splitter for Manchu. It can split verbs and nouns into stems and endings. 
The analyzer first test if a token is already included in dictionary entries of 新满汉大辞典, if so, it will not split. Otherwise, it will try to split the token into stem and suffixes, making sure that the stem can be found in the dictionary 新满汉大辞典.
Note that 新满汉大辞典 only includes non-inflected word forms in its dictionary entries.
Therefore, when encountering ambiguity (e.g. sere, oho), the morpheme splitter will not split. And when the token is out of the vocabulary, it will not split.

# install
```python
pip install --upgrade git+https://github.com/Peirh/manchu_morphology_analyzer.git
```

# usage
```python
from manchu_morphology_analyzer import manchu_morphology_analyzer

manchu_morphology_analyzer.noun_verb_splitter('manjui mafari i adali, muse sasa gabtambi')
```

If you want to split derivational suffixes, set split_derivational = True:
```python
manchu_morphology_analyzer.noun_verb_splitter('kadalara hafan elik sandari semin no cy uthai acanjimbi',
                                            split_derivational = True)
```