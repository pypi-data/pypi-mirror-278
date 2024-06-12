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

# Перевод текста с английского на испанский
answer = translate("Hello, world!", "en", "es")
print(answer.translated_text)  # Вывод: Hola, mundo!
```
