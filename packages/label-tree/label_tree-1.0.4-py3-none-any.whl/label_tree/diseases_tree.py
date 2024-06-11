import os
import re
import warnings
from typing import Optional

import boto3
import igraph as ig
import yaml
from dotenv import load_dotenv
from packaging import version

from label_tree.exceptions import UnknownDisease
from label_tree.utils import get_lateset_yaml_version

load_dotenv()

# AWS credentials
_AWS_DEFAULT_REGION = os.getenv("AWS_DEFAULT_REGION")
_AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
_AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
_S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
_S3_DIAGNOSIS_TREE_PATH = os.getenv("S3_DIAGNOSIS_TREE_PATH")
_S3_SYNONYMS_PATH = os.getenv("S3_SYNONYMS_PATH")


class DiseaseTree:
    def __init__(self, label_version: Optional[str] = None, skip_comments: bool = True):
        """
        A client getting the label tree data and serving it via an API.

        Args:
            label_version: The version of the label tree to use, a string
            representing SemVer (X.Y or X.Y.Z), if None, the latest version.
            skip_comments: Should we skip comment labels in the tree loading?
        """
        self._skip_comments = skip_comments
        self.tree = ig.Graph(directed=True)

        # Add name attribute to allow search on an empty tree
        self.tree.vs.set_attribute_values("name", [])

        # read data from s3
        s3_bucket = boto3.resource(
            service_name="s3",
            region_name=_AWS_DEFAULT_REGION,
            aws_access_key_id=_AWS_ACCESS_KEY_ID,
            aws_secret_access_key=_AWS_SECRET_ACCESS_KEY,
        ).Bucket(_S3_BUCKET_NAME)

        # Get the latest version if not provided
        if label_version is None:
            label_version = get_lateset_yaml_version(s3_bucket).base_version

        if get_lateset_yaml_version(s3_bucket) > version.parse(label_version):
            warnings.warn(
                "Newer version of diagnosis tree and synonyms are available in s3. "
                "Please update the library.",
                stacklevel=2,
            )
        self._label_version = label_version

        # Read diagnosis tree (not using os.path.join to be local os agnostic )
        diagnosis_tree_key = f"v{label_version}" + "/" + _S3_DIAGNOSIS_TREE_PATH
        response = s3_bucket.Object(diagnosis_tree_key).get()
        self.read_diagnosis_yaml(yaml.safe_load(response["Body"]))

        # Read synonyms
        synoyms_tree_key = f"v{label_version}" + "/" + _S3_SYNONYMS_PATH
        response = s3_bucket.Object(synoyms_tree_key).get()
        self.read_synonyms_yaml(yaml.safe_load(response["Body"]))

        # Tag the tree nodes with diagnosis status
        self._get_diagnosed_diseases()
        for v in self.tree.vs:
            v["is_diagnosed"] = self.check_if_diagnosed(v["name"])

    def _get_diagnosed_diseases(self):
        """
        Gets the diagnosed diseases from the latest checkpoint in the s3 bucket and
        stores them as part of object state.
        """
        # Connect to s3
        s3 = boto3.client("s3")

        # Get the latest checkpoint
        buckets = s3.list_buckets()["Buckets"]
        pattern = "classifier-production-checkpoints"
        matching_buckets = [bucket for bucket in buckets if pattern in bucket["Name"]]
        latest_checkpoint = max(matching_buckets, key=lambda x: x["CreationDate"])[
            "Name"
        ]

        # Get the list of objects in the latest checkpoint
        response = s3.list_objects_v2(Bucket=latest_checkpoint)
        file_names = [obj["Key"] for obj in response.get("Contents", [])]

        # Parse the labels from the file names
        diagnosed = [
            re.search(r"(?<=GPU\d_).+(?=_epoch)", s).group()
            for s in file_names
            if re.search(r"(?<=GPU\d_).+(?=_epoch)", s)
        ]

        self.diagnosed_diseases = []

        for d in diagnosed:
            try:
                self.diagnosed_diseases.append(self.get_canonial_form(d))
            except UnknownDisease:
                pass

    def normalize_disease(self, disease: str) -> str:
        """
        Normalize a given disease name.
        Removes non-letter characters and redundant
        whitespace and converts the name to lowercase.

        Args:
            disease: The disease name to be normalized.

        Returns:
            The normalized disease name.

        """
        disease = disease.lower()
        disease = disease.strip()
        bad_chars = ["-", "(", ")", "!", "*", "–", "_"]
        for char in bad_chars:
            disease = disease.replace(char, " ")
        disease = " ".join(disease.split())
        return disease

    def check_if_diagnosed(self, disease: str) -> bool:
        """Checks if a given disease is diagnosed.
        A diagnosed disease is a disease that is diagnosable
        by the production version of the app.

        Args:
            disease: The name of the disease to check.

        Returns:
            True if the disease is diagnosed, False otherwise.
        """
        return self.get_canonial_form(disease) in self.diagnosed_diseases

    def get_canonial_form(self, disease: str) -> str:
        """Get the canonical form of a given disease as represented in the label tree.

        Args:
            disease: The disease to get the canonical form for.

        Returns:
            The canonical form of the given disease.

        Raises:
            UnknownDisease: If the given disease is not found in the tree.
        """
        norm_disease = self.normalize_disease(disease)
        for v in self.tree.vs:
            if norm_disease == v["name"]:
                return v["orig_name"]
            for synonym in v["synonyms"]:
                if norm_disease == synonym:
                    return v["orig_name"]

        raise UnknownDisease(disease)

    def get_nearest_diagnosed_disease(self, disease: str) -> Optional[str]:
        """Get the nearest parent diagnosed disease of a given disease.

        Args:
            disease: The name of the disease.

        Returns:
            The name of the nearest parent diagnosed disease.
            None if no parent diagnosed disease is found.
        """
        canonical_name = self.normalize_disease(self.get_canonial_form(disease))
        n_reachable_vertices = 0
        nearset_diagnosed_disease = None
        for order in range(0, self.tree.vcount()):
            neighborhood = self.tree.neighborhood(
                canonical_name, order=order, mode="in"
            )
            if n_reachable_vertices == len(neighborhood):
                break
            n_reachable_vertices = len(neighborhood)
            for v in neighborhood:
                if self.tree.vs[v]["is_diagnosed"]:
                    nearset_diagnosed_disease = self.tree.vs[v]["orig_name"]
                    break
        return nearset_diagnosed_disease

    def _add_sub_disease(self, parent: str, disease: str):
        """
        Add a sub-disease to the parent disease in the tree.

        Args:
            parent: The name of the parent disease.
            disease: The name of the sub-disease to add.
        """
        norm_parent = self.normalize_disease(parent)
        norm_disease = self.normalize_disease(disease)

        # Check if parent and disease are the same
        if norm_parent == norm_disease:
            return

        # Check if parent exists
        if norm_parent not in self.tree.vs["name"]:
            return

        # Check that disease does not already exist
        if norm_disease in self.tree.vs["name"]:
            # Check that disease is not a parent of parent disease
            if self.tree.are_connected(norm_disease, norm_parent):
                return
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                # Check if exists a path from parent to disease
                if self.tree.get_shortest_paths(norm_parent, to=norm_disease)[0]:
                    return

        parent_id = self.tree.vs["name"].index(norm_parent)
        is_morphology_parent = self.tree.vs[parent_id]["is_morphology"]

        # Add disease to tree if needed
        if norm_disease not in self.tree.vs["name"]:
            self.tree.add_vertex(
                norm_disease,
                synonyms=[],
                is_morphology=is_morphology_parent,
                orig_name=disease,
            )

        # Add edge from disease to parent
        disease_id = self.tree.vs["name"].index(norm_disease)
        is_morphology_disease = self.tree.vs[disease_id]["is_morphology"]
        self.tree.add_edge(
            norm_parent,
            norm_disease,
            morphology_to_disease=(is_morphology_parent and not is_morphology_disease),
        )

    def _add_new_disease(self, disease: str, is_morphology: bool = False):
        """
        Add a new disease to the tree.

        Args:
            disease: The name of the new disease to add.
            is_morphology: Whether the disease is an ECG morphology or not.
        """
        norm_disease = self.normalize_disease(disease)
        # Check that disease does not already exist
        if norm_disease in self.tree.vs["name"]:
            return
        # Add disease to root node
        self.tree.add_vertex(
            norm_disease,
            synonyms=[],
            is_morphology=is_morphology,
            orig_name=disease,
        )

    def _read_diagnosis_yaml(self, disease: str, sub_diseases: list):
        """
        Add diseases and sub-diseases to the tree recursively.

        Args:
            disease: The name of the disease.
            sub_diseases: The list of sub-diseases.
        """
        # Add parent disease if not exists
        if self.normalize_disease(disease) not in self.tree.vs["name"]:
            self._add_new_disease(
                disease, is_morphology=disease == "ECG Morphology Abnormalities"
            )

        # Add sub diseases
        for sub_disease in sub_diseases:
            # Check if sub disease is a leaf
            if isinstance(sub_disease, str):
                self._add_sub_disease(disease, sub_disease)
            else:
                # Sub disease is not a leaf node from type dict
                child_disease = list(sub_disease.keys())[0]
                self._add_sub_disease(disease, child_disease)
                self._read_diagnosis_yaml(child_disease, sub_disease[child_disease])

    def read_diagnosis_yaml(self, diagnosis_dict: dict):
        """
        Read the diagnosis YAML and build the diagnosis tree.

        Args:
            diagnosis_dict: The dictionary representing the diagnosis tree.
        """
        for disease, sub_diseases in diagnosis_dict.items():
            # Skip comments
            if self._skip_comments and disease == "Comments":
                continue
            self._read_diagnosis_yaml(disease, sub_diseases)

    def read_synonyms_yaml(self, synonyms_dict: dict, strict: bool = False):
        """
        Reads a synonyms YAML and adds the synonyms to the tree.

        On strict mode, requires all nodes to exist and fails on synonym
        addition failure, on non-strict, just logs the nodes not found.

        Args:
            synonyms_dict: Dict which holds the yaml data
            strict: Strict vs. non-strict mode
        """
        for canonical, synonyms in synonyms_dict.items():
            if isinstance(synonyms, str):
                synonyms = [synonyms]
            for synonym in synonyms:
                try:
                    self.add_synonym(canonical, self.normalize_disease(synonym))
                except UnknownDisease as e:
                    if strict:
                        raise e
                    else:
                        pass

    def add_synonym(self, disease: str, synonym: str):
        """
        Add a synonym to the specified disease in the disease tree.

        Args:
            disease: The name of the disease.
            synonym: The synonym to be added.

        Raises:
            UnknownDisease: If the specified disease is not found in the disease tree.
        """
        norm_disease = self.normalize_disease(disease)
        norm_synonym = self.normalize_disease(synonym)
        if norm_disease not in self.tree.vs["name"]:
            raise UnknownDisease(disease)
        if norm_synonym in self.tree.vs["name"]:
            return
        disease_id = self.tree.vs["name"].index(norm_disease)
        if synonym not in self.tree.vs[disease_id]["synonyms"]:
            self.tree.vs[disease_id]["synonyms"].append(synonym)

    def is_morphology(self, disease: str) -> bool:
        """
        Check if a given disease is an ECG morphology.

        Args:
            disease: The name of the disease.

        Returns:
            True if the disease is an ECG morphology, False otherwise.

        Raises:
            UnknownDisease: If the given disease is not found in the tree.

        Notes:
            In case a disease appears in the tree both as a morphology and as a disease,
            the function will return False, as it reflects the disease being a valid
            diagnosis, and the inclusion in the morphology tree reflects the typical
            ECG findings.
        """
        norm_disease = self.normalize_disease(self.get_canonial_form(disease))
        if norm_disease not in self.tree.vs["name"]:
            raise UnknownDisease(disease)
        disease_id = self.tree.vs["name"].index(norm_disease)
        return self.tree.vs[disease_id]["is_morphology"]

    def get_synonyms(self, disease: str) -> set:
        """
        Retrieve the set of synonyms for a given disease.

        Args:
            disease: The name of the disease.

        Returns:
            A set of synonyms for the given disease.

        Raises:
            UnknownDisease: If the given disease is not found in the tree.
        """
        norm_disease = self.normalize_disease(self.get_canonial_form(disease))
        if norm_disease not in self.tree.vs["name"]:
            raise UnknownDisease(disease)

        disease_id = self.tree.vs["name"].index(norm_disease)
        return set(self.tree.vs[disease_id]["synonyms"])

    def get_child_diseases(self, disease: str) -> set:
        """
        Returns a set of child diseases for the given disease.

        Args:
            disease: The name of the disease.

        Returns:
            A set of child diseases.

        Raises:
            UnknownDisease: If the given disease is not found in the tree.
        """
        norm_disease = self.normalize_disease(self.get_canonial_form(disease))
        if norm_disease not in self.tree.vs["name"]:
            raise UnknownDisease(disease)

        # get disease's children
        out_edges = self.tree.es.select(_source=norm_disease)
        if not out_edges:
            return set()

        return {self.tree.vs[e.target]["orig_name"] for e in out_edges}

    def get_parent_diseases(self, disease: str) -> set:
        """
        Returns a set of parent diseases for the given disease.

        Args:
            disease: The name of the disease.

        Returns:
            A set of parent diseases.

        Raises:
            UnknownDisease: If the given disease is not found in the tree.
        """
        norm_disease = self.normalize_disease(self.get_canonial_form(disease))
        if norm_disease not in self.tree.vs["name"]:
            raise UnknownDisease(disease)

        # get disease's parents
        in_edges = self.tree.es.select(_target=norm_disease)
        if not in_edges:
            return set()

        return {self.tree.vs[e.source]["orig_name"] for e in in_edges}


