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


# TODO : test_start_order
# TODO : test_cannot_complete_order_that_is_not_started
# TODO : test_add_part_to_started_order
# TODO : test_cannot_exceed_planned_quantity
# TODO : test_summary_calculates_yield
