# test_project
This project entended for avtomatic replacing of yaml atributes on GITHUB repository. 
 
Project consist of: 
1. API implemenation with two endpoints: update and delete yaml data. 
2. Directory "Temp" used for repository downloading.
3. Directory "tests" has everything related to project testing. 
* File "test_data. json" contains input data for API POST request. 
* File "test_del.json" containes input data for API DELETE request. 
* File "sample.yaml" used for unittesting.
* Files "test_yaml_change.py"and "test_api.py" is used for unittests functions update&delete data and API.
4.Tests repo "test_git_repo.git" is local repository for unittesting.


To for posting command to HTTP API following next commands: 

1.For update yaml files:
curl -F upload=@test_data.json -F press=OK http://127.0.0.1:5000/posting_file

2.For delete key and values in yaml file:
curl -F upload=@test_del.json -F press=OK http://127.0.0.1:5000/remove_elem