def get_subtree(tree: DiseaseTree, label: str) -> set:
    """
    Get the all the children of a label, including the label itself.

    Reflects every string that may be considered equivalent to label in the tree,
    including synonyms, children and synonyms of the children.

    Args:
        tree: A DiseaseTree to search in.
        label: The label to get the subtree of.

    Returns: A set of all the children and synonyms of the label.
    """
    children = get_all_children(tree, label, with_synonyms=True)
    return children.union({tree.get_canonial_form(label)}).union(
        tree.get_synonyms(label)
    )


def get_all_children(tree: DiseaseTree, label: str, with_synonyms=False) -> set:
    """
    Get all children (including grandchildren, etc.) of a label in the tree.

    Args:
        tree: A DiseaseTree to search in.
        label: The label to get the children of.
        with_synonyms: Whether to include children nodes synonyms in the returned list.

    Returns: A set of all children of the label.
    """
    children_list = [
        {child}.union(get_all_children(tree, child))
        for child in tree.get_child_diseases(label)
    ]
    children_set = set().union(*children_list)

    if with_synonyms:
        children_set = children_set.union(
            *[tree.get_synonyms(child) for child in children_set]
        )

    return children_set


def get_all_parents(tree: DiseaseTree, label: str) -> set:
    """
    Get all parents (including grandparents, etc.) of a label in the tree.

    Args:
        tree: A DiseaseTree to search in.
        label: The label to get the parents of.

    Returns: A set of all parents of the label.
    """
    parents_list = [
        {parent}.union(get_all_parents(tree, parent))
        for parent in tree.get_parent_diseases(label)
    ]
    return set().union(*parents_list)
