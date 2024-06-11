import unittest
from uuid import UUID

from mock import patch
from fastapi.testclient import TestClient

from delta.run.api import app, RunBase, RunBaseCreate
from delta.run.orchestrator import DeltaOrchestratorService

client = TestClient(app)


class TestApi(unittest.TestCase):

    def fake_get_run_by_id(self, run_id: str):
        return {"run": '"test_ok"', "inputs": 'in', "outputs": 'out'}

    def fake_get_runs(self):
        return {"runs": [{"run": '"test_ok"',
                          "inputs": 'in',
                          "outputs": 'out'},
                         {"run": '"test_ok"',
                          "inputs": 'in',
                          "outputs": 'out'}]}

    def fake_get_runs_ko(self):
        raise Exception("Error when get runs")

    async def fake_orchestrate(self, owner, twin_id, user_inputs):
        return {"run": '"test_ok"', "inputs": 'in', "outputs": "out"}

    async def fake_orchestrate_KO(self, owner, twin_id, user_inputs):
        raise Exception("Error when create run")

    async def fake_actifact(self):
        return {"run": '"test_ok"', "inputs": 'in', "outputs": 'out'}

    @patch.object(DeltaOrchestratorService, 'get_run_by_id',
                  fake_get_run_by_id)
    def test_get_runs(self):
        response = client.get("/runs/61cdd9a3-30e5-449c-ad23-e83d24fb25c9")
        print(response)
        print(response.json())
        self.assertIn("run", response.json())
        self.assertNotIn("test_ko", response.json())
        pass

    @patch.object(DeltaOrchestratorService, 'get_run_by_id',
                  fake_get_run_by_id)
    def test_get_404(self):
        response = client.get("/runs_twin")
        print(response)
        print(response.json())
        self.assertEqual(response.status_code, 404)
        pass

    @patch.object(DeltaOrchestratorService, 'get_run_by_id',
                  fake_get_run_by_id)
    def test_get_runs_error(self):
        response = client.get("/runs/11345")
        print(response)
        print(response.json())
        self.assertEqual(response.status_code, 422)
        pass

    @patch.object(DeltaOrchestratorService, 'get_runs', fake_get_runs)
    def test_get_runs_all(self):
        response = client.get("/runs")
        print(response)
        print(response.json())
        self.assertEqual(response.status_code, 200)
        pass

    @patch.object(DeltaOrchestratorService, 'get_runs', fake_get_runs_ko)
    def test_get_runs_all_exception(self):

        response = client.get("/runs")
        print(response)
        print(response.json())
        self.assertEqual(response.status_code, 500)

    @patch.object(DeltaOrchestratorService, 'orchestrate', fake_orchestrate)
    def test_create(self):

        run_context = RunBaseCreate(
            owner='test',
            twin_id='61cdd9a3-30e5-449c-ad23-e83d24fb25c9',
            user_inputs={})
        print(run_context.model_dump_json())
        response = client.post("/runs", data=run_context.model_dump_json())
        print(response)
        print(response.json())
        self.assertEqual(response.status_code, 201)

    @patch.object(DeltaOrchestratorService, 'orchestrate', fake_orchestrate_KO)
    def test_create_exception(self):

        run_context = RunBaseCreate(
            owner='test',
            twin_id='61cdd9a3-30e5-449c-ad23-e83d24fb25c9',
            user_inputs={})
        print(run_context.model_dump_json())
        response = client.post("/runs", data=run_context.model_dump_json())
        print(response)
        print(response.json())
        self.assertEqual(response.status_code, 500)
        pass

    @patch.object(DeltaOrchestratorService, 'orchestrate', fake_orchestrate)
    def test_create_ko(self):

        run_context = RunBase(
            owner='test',
            twin_id=UUID('61cdd9a3-30e5-449c-ad23-e83d24fb25c9'))
        print(run_context.model_dump_json())
        response = client.post("/runs", data=run_context.model_dump_json())
        print(response)
        print(response.json())
        self.assertEqual(response.status_code, 422)

    @patch.object(DeltaOrchestratorService, 'orchestrate', fake_actifact)
    def test_create_artifact(self):

        response = (
            client.post(
                "/runs/61cdd9a3-30e5-449c-ad23-e83d24fb25c9/artifacts"))
        print(response)
        print(response.json())
        self.assertEqual(response.status_code, 201)

    @patch.object(DeltaOrchestratorService, 'orchestrate', fake_orchestrate)
    def test_create_artifact_ko(self):

        response = client.post(
            "/runs/61cdd9a3-30e5-449c-ad23-e8c9/artifacts")
        print(response)
        print(response.json())
        self.assertEqual(response.status_code, 422)

    @patch.object(DeltaOrchestratorService, 'orchestrate', fake_actifact)
    def test_get_artifact(self):

        response = (
            client.get(
                "/runs/61cdd9a3-30e5-449c-ad23-e83d24fb25c9/artifacts"))
        print(response)
        print(response.json())
        self.assertEqual(response.status_code, 200)
