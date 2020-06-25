all: lint utest

lint:
	@flake8 --ignore=F401,F403,F405 test
	@flake8 --ignore=F401,F403,F405 dicomorg

utest:
	@pytest test
