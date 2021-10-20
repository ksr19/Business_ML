# python-flask-docker
Итоговый проект курса "Машинное обучение в бизнесе"

Стек:

ML: sklearn, pandas, numpy
API: flask
Данные: с kaggle - https://www.kaggle.com/mnassrib/telecom-churn-datasets

Задача: оценить вероятность того, что пользователь отменит действующую подписку на услуги

Используемые признаки:

- Account length: integer
- International plan: string
- Number vmail messages: integer
- Total day minutes: double
- Total day calls: integer
- Total day charge: double
- Total eve minutes: double
- Total eve calls: integer
- Total eve charge: double
- Total night minutes: double
- Total night calls: integer
- Total night charge: double
- Total intl minutes: double
- Total intl calls: integer
- Total intl charge: double
- Customer service calls: integer 

Дополнительного преобразования признаков не производится, однако были созданы новые для улучшения качества модели. Детали содержатся в ноутбуке `project.ipynb`

Модель: GradientBoostingClassifier

### Клонируем репозиторий и создаем образ
```
$ git clone https://github.com/ksr19/Business_ML.git 
$ cd Business_ML/Project
$ docker build -t model . 
```

### Запускаем контейнер

```
$ docker run -d -p 8180:8180 -p 8181:8181 -v $(pwd)/model:/app/app/models model 
```

Переходим на localhost:8181 и вводим клиентские данные, после чего получаем вероятность того, что клиент отменит подписку
