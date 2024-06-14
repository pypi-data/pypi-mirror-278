# Python client for UnderstandLabs

[![PyPi page link -- version](https://img.shields.io/pypi/v/understand-sdk.svg)](https://pypi.python.org/pypi/understand-sdk)

This is the official Python SDK for [UnderstandLabs](https://www.understandhq.com/)

## Getting Started

### Install

```sh
pip install understand-sdk

# or
# poetry add understand-sdk
```

### Configuration

```py
from understand_sdk.client import UnderstandPublicClient

# contact us at it@understandlabs.com for getting API key
client = UnderstandPublicClient(api_key="api key") 
```

### Usage

```py
from understand_sdk.story import StoryWithChannels

# create new story object
story = StoryWithChannels(
    title="A new awesome story",
    channels=[
        "general"
    ],
    slides=[
        # add your slides
    ]
)

# push a new story to Understand platform
client.create_story(story)
```

## Getting Help/Support

If you need help reach out to us at it@understandlabs.com.

## License

Licensed under the MIT license, see [`LICENSE`](LICENSE)
