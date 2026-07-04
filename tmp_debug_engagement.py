from backend.api.main import create_app
from fastapi.testclient import TestClient

app = create_app()
class S:
    def put(self, *a, **k):
        return None
    def get(self, *a, **k):
        return None
    def query(self, *a, **k):
        return iter([])
    def delete(self, *a, **k):
        return None

class P:
    engagement_store = S()
    secrets = type('SS', (), {'get_secret': lambda self, name: 'test-secret'})()

app.state.di_provided = P()
client = TestClient(app)
r = client.post('/v1/engagements/', json={'title':'T','description':'D'})
print('status', r.status_code)
print(r.text)
