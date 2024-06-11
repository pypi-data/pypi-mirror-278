import os
from unittest.mock import patch

import pytest

from label_tree.diseases_tree import DiseaseTree
from label_tree.utils import plot_tree


@pytest.fixture
def disease_tree():
    return DiseaseTree()


def test_plot_tree(tmp_path, disease_tree):
    file_path = tmp_path / "diseases_tree.png"
    # Test that the function runs without errors
    plot_tree(disease_tree, path=file_path)
    # Assert that the file was created
    assert os.path.exists(file_path)


def test_pycairo_not_installed(tmp_path, disease_tree):
    with patch.dict("sys.modules", {"cairo": None}):
        with pytest.raises(
            ImportError, match="The pycairo package is required for plotting the tree."
        ):
            file_path = tmp_path / "diseases_tree.png"
            # Test that the function runs without errors
            plot_tree(disease_tree, path=file_path)
