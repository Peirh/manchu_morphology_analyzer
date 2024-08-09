# manchu_morphology_analyzer
A simple rule-based morphological analyzer/morpheme splitter for Manchu. It can split verbs and nouns into stems and endings. When encountering ambiguity, the morpheme splitter will not split.

# install
pip install --upgrade git+https://github.com/Peirh/manchu_morphology_analyzer.git

# usage
from manchu_morphology_analyzer import manchu_morphology_analyzer

manchu_morphology_analyzer.noun_verb_splitter('manjui mafari i adali, muse sasa gabtambi')
