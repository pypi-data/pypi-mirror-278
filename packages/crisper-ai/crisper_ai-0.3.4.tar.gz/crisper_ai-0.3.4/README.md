

### Install SDK
```bash
pip install crisper-ai
```


### sdk.py usage

```python
from crisper_api_client import Crisper
assistant = Crisper.create_assistant(name="customer-support-bot")
```


## Add a knowlege source

```python
assistant.add_knowledge_source(content_type="pdf", pdf="https://www.example.com/frequently-asked-questions.pdf")
assistant.add_knowledge_source(content_type="url", pdf="https://help.example.com")
```

## Ask a query

```python
assistant.ask("How do I get a refund?")
```
