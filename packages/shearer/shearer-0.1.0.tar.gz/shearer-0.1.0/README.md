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

We haven't wrap `shearer` as a package yet, but you can clone and use it locally.

```bash
git clone https://github.com/edwardmfho/python-llmscraper.git
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
from llmscraper.scraper import XMLScraper
from llmscraper.models import ScrappingOptions

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()

options = ScrappingOptions(model="gpt-4o", temperature=0.0, content_type="xml", required_data="author name, article title, article_url")

scraper = XMLScraper.from_input_options(client=client, options=options)
output = scraper.scrape(url="https://{substack_name}.substack.com/feed")
```
You can also get the schematic required.
```
scraper = XMLScraper.from_input_options(client=client, options=options)
output = scraper.get_site_schema(url="https://{substack_name}.substack.com/feed")
```

## Contributing
If you want to contribute to the project, do the following:

1. Create your feature branch (git checkout -b feature/AmazingFeature)
2. Commit your changes (git commit -m 'Add some AmazingFeature')
3. Push to the branch (git push origin feature/AmazingFeature)
4. Open a Pull Request

## License
This project is licensed under [MIT](https://opensource.org/licenses/MIT) license.
