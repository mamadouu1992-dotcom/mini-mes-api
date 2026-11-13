"""Tests des ordres de fabrication (nécessitent PostgreSQL)."""


def test_create_order(db_client):
    """Exemple complet : à lire avant d'écrire les tiens."""
    response = db_client.post("/orders", json={"product": "ANODE-A1", "planned_quantity": 10})

    assert response.status_code == 201
    data = response.json()
    assert data["product"] == "ANODE-A1"
    assert data["planned_quantity"] == 10
    assert data["status"] == "CREATED"


def test_create_order_with_invalid_quantity_is_rejected(db_client):
    response = db_client.post("/orders", json={"product": "ANODE-A1", "planned_quantity": 0})
    assert response.status_code == 422  # rejeté par la validation Pydantic


def test_get_unknown_order_returns_404(db_client):
    response = db_client.get("/orders/9999")
    assert response.status_code == 404


def create_started_order(client, quantity=2):
    """Crée un ordre et le démarre. Renvoie son id."""
    order_id = client.post("/orders", json={"product": "ANODE-A1", "planned_quantity": quantity}).json()["id"]
    client.patch(f"/orders/{order_id}/start")
    return order_id

# TODO : test_start_order
def test_start_order(db_client):
    order_id = db_client.post("/orders", json={"product": "ANODE-A1", "planned_quantity": 5}).json()["id"]

    response = db_client.patch(f"/orders/{order_id}/start")

    assert response.status_code == 200
    assert response.json()["status"] == "STARTED"

# TODO : test_cannot_complete_order_that_is_not_started
def test_cannot_complete_order_that_is_not_started(db_client):
    order_id = db_client.post("/orders", json={"product": "ANODE-A1", "planned_quantity": 5}).json()["id"]

    response = db_client.patch(f"/orders/{order_id}/complete")

    assert response.status_code == 409
    assert "Impossible de terminer un ordre au statut CREATED" in response.json()["detail"]
# TODO : test_add_part_to_started_order
def test_add_part_to_started_order(db_client):
    order_id = create_started_order(db_client, quantity=5)

    response = db_client.post(
        f"/orders/{order_id}/parts",
        json={"serial_number": "ANODE-A1-001", "quality_result": "GOOD"},
    )

    assert response.status_code == 201
    assert response.json()["work_order_id"] == order_id
    assert response.json()["quality_result"] == "GOOD"

# TODO : test_cannot_exceed_planned_quantity
def test_cannot_exceed_planned_quantity(db_client):
    order_id = create_started_order(db_client, quantity=1)

    first_response = db_client.post(
        f"/orders/{order_id}/parts",
        json={"serial_number": "ANODE-A1-001", "quality_result": "GOOD"},
    )
    assert first_response.status_code == 201

    response = db_client.post(
        f"/orders/{order_id}/parts",
        json={"serial_number": "ANODE-A1-002", "quality_result": "REJECTED"},
    )

    assert response.status_code == 409
    assert "Quantité prévue déjà atteinte" in response.json()["detail"]

# TODO : test_summary_calculates_yield
def test_summary_calculates_yield(db_client):
    order_id = db_client.post("/orders", json={"product": "ANODE-A1", "planned_quantity": 5}).json()["id"]

    response = db_client.get(f"/orders/{order_id}/summary")

    assert response.status_code == 200