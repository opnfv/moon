all: built run

built:
    docker build -t moon_policy:16.04 .

run:
    docker run -p 8000:8000 moon_policy:16.04

.PHONY: clean

clean:
    find . -name "*.py" -exec echo rm {}\;
