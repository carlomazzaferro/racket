
def test_info(init_project, client):
    res_health = client.get('/api/v1/model/active')
    assert res_health.status_code == 200
    assert isinstance(res_health.json, dict)
    assert res_health.json['model_name'] == 'test'

    res_health = client.get('/api/v1/model/all')
    assert res_health.status_code == 200
    assert isinstance(res_health.json, list)
    assert isinstance(res_health.json[0], dict)

    res_health = client.get('/api/v1/model/all?model_id=1')
    assert res_health.status_code == 200
    assert isinstance(res_health.json, dict)
    assert res_health.json['major'] == 0
    assert res_health.json['minor'] == 1

    res_health = client.get('/api/v1/model/scores?model_id=1')
    assert res_health.status_code == 200
    assert isinstance(res_health.json, list)
    assert isinstance(res_health.json[0], dict)
    assert res_health.json[0]['id'] == 1
