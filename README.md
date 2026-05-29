Структура репозитория

task1.py          # Сбор зависимостей проекта

task2.py          # Анализ уязвимостей через GitHub Security Advisory API

task3.py          # Формирование рекомендаций по устранению уязвимостей

task4.py          # Инвентаризация ОС и RPM-пакетов

requirements.txt

Подготовка окружения



Клонирование проекта и создание виртуального окружения:



git clone https://github.com/pytorch/pytorch.git

cd pytorch

git checkout v1.10.0



python3 -m venv venv

source venv/bin/activate



pip install requests packageurl-python


Задача 1. Сбор зависимостей



Запуск:



cd \~/lab3/pytorch

python ../task1.py



Результат:



result\_task\_1.json


Задача 2. Анализ уязвимостей через GitHub Security Advisory



Необходимо создать GitHub Personal Access Token и экспортировать его в переменную окружения:



export GITHUB\_TOKEN=<YOUR\_TOKEN>



Запуск:



cd \~/lab3

python task2\_graphql.py



Результат:



result\_task\_2.json


Задача 3. Формирование рекомендаций



Запуск:



python task3.py



Результат:



result\_task\_3.json


Задача 4. Инвентаризация операционной системы



Запуск:



python task4.py



Результат:



result\_task\_4.json


Задача 5. Анализ уязвимостей с использованием OSV-Scanner



Запуск:



./osv-scanner scan \~/lab3/pytorch --format json > result\_task\_5.json



Результат:



result\_task\_5.json

