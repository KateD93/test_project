# test_project

Using command for update yaml files
curl -F upload=@test_data.json -F press=OK http://127.0.0.1:5000/posting_file

Using command for delete key and values in yaml file:
curl -F upload=@test_del.json -F press=OK http://127.0.0.1:5000/remove_elem
