import pytest

from label_tree.diseases_tree import DiseaseTree


@pytest.fixture
def label_version():
    return DiseaseTree()._label_version
