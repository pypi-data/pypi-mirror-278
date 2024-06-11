import pytest

from label_tree.diseases_tree import (
    DiseaseTree,
    get_all_children,
    get_all_parents,
    get_subtree,
)
from label_tree.exceptions import UnknownDisease


@pytest.fixture
def disease_tree():
    return DiseaseTree()


def test_normalize_disease(disease_tree):
    assert (
        disease_tree.normalize_disease("Mobitz Type I (Wenckebach)")
        == "mobitz type i wenckebach"
    )
    assert (
        disease_tree.normalize_disease("AV Block - Third-degree (Complete)")
        == "av block third degree complete"
    )


def test_check_if_diagnosed(disease_tree):
    assert disease_tree.check_if_diagnosed("AV Block - First-degree")
    assert not disease_tree.check_if_diagnosed("De Winter T Wave")
    # Test synonyms
    assert disease_tree.check_if_diagnosed("AFIB")


def test_get_canonial_form(disease_tree):
    # Test that normalization is performed
    assert (
        disease_tree.get_canonial_form("Ventricular fibrillation")
        == "Ventricular Fibrillation"
    )
    # Test synonyms
    assert disease_tree.get_canonial_form("AF") == "Atrial Fibrillation"
    # Test that unknown diseases raise an error
    with pytest.raises(UnknownDisease):
        disease_tree.get_canonial_form("Test Disease")


def test_get_nearest_diagnosed_disease(disease_tree):
    # Test disease with diagnosed parent diseases
    assert (
        disease_tree.get_nearest_diagnosed_disease(
            "Pacing - Failure to inhibit - Atrial"
        )
        == "Pacing"
    )
    # Test disease with no diagnosed parent diseases
    assert disease_tree.get_nearest_diagnosed_disease("Sinoatrial Block") is None
    # Test disease that is diagnosed
    assert (
        disease_tree.get_nearest_diagnosed_disease("Atrial Fibrillation")
        == "Atrial Fibrillation"
    )
    # Test synonym
    assert disease_tree.get_nearest_diagnosed_disease("AF") == "Atrial Fibrillation"


def test_get_all_children(disease_tree):
    # Test disease with no children
    assert get_all_children(disease_tree, "Ashman Phenomenon") == set()
    # Test disease with children
    assert get_all_children(disease_tree, "Left Bundle Branch Block") == {
        "Intermittent Left Bundle Branch Block",
        "Complete Left Bundle Branch Block",
        "Incomplete Left Bundle Branch Block",
        "Left Anterior Fascicular Block",
        "Left Posterior Fascicular Block",
    }
    assert get_all_children(disease_tree, "Left Bundle Branch Block", True) == {
        "Complete Left Bundle Branch Block",
        "Incomplete Left Bundle Branch Block",
        "Intermittent Left Bundle Branch Block",
        "Left Anterior Fascicular Block",
        "Left Posterior Fascicular Block",
        "clbbb",
        "ilbbb",
        "lanfb",
        "lpfb",
    }
    # Test synonym
    assert get_all_children(disease_tree, "AF") == {
        "Paroxysmal Atrial Fibrillation",
        "Chronic Atrial Fibrillation",
        "Atrial Fibrillation with a Rapid Ventricular Rate",
        "Atrial Fibrillation with a Slow Ventricular Rate",
    }


def test_get_subtree(disease_tree):
    # Test disease with no children
    assert get_subtree(disease_tree, "Ashman Phenomenon") == {"Ashman Phenomenon"}

    # Test disease with children
    assert get_subtree(disease_tree, "Left Bundle Branch Block") == {
        "Left Bundle Branch Block",
        "Complete Left Bundle Branch Block",
        "Incomplete Left Bundle Branch Block",
        "Intermittent Left Bundle Branch Block",
        "Left Anterior Fascicular Block",
        "Left Posterior Fascicular Block",
        "lbbb",
        "left bundle branch block general",
        "clbbb",
        "ilbbb",
        "lanfb",
        "bundle branch block left lbbb",
        "lpfb",
    }


def test_get_all_parents(disease_tree):
    # Test disease with no parents
    assert get_all_parents(disease_tree, "Diagnoses Tree") == set()
    # Test disease with parents
    assert get_all_parents(disease_tree, "Asystole") == {
        "Diagnoses Tree",
        "Cardiac Arrest",
    }
    # Test synonym
    assert get_all_parents(disease_tree, "VF") == {
        "Abnormal QRS",
        "Cardiac Arrest",
        "Diagnoses Tree",
        "ECG Morphology Abnormalities",
        "Intraventricular Conduction Delay",
        "QRS - Prolonged",
        "Tachycardia",
        "Ventricular Rhythm",
        "Ventricular Tachycardia",
        "Wide-QRS Tachycardia",
    }


def test_is_morphology(disease_tree):
    # Test morphology disease
    assert disease_tree.is_morphology("Axis Deviation")
    # Test non-morphology disease
    assert not disease_tree.is_morphology("Atrial Fibrillation")
    # Test synonym
    assert not disease_tree.is_morphology("VF")
