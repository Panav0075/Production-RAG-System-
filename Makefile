install:
	pip install -r requirements.txt

test:
	pytest -q

evaluate:
	python -m src.evaluate

demo:
	python -m src.demo "How do I verify a webhook request?" --strategy hybrid
