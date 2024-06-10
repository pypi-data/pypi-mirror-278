<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

- [mt-ai-python](#mt-ai-python)
  - [API SECRET KEY](#api-secret-key)
  - [Installation](#installation)
  - [Example](#example)
    - [Instantiate mtai](#instantiate-mtai)
    - [Static Use](#static-use)
    - [Resources](#resources)
    - [Contribution](#contribution)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# mt-ai-python
Python package for [MediaTranscribe](https://ai.mediatranscribe.com/) View on [pypi.python.org](https://pypi.org/project/mtai/)

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://img.shields.io/badge/license-MIT-blue.svg)
[![PyPI version](https://badge.fury.io/py/mtai.svg)](https://badge.fury.io/py/mtai)

## API SECRET KEY
Get your secret key from [https://ai.mediatranscribe.com/](https://ai.mediatranscribe.com/)
## Installation
```sh
pip install mtai
```
## Example
### Instantiate mtai
```python
from mtai.mt import MT
secret_key = "secret_key_here"
mt = MT(secret_key=secret_key)

# use tag class
print(mt.tags.list()) # list tags
print(mt.tags.create_from_title(title="Python Programming Language")) # create tags
print(mt.tags.create_from_title_summary("Python", "Python is a programming language")) # create tags
print(mt.tags.get_tag_by_id("664e033837511b57fa93dd2e")) # get a tag
print(mt.tags.delete_tag_by_id("664e033837511b57fa93dd2e")) # delete a tag
```

### Static Use
To start using the MTAI Python API, you need to start by setting your secret key.

You can set your secret key in your environment by running:

```sh
export SECRET_KEY = 'your_secret_secret_key'
```

After exporting the keys, you can use the api like this
```python
# work with tags
from mtai.tags import Tag
print(Tag.list())
print(Tag.create_from_title(title="Python Programming Language"))
print(Tag.create_from_title_summary("Python", "Python is a programming language"))
print(Tag.get_tab_by_id("664e033837511b57fa93dd2e"))
print(Tag.delete_tag_by_id("664e033837511b57fa93dd2e"))
```

### Resources
```python
Transcription
Tag
Prompt
Bio
Description
```

Please reference the **[docs](https://github.com/mediatranscribe/mt-ai-python/tree/main/docs)** folder for usage.

### Contribution
If you want to join, kindly see this **[contribution](https://github.com/mediatranscribe/mt-ai-python/tree/main/contribution.md)**