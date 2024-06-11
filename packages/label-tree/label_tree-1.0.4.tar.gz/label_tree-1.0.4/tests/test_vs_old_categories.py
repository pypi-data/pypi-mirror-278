import os
from contextlib import redirect_stdout

import pytest

from label_tree.diseases_tree import DiseaseTree
from test_data.categories import dataset_lookup_dicts


@pytest.mark.parametrize("dataset", dataset_lookup_dicts.keys())
def test_dataset(dataset, label_version):

    with open(os.devnull, "w") as f, redirect_stdout(f):
        disease_tree = DiseaseTree(skip_comments=False, label_version=label_version)

    labels = []
    for label, synonyms in dataset_lookup_dicts[dataset].categories_lookup_dict.items():
        labels.append(label)
        if isinstance(synonyms, str):
            labels.append(synonyms)
        else:
            for s in synonyms:
                labels.append(s)

    for label in labels:
        disease_tree.get_canonial_form(label)
