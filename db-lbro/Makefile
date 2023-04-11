run:
	python app/manage.py runserver 0.0.0.0:8080

migrate:
	python app/manage.py migrate

clean_db:
	mongo lbro --eval "printjson(db.dropDatabase())"

reset: clean_db migrate run
