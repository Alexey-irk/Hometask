# Домашняя работа 10_1
## Создание виджета банковских операций клиента.
## Установка

1. Клонируйте репозиторий:
~~~
git clone https://git@github.com:Alexey-irk/Hometask.git 
~~~

2. Установите зависимости:
```
pip install -r requirements.txt
```

## Dev-зависимости
 
`mypy` (>=2.3.1,<3.0.0),  статическая проверка типов  
`black` (>=26.5.1,<27.0.0), форматирование кода  
`isort` (>=9.0.1,<10.0.0), сортировка импортов   
`flake8` (>=7.3.0,<8.0.0)" линтинг 

## Конфигурация

### 1. Настройки mypy
В `pyproject.toml`:

```toml
[tool.mypy]
disallow_untyped_defs = true
no_implicit_optional = true
warn_return_any = true
exclude = 'venv'
```

### 2. Настройки black / isort

```toml
[tool.black]
line-length = 119
check = true
diff = true

[tool.isort]
line_length = 119

```

## 3. Покрытие тестами

### Установка code coverage
~~~
poetry add --group dev pytest-cov 
~~~

### Покрытие кода составило 93%

