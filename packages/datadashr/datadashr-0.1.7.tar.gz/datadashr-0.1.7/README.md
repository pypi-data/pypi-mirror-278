![DataDashr Logo](https://www.datadashr.com/wp-content/uploads/2024/06/datadashr.svg)

## Description

Converse with Your Data Through Open Source AI.

Unleash the power of your data with natural language questions.  
Our open-source platform, built on Ollama, delivers powerful insights without the cost of APIs.

Integrate effortlessly with your existing infrastructure, connecting to various data sources including SQL, NoSQL, CSV, and XLS files.

Obtain in-depth analytics by aggregating data from multiple sources into a unified platform, providing a holistic view of your business.

Convert raw data into valuable insights, facilitating data-driven strategies and enhancing decision-making processes.

Design intuitive and interactive charts and visual representations to simplify the understanding and interpretation of your business metrics.

## Installation

To install the package, run the following command:

```bash
pip install datadashr
```

## Starting the Interface

To start the user interface, run the following command:

```bash
datadashr
```

## Usage Example

```python
from pprint import pprint
from datadashr import DataDashr
from datadashr.llm.ollama import OllamaLLM
from datadashr.connectors.pandas import CSVConnector

llm = OllamaLLM(model='codestral', params={"temperature": 0.0}, verbose=False)
connector = CSVConnector(filepath='data/titanic.csv')
df = DataDashr(data_connector=connector, llm_instance=llm, verbose=True, enable_cache=False, enable_vector=True, format_type='rich')
result = df.chat('show me the first 5 rows of the dataset')

pprint(result)
```
