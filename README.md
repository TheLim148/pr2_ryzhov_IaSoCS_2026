# Unit Converter

Учебное CLI-приложение на Python для преобразования величин.

## Запуск

```bash
python converter.py CATEGORY VALUE FROM_UNIT TO_UNIT
```

Категории:

    length — длина;
    
    mass — масса;
    
    temperature — температура.

## Пакетное преобразование

Можно выполнить несколько преобразований из файла:

```bash
python converter.py --file batch.txt.example
```

Формат строки:

```text
CATEGORY;VALUE;FROM_UNIT;TO_UNIT
```

Пример:

```text
length;1;m;cm
mass;2;kg;g
temperature;0;c;f
```
