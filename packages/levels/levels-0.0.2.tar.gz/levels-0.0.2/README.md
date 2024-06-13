# levels

A library to give a vertical view of nested data structures of any depth in Python.  
Nested data structures are common and can be hard to navigate and debug by hand/eye.   
Currently only supports dictionaries and lists (JSON-like structures).  

The base function (levels) gives a path and value for each key at a defined level.  

Useful when handling nested data structures in the REPL, iPython or Jupyter notebooks.  
Also useful for debugging and logging.  

If you are familiar with the glom library, this library plays a similar role but with a different approach.  
However, levels is not as feature-rich as glom and is not intended to be a replacement.  

levels allows you to get glom-like "recipes" / slices to play nicely in conjunction with glom.  
simply pass `glom=True` to the levels function.  

## Installation

```bash
pip install levels
```


### Short introduction to features

levels range from 0 - n, where 0 is the top level of the data structure.  

levels.levels() - returns a slice path and value for each key at a defined level.  
levels.get_level() - returns the level of a key or value in a dictionary.  
levels.find_path() - returns the full slice path to a value.  
levels.search() - returns the level of a value in a nested data structure.  


## Examples

```python
from levels import levels

nested_dict = {
    'a': {
        'b': {
            'c': 1,
            'd': 2
        },
        'e': 3
    },
    'f': {
        'g': {
            'h': [4,5]
        }
    }
}

for path, value in levels(nested_dict, 2):
    print(path, ":", value)

# ['a']['b']['c']: 1
# ['a']['b']['d']: 2
# ['f']['g']['h']: [...]
```

As can be seen this conveniently returns a path / "slice recipe" for the nested data structure.

Eyes saved!

levels is based on generators and will only consume memory and processing time if you let it run wild on big structures... 

### Advanced usage

```python
from levels import levels, get_level, find_path, search
import re

nested_dict = {
    'a': {
        'b': {
            'c': 1,
            'd': 2
        },
        'e': 3
    },
    'f': {
        'g': {
            'h': [4,5]
        }
    }
}

# Get the level of a key
print(get_level(nested_dict, key='a')) # 0
print(get_level(nested_dict, key='b')) # 1

# Get the level of a value
print(get_level(nested_dict, value=3)) # 1

# get path and value for a key
for path, value in levels(nested_dict, 2, key="h"):
    print(path, ":", value)

# get path and value for a key matching a regex
regex = re.compile(r"[d-f]") # match any letter between d and f

for path, value in levels(nested_dict, 2, regex_k=regex, values=True):
    print(path, ":", value)

# get path and value for a value matching a regex
value_regex = re.compile(r"[1-2]")  # match any digit between 1 and 2

for path, value in levels(nested_dict, 2, regex_v=value_regex):
    print(path, ":", value)

# search for a value and return the level
want = 4
level = search(nested_dict, value=want)

# get path and value for a value at a specific level (from search)
for path, value in levels(nested_dict, depth=level, value=want):
    print(path, ":", value)
# ['f']['g']['h'][0]: 4

# find_path: a convenience function, a combination of search and levels (returns only one path!)
want = 2
print(find_path(nested_dict, want)) # ['a']['b']['d']
```

## Using it from the command-line

```bash
python -m levels -h # prints help screen
```

### Examples

```bash
    #Print the values of the JSON file at level 2:
python -m levels data.json 2

```
