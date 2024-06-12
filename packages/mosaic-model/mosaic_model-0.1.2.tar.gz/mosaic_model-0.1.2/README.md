<h1 align="center" id="title">Mosaic Model</h1>

<p id="description">Here I collected some online and offline models for text tagging.</p>

<h2>🚀 Demo</h2>

[]()



<h2>🧐 Features</h2>

Here're some of the project's best features:

*   Online model: Rake Based Model. 10-20 it/sec
*   Offline models: Bart based model with summarisation. 1-5 it/sec
*   API model: YandexGPT based model. 1-2 it/sec

<h2>🛠️ Installation Steps:</h2>

<p>1. Installation</p>

```
pip install mosaic-model
```

<p>2. import</p>

```
from mosaic-model.models.rake_based_model import TagsExtractor
```

<p>3. Init tagger</p>

```
tagger = TagsExtractor()
```

<p>4. Get tags</p>

```
tagger.extract(some_text)
```
