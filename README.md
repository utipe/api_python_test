# api_python_test
docker build -t=papi https://github.com/utipe/api_python_test.git


docker run -p 4000:80 -d papi

API is run on localhost:4000/api/
