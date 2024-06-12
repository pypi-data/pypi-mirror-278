# FreeLibreTranslateAPI

FreeLibreTranslateAPI - бесплатный API LibreTranslate. Данная библиотека является бесплатным решением API без использования API-ключа.

## Установка

Вы можете установить библиотеку с помощью `pip`:
```bash

pip install free-libretranslate-api

```

Или из исходников:
```bash

git clone https://codeberg.org/Ktoto/FreeLibreTranslateAPI

cd FreeLibreTranslateAPI

pip install .

```

## Использование

Пример использования библиотеки:

```python
from libre_translate_api import translate


answer = translate(
    query="Hello, world!", # Текст, который нужно перевести
    source_lang="auto", # Язык текста (auto - определить автоматически)
    target_lang="ru", # На какой язык перевести
    alternatives=3 # Кол-во альтернативных переводов (max = 3)
    )


print(answer.translated_text)  # Выведет переведенный текст
print(answer.alternatives) # Выведет список альтернативных вариантов
print(answer.detectedLanguage) # Информация об обнаруженном языке, если она доступна.  Может быть `None`, если информация об обнаруженном языке отсутствует. (Не None при source_lang = "auto")
```
