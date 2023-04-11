build:
	python3 -m venv .venv
	(\
	. .venv/bin/activate; \
	pip install -r requirements.txt; \
	)
	sudo apt install -y xvfb
	

remove:
	rm -r env

	
run:
	xvfb-run --server-args="-screen 0, 1920x1080x24"  python3 run.py --profile profile.json