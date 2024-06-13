### Tetun LID
Tetun Language Identification (Tetun LID) model is a machine learning model that automatically identifies the language of a given text. It was specifically designed to recognize four languages commonly spoken in Timor-Leste: Tetun, Portuguese, English, and Indonesian.

### Installation

With pip:

```
pip install tetun-lid joblib scikit-learn
```


### Usage

The examples of its usage are as follows:

1. To predict the language of an input text, use the `predict_language()` function.

```python

from tetunlid import lid

input_text = "Sé mak toba iha ne'ebá?"
output = lid.predict_language(input_text)

print(output)
```


This will be the output. (Note: The initial call may take a few minutes to complete as it will load the LID model.)

```
Tetun
```

2. To print the details of the Probability of being predicted to Tetun use the `predict_detail()` function.

```python

from tetunlid import lid

input_list_of_str = ["Sé mak toba iha ne'ebá?"]
output_detail = lid.predict_detail(input_list_of_str)
print('\n'.join(output_detail))
```

This will be the output:

```
Input text: "Sé mak toba iha ne'ebá?"
Probability:
        English: 0.0010
        Indonesian: 0.0014
        Portuguese: 0.0082
        Tetun: 0.9967
```


3. We can feed a mixed of corpus containing multiple languages into the LID model as the input list. Observe the following example:

```python
from tetunlid import lid

multiple_langs = ["Ha'u ema baibain", "I am not available",
                  "Apa kabar kawan?", "Estou a estudar"]

output = [(ml, lid.predict_language(ml)) for ml in multiple_langs]
print(output)
```

This will be the output:

```
[("Ha'u ema baibain", 'Tetun'), ('I am not available', 'English'), ('Apa kabar kawan?', 'Indonesian'), ('Estou a estudar', 'Portuguese')]
```

You can use print the output in the console as follows:

```python
from tetunlid import lid
import warnings
warnings.filterwarnings('ignore')

input_texts = ["Ha'u ema baibain", "I am not available",
                "Apa kabar kawan?", "Estou a estudar"]

for input_text in input_texts:
    lang = lid.predict_language(input_text)
    print(f"{input_text} ({lang})")
```

This will be the output:

```
Ha'u ema baibain (Tetun)
I am not available (English)
Apa kabar kawan? (Indonesian)
Estou a estudar (Portuguese)
```

To print the details of each input, use the same function as previously explained. Here is the example:

```python

from tetunlid import lid
import warnings
warnings.filterwarnings('ignore')

input_texts = ["Ha'u ema baibain", "I am not available",
                "Apa kabar kawan?", "Estou a estudar"]

output_multiple_details = lid.predict_detail(input_texts)
print('\n'.join(output_multiple_details))
```

This will be the output:

```
Input text: "Ha'u ema baibain"
Probability:
        English: 0.0032
        Indonesian: 0.0032
        Portuguese: 0.0028
        Tetun: 0.9907

Input text: "I am not available"
Probability:
        English: 0.9999
        Indonesian: 0.00001
        Portuguese: 0.00001
        Tetun: 0.00001

Input text: "Apa kabar kawan?"
Probability:
        English: 0.0011
        Indonesian: 0.9961
        Portuguese: 0.0015
        Tetun: 0.0184

Input text: "Estou a estudar"
Probability:
        English: 0.0003
        Indonesian: 0.002
        Portuguese: 0.9810
        Tetun: 0.0184
```

4. We can filter only Tetun text from a mixed of corpus containing multiple languages using the `predict_language()` function.

```python
from tetunlid import lid
import warnings
warnings.filterwarnings('ignore')


input_texts = ["Ha'u ema baibain", "I am not available",
                "Apa kabar kawan?", "Estou a estudar"]

output = [text for text in input_texts if lid.predict_language(text) == 'Tetun']
print(output)
```

This will be the output:

```
["Ha'u ema baibain"]
```


### Additional notes

1. If you encountered an `AttributeError: 'list' object has no attribute 'predict_proba'`, you might have some issues while installing the package. Please send me an email, and I will guide you on how to handle the error.
2. Please make sure that you use the latest version of Tetun LID by running this command in your console: `pip install --upgrade tetun-lid`.


### Citation
If you use this repository or any of its contents for your research, academic work, or publication, we kindly request that you cite it as follows:

````
@inproceedings{de-jesus-nunes-2024-labadain-crawler,
    title = "Data Collection Pipeline for Low-Resource Languages: A Case Study on Constructing a Tetun Text Corpus",
    author = "de Jesus, Gabriel  and
      Nunes, S{\'e}rgio Sobral",
    editor = "Calzolari, Nicoletta  and
      Kan, Min-Yen  and
      Hoste, Veronique  and
      Lenci, Alessandro  and
      Sakti, Sakriani  and
      Xue, Nianwen",
    booktitle = "Proceedings of the 2024 Joint International Conference on Computational Linguistics, Language Resources and Evaluation (LREC-COLING 2024)",
    month = may,
    year = "2024",
    address = "Torino, Italia",
    publisher = "ELRA and ICCL",
    url = "https://aclanthology.org/2024.lrec-main.390",
    pages = "4368--4380"
}
````

### Acknowledgement
This work is financed by National Funds through the Portuguese funding agency, FCT - Fundação para a Ciência e a Tecnologia under the PhD scholarship grant number SFRH/BD/151437/2021 (DOI 10.54499/SFRH/BD/151437/2021).


### License

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/gabriel-de-jesus/tetun-lid/blob/main/LICENSE)


### Contact Information
If you have any questions or feedback, please feel free to contact me at mestregabrieldejesus[at]gmail.com