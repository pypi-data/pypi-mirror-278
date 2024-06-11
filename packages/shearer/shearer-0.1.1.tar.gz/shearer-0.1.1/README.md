<h1 align="center">Shearer</h1>
<p align="center"><i>`shearer` is a large-languge model driven package to help you scrape webpage automatically.</i></p>

<div align="center">
  <a href="https://github.com/edwardmfho/shearer/stargazers"><img src="https://img.shields.io/github/stars/elangosundar/shearer" alt="Stars Badge"/></a>
<a href="https://github.com/edwardmfho/shearer/network/members"><img src="https://img.shields.io/github/forks/edwardmfho/shearer" alt="Forks Badge"/></a>
<a href="https://github.com/edwardmfho/shearer/pulls"><img src="https://img.shields.io/github/issues-pr/edwardmfho/shearer" alt="Pull Requests Badge"/></a>
<a href="https://github.com/edwardmfho/shearer/shearer/issues"><img src="https://img.shields.io/github/issues/edwardmfho/shearer" alt="Issues Badge"/></a>
<a href="https://github.com/edwardmfho/shearer/graphs/contributors"><img alt="GitHub contributors" src="https://img.shields.io/github/contributors/edwardmfho/shearer?color=2b9348"></a>
<a href="https://github.com/edwardmfho/shearer/blob/master/LICENSE"><img src="https://img.shields.io/github/license/edwardmfho/shearer?color=2b9348" alt="License Badge"/></a>
</div>

<br>

This repo helps you to extract the eye tag from a sourcecode for a webpage, whether it is a XML or HTML file, we can help you to get the relevant data as requested using large language model.

If you like this Repo, Please click the :star:

## Installation

You can install `shearer` using `pip install` or `poetry`

### Install via pip
```bash
pip install shearer
```
### Install via poetry
```bash
poetry add shearer
poetry install
```
## Usage
`shearer` currently supports only `XML` file but will aim to support `HTML` in the future.

### Getting Started
```bash
poetry install
poetry shell
```
### XML
To scrape a XML file into structured format. 

```python
from shearer.scraper import XMLScraper
from shearer.models import ScrappingOptions

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()

options = ScrappingOptions(model="gpt-4o", temperature=0.0, content_type="xml", required_data="author name, article title, article_url")
```

Once you have configure the options, we recommend you to get page_schema first
before scraping. THis will save you a lot of time in long run.

```
scraper = XMLScraper.from_input_options(client=client, options=options)
page_schema = scraper.get_site_schema(url="https://{substack_name}.substack.com/feed")

# Check the site schema
print(page_schema)
```

In the currently update, we introduce the concept of `key`. `key` refers
to the tag that capture all the required field you want. For example:

```
<rss>
  <item>
    <title>A great article</title>
    <author>John Doe</author>
  </item>
  <item>
    <title>A even better article</title>
    <author>Jane Doe</author>
  </item>  
</rss>
```

In this scenario, the `item` tag will be the `key` for the `page_schema`. 
It is important as it will help you organize your data in a structured 
format.

The page schema in Substack is slightly different from what we expected,
there is a required field outside of your `key` field.

One way to do it is manually modify the `page_schema`, remove the field that
is outside of your `key` field. So the modified `page_schema` will be like
the below:

```
updated_page_schema = {
    'rss': 
        {'channel': {
            'item': {
                'title': 'target_field', 
                'link': 'target_field',
                'dc:creator': 'target_field'
                }
            }
        }
    }
```

Then pass the new `page_schema` into the `scape` method.

```
output = scraper.scrape(
  url="https://{substack_name}.substack.com/feed",
  page_schema=updated_page_schema,
  key="item"
)

```
And done! You have extracted your first structured data. 


## Contributing
If you want to contribute to the project, do the following:

1. Create your feature branch (git checkout -b feature/AmazingFeature)
2. Commit your changes (git commit -m 'Add some AmazingFeature')
3. Push to the branch (git push origin feature/AmazingFeature)
4. Open a Pull Request

## License
This project is licensed under [MIT](https://opensource.org/licenses/MIT) license.
