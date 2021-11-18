run_api:
	uvicorn albums_api:app --reload  # load web server with code autoreload  

test:
	pytest