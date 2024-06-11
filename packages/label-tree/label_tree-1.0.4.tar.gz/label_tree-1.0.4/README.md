# Label Tree
A minimal client to access the label tree across BeatBoxAI applications

## Installation
Installation with pip from GitHub:
```
$ pip install git+https://github.com/Medpic/label-tree.git
```
To enable tree plotting, you need to install the package with the `viz` extra:
```
$  pip install 'label-tree[viz] @ git+https://github.com/Medpic/label-tree.git'
```

## Requirements

**You need a .env file with AWS credentials to access the label tree.**

## Usage
```python
from label_tree import DiseaseTree, get_all_children, get_all_parents, get_subtree
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

# Create a tree
tree = DiseaseTree()

# Get the canonical name of a label
canonical_name = tree.get_canonial_form("AF")

# Get direct children of a node
direct_children = tree.get_child_diseases("AF")

# Get direct parents of a node
direct_parents = tree.get_parent_diseases("AF")

# Check if label is "diagnosed" (aka. exists in tre production app)
is_diagnosed = tree.check_if_diagnosed("AF")

# Get the nearest diagnosed ancestor
nearest_diagnosed_ancestor = tree.get_nearest_diagnosed_disease("AF")

# Get all children of a node
children = get_all_children(tree, "AF")

# Get all children of a node, including synonyms
children_with_synonyms = get_all_children(tree, "AF", with_synonyms=True)

# Get the node subtree, including the node itself, children and synonyms
subtree = get_subtree(tree, "AF")

# Get all parents of a node
parents = get_all_parents(tree, "AF")

# Check if a node is an ECG morphology description
is_ecg_morphology = tree.is_morphology("AF")
```


## Development
To join the development of this repo:
- Clone the repo:
```commandline
git clone https://github.com/Medpic/label-tree.git
```
- Create a virtual environment (with your favorite tool) and install the library as editable:
```commandline
pip install -e .[dev,testing]
```
- Initialize the pre-commit hooks and run them to make sure things work:
```commandline
pre-commit
pre-commit run -a
```
- Run the tests:
```commandline
pytest
```
- You are good to go.
- Develop on small feature branches stemming from `master` and returning to `master` soon.
- Zen of python `python -c "import this"`
- Google's lovely python style guide: https://google.github.io/styleguide/pyguide.html
