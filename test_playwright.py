import pytest
import requests

BASE_URL = 'http://localhost:8000/tasks'

def send_request(method, url, data=None):
    headers = {"Content-Type": "application/json"}
    response = requests.request(method, url, json=data, headers=headers)
    return response.json(), response.status_code


def test_get_all_tasks():
    url = BASE_URL
    result, status_code = send_request('GET', url)

    assert status_code == 200
    assert isinstance(result['data'], list)

def test_create_task():
    url = BASE_URL
    data = {"title": "Test Task", "done": False}
    result, status_code = send_request('POST', url, data=data)

    assert status_code == 201
    assert 'id' in result['data']
    assert result['data']['title'] == data['title']
    assert result['data']['done'] == data['done']

def test_delete_task():
    url = BASE_URL
    data = {"title": "Task to Delete", "done": False}
    create_result, _ = send_request('POST', url, data=data)

    task_id = create_result['data']['id']

    delete_url = f'{BASE_URL}/{task_id}'
    result, status_code = send_request('DELETE', delete_url)

    assert status_code == 200
    assert result == {"message": f"Task #{task_id} deleted"}

    result, status_code = send_request('DELETE', delete_url)

    assert status_code == 404
    assert result['detail'] == f"Task #{task_id} doesn't exist"

def test_update_task():
    url = BASE_URL
    data = {"title": "Task to Update", "done": False}
    create_result, _ = send_request('POST', url, data=data)

    task_id = create_result['data']['id']

    update_url = f'{BASE_URL}/{task_id}'
    update_data = {"title": "Updated Task", "done": True}
    result, status_code = send_request('PUT', update_url, data=update_data)

    assert status_code == 200
    assert result['data']['title'] == update_data['title']
    assert result['data']['done'] == update_data['done']

    non_existing_update_url = f'{BASE_URL}/99999'
    result, status_code = send_request('PUT', non_existing_update_url, data=update_data)

    assert status_code == 404
    assert result['detail'] == "Task #99999 doesn't exist"

def test_invalid_data():
    url = BASE_URL
    invalid_data = {"title": "Invalid Task", "done": "not_a_bool"}
    result, status_code = send_request('POST', url, data=invalid_data)

    assert status_code == 422
    assert 'detail' in result

def test_missing_fields():
    url = BASE_URL
    incomplete_data = {"title": "Incomplete Task"}
    result, status_code = send_request('POST', url, data=incomplete_data)

    assert status_code == 422
    assert 'detail' in result
