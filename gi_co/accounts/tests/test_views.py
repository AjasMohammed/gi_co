import pytest
# import logging

# logger = logging.getLogger(__name__)

@pytest.mark.django_db
def test_add_user_data(api_client):
    """
    Test with csv data set.
    """
    with open("./data.csv", "rb") as file:
        files = {"user_data": file}
        response = api_client.post(
            "/accounts/user-data/", files, format="multipart"
        )
    data = response.data['data']  # retrive the response data.
    assert response.status_code == 200
    users = []
    for user in data:
        valid = True # flag to check if the data is valid
        if user['name'].strip() == "":  # if the "name" field is empty "name" field would be present in the status errors.
            assert bool(user['status']['errors'].get('name', False) )== True
            valid = False
        if int(user['age'])  > 120 or int(user['age']) <= 0:  # if the "age" field is out of required range "age" would be present in the status errors.
            assert bool(user['status']['errors'].get('age', False)) == True
            valid = False
        if user['email'] in users:  # if the email already exists the field "email" would be present in the status errors.
            assert bool(user['status']['errors']. get('email', False)) == True
            valid = False
        if "@" not in user['email'] or '.' not in user['email']:  # if the email is not valid the field "email" would be present in the status errors.
            assert bool(user['status']['errors']. get('email', False)) == True
            valid = False
        if valid:  # if the data is valid then it should have a status "created".
            assert user['status'] == 'created'
            users.append(user['email'])
    assert response.data['rejected'] == 3
    assert response.data['success'] == 10
    assert response.data['total'] == 13


def test_blank_file(api_client):
    """
    Testing API without sending a csv file.
    """
    files = {}
    response = api_client.post("/accounts/user-data/", files)
    # logger.info(response.data)
    assert response.status_code == 400
    assert response.data['message'] == 'Input file missing!'

def test_invalid_extention(api_client):
    """''
    Testing API with files other than csv.
    """
    with open("./test.py", "rb") as file:
        files = {"user_data": file}
        response = api_client.post("/accounts/user-data/", files)

    assert response.status_code == 400
    assert response.data["message"] == "Invalid file format!"
