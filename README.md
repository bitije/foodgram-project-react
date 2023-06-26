# Foodgram (сервис публикации и оценки рецептов)

### Запуск проекта

-  Клонировать репозиторий:

``` git clone https://github.com/vojdelenie/foodgram-project-react ```

-  Установить docker и запустить проект при помощи docker-compose:

```sudo docker-compose up -d --build```


-  Собрать статику:

```sudo docker-compose exec backend python manage.py collectstatic --noinput```


-  Применить миграции:

```sudo docker-compose exec backend python manage.py migrate --noinput```

-  Проект доступен по ip
