build:
	python3.8 -m venv env
	(\
	. env/bin/activate; \
	pip install wheel; \
	pip install -r requirements.txt; \
	bash install-spacy-nlp-models.sh; \
	)
	

remove:
	rm -r env
    
run:
	python3 Trainer.py
