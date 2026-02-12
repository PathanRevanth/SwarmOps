from fastapi.testclient import TestClient

from hiveops.api import app


client = TestClient(app)


def test_dashboard_endpoint():
    response = client.get('/')
    assert response.status_code == 200
    assert 'HiveOps Platform' in response.text
    assert 'Phase 3: MACOG-style IaC generation' in response.text


def test_health_endpoint():
    response = client.get('/health')
    assert response.status_code == 200
    payload = response.json()
    assert payload['status'] == 'ok'
    assert payload['agents'] == 5




def test_platform_screenshot_endpoint():
    response = client.get('/platform/screenshot')
    assert response.status_code == 200
    assert response.headers['content-type'].startswith('image/svg+xml')
    assert 'HiveOps Platform' in response.text




def test_alignment_plan_endpoint():
    response = client.get('/platform/plan/alignment')
    assert response.status_code == 200
    payload = response.json()
    assert payload['startup'] == 'HiveOps'
    assert len(payload['source_coverage']) == 3
    assert len(payload['execution_phases']) >= 5


def test_roadmap_endpoint():
    response = client.get('/platform/roadmap')
    assert response.status_code == 200
    payload = response.json()
    assert payload['product'] == 'HiveOps'
    assert len(payload['phases']) >= 5


def test_triage_endpoint():
    response = client.post(
        '/incidents/triage',
        json={
            'incident_id': 'INC-777',
            'service': 'payments-api',
            'symptom': 'error rate increase after release',
            'severity': 'critical',
            'environment': 'prod',
        },
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload['incident_id'] == 'INC-777'
    assert payload['service'] == 'payments-api'
    assert payload['environment'] == 'prod'
    assert len(payload['signals']) == 5
    assert payload['estimated_minutes_to_mitigate'] >= 1
    assert isinstance(payload['audit_recommendations'], list)


def test_iac_generate_endpoint():
    response = client.post(
        '/iac/generate',
        json={
            'intent': 'Create a high availability web service with secure defaults',
            'provider': 'aws',
        },
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload['provider'] == 'aws'
    assert 'resource "aws_vpc" "main"' in payload['terraform']
    assert len(payload['policy_checks']) >= 2


def test_pipelines_evolve_endpoint():
    response = client.post('/pipelines/evolve', json={'generation': 12})
    assert response.status_code == 200
    payload = response.json()
    assert payload['generation'] == 12
    assert payload['composite_fitness'] > 0
