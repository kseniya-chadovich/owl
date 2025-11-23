import os
import time
import pytest
from fastapi.testclient import TestClient

from app.data_service import supabase_client
from app.data_service.main import app as data_app


class _FakeResponse:
    def __init__(self, data=None, error=None):
        self.data = data or []
        self.error = error


class _FakeTableOps:
    def __init__(self, store, table_name):
        self.store = store
        self.table_name = table_name
        self._filters = []
        self._single = False
        self._last_data = None

    def select(self, *_):
        return self

    def order(self, *_args, **_kwargs):
        return self

    def single(self):
        self._single = True
        return self

    def eq(self, column, value):
        self._filters.append((column, value))
        return self

    def insert(self, payload):
        return self._upsert(payload, allow_update=False)

    def upsert(self, payload):
        return self._upsert(payload, allow_update=True)

    def delete(self):
        rows = self.store.setdefault(self.table_name, [])
        filtered = self._apply_filters(rows)
        self.store[self.table_name] = [r for r in rows if r not in filtered]
        self._last_data = []
        return self

    def execute(self):
        if self._last_data is not None:
            data = self._last_data
        else:
            rows = self.store.setdefault(self.table_name, [])
            data = self._apply_filters(rows)
            if self._single and data:
                data = data[0]
        return _FakeResponse(data=data, error=None)

    def _apply_filters(self, rows):
        data = rows
        for col, val in self._filters:
            data = [r for r in data if r.get(col) == val]
        return data

    def _upsert(self, payload, allow_update):
        if isinstance(payload, list):
            for item in payload:
                self._upsert(item, allow_update)
            return self

        rows = self.store.setdefault(self.table_name, [])
        pk = "user_id" if self.table_name.startswith("student_") else "id"
        updated = False
        for idx, row in enumerate(rows):
            if pk in row and row.get(pk) == payload.get(pk):
                if allow_update:
                    rows[idx] = {**row, **payload}
                updated = True
                break

        if not updated:
            rows.append(payload.copy())
        self.store[self.table_name] = rows

        # Stamp conversation rows with updated_at for parity with Supabase
        if self.table_name == "student_conversations":
            payload = {**payload, "updated_at": payload.get("updated_at") or time.strftime("%Y-%m-%dT%H:%M:%SZ")}

        self._last_data = [payload]
        return self


class FakeSupabase:
    def __init__(self):
        self._store = {}

    def table(self, name):
        return _FakeTableOps(self._store, name)


@pytest.fixture(autouse=True)
def _fake_env():
    os.environ.setdefault("SUPABASE_URL", "http://example.supabase.co")
    os.environ.setdefault("SUPABASE_ANON_KEY", "test-anon-key")
    os.environ.setdefault("GOOGLE_API_KEY", "test-google-key")


@pytest.fixture
def supabase_mock(monkeypatch):
    fake = FakeSupabase()
    monkeypatch.setattr(supabase_client, "get_supabase", lambda: fake)
    # Ensure FastAPI routes use the fake too
    import app.data_service.main as data_main
    monkeypatch.setattr(data_main, "get_supabase", lambda: fake)
    return fake


@pytest.fixture
def data_client(supabase_mock):
    return TestClient(data_app)


@pytest.fixture
def ai_client(monkeypatch):
    from app.ai_service import main as ai_main
    from scripts import terminal_chat as tc

    class DummyClient:
        pass

    ai_main.user_state.clear()
    monkeypatch.setattr(ai_main, "client", DummyClient())
    monkeypatch.setattr(tc, "build_client", lambda: DummyClient())

    def fake_request_json(client, model_name, conversation_history, temperature):
        return '{"min_credits":12,"max_credits":12,"preferred_days":["M"],"no_days":[],"lunch_break":false,"no_mornings":false,"no_evenings":false,"prefer_mode":null,"avoid_professors":[]}'

    def fake_generate(payload, num_schedules):
        return [{"total_credits": 12, "courses": [], "progress_report": {}}]

    monkeypatch.setattr(tc, "request_json", fake_request_json)
    monkeypatch.setattr(tc, "generate_schedules_from_payload", fake_generate)

    return TestClient(ai_main.app)
