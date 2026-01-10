import pytest
from fastapi.testclient import TestClient
from app.main import app, tasks_db, task_id_counter


@pytest.fixture
def client():
    """
    Fixture to create a test client for the FastAPI app.
    """
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_db():
    """
    Fixture to reset the in-memory database before each test.
    """
    global task_id_counter
    tasks_db.clear()
    # Reset the counter (we'll use a workaround since it's a module variable)
    yield
    tasks_db.clear()


class TestHealthEndpoint:
    """Tests for the health check endpoint."""
    
    def test_health_check_returns_200(self, client):
        """Health check should return 200 status code."""
        response = client.get("/health")
        assert response.status_code == 200
    
    def test_health_check_returns_healthy_status(self, client):
        """Health check should return healthy status."""
        response = client.get("/health")
        data = response.json()
        assert data["status"] == "healthy"
        assert data["message"] == "API is running"


class TestCreateTask:
    """Tests for task creation endpoint."""
    
    def test_create_task_success(self, client):
        """Should successfully create a task."""
        task_data = {
            "title": "Test Task",
            "description": "This is a test task",
            "completed": False
        }
        response = client.post("/tasks", json=task_data)
        assert response.status_code == 200
        
        data = response.json()
        assert data["title"] == "Test Task"
        assert data["description"] == "This is a test task"
        assert data["completed"] is False
        assert "id" in data
        assert "created_at" in data
    
    def test_create_task_with_minimal_data(self, client):
        """Should create a task with only title."""
        task_data = {"title": "Minimal Task"}
        response = client.post("/tasks", json=task_data)
        assert response.status_code == 200
        
        data = response.json()
        assert data["title"] == "Minimal Task"
        assert data["description"] is None
        assert data["completed"] is False
    
    def test_create_task_with_empty_title(self, client):
        """Should reject task with empty title."""
        task_data = {"title": "   ", "description": "Invalid"}
        response = client.post("/tasks", json=task_data)
        assert response.status_code == 400
        assert "empty" in response.json()["detail"].lower()
    
    def test_create_task_missing_title(self, client):
        """Should reject task without title."""
        task_data = {"description": "No title"}
        response = client.post("/tasks", json=task_data)
        assert response.status_code == 422  # Validation error


class TestGetTasks:
    """Tests for retrieving tasks."""
    
    def test_get_empty_tasks_list(self, client):
        """Should return empty list when no tasks exist."""
        response = client.get("/tasks")
        assert response.status_code == 200
        assert response.json() == []
    
    def test_get_all_tasks(self, client):
        """Should return all tasks."""
        # Create multiple tasks
        for i in range(3):
            client.post("/tasks", json={"title": f"Task {i}"})
        
        response = client.get("/tasks")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3
        assert all("title" in task for task in data)
    
    def test_get_single_task(self, client):
        """Should retrieve a specific task by ID."""
        # Create a task
        create_response = client.post("/tasks", json={"title": "Single Task"})
        task_id = create_response.json()["id"]
        
        # Retrieve it
        response = client.get(f"/tasks/{task_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Single Task"
        assert data["id"] == task_id
    
    def test_get_nonexistent_task(self, client):
        """Should return 404 for nonexistent task."""
        response = client.get("/tasks/999")
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()


class TestUpdateTask:
    """Tests for updating tasks."""
    
    def test_update_task_success(self, client):
        """Should successfully update a task."""
        # Create a task
        create_response = client.post("/tasks", json={"title": "Original"})
        task_id = create_response.json()["id"]
        
        # Update it
        update_data = {
            "title": "Updated Task",
            "description": "Updated description",
            "completed": True
        }
        response = client.put(f"/tasks/{task_id}", json=update_data)
        assert response.status_code == 200
        
        data = response.json()
        assert data["title"] == "Updated Task"
        assert data["description"] == "Updated description"
        assert data["completed"] is True
    
    def test_update_nonexistent_task(self, client):
        """Should return 404 when updating nonexistent task."""
        update_data = {"title": "Updated"}
        response = client.put("/tasks/999", json=update_data)
        assert response.status_code == 404
    
    def test_update_task_with_empty_title(self, client):
        """Should reject update with empty title."""
        # Create a task
        create_response = client.post("/tasks", json={"title": "Original"})
        task_id = create_response.json()["id"]
        
        # Try to update with empty title
        update_data = {"title": ""}
        response = client.put(f"/tasks/{task_id}", json=update_data)
        assert response.status_code == 400


class TestDeleteTask:
    """Tests for deleting tasks."""
    
    def test_delete_task_success(self, client):
        """Should successfully delete a task."""
        # Create a task
        create_response = client.post("/tasks", json={"title": "To Delete"})
        task_id = create_response.json()["id"]
        
        # Delete it
        response = client.delete(f"/tasks/{task_id}")
        assert response.status_code == 200
        assert "deleted successfully" in response.json()["message"].lower()
        
        # Verify it's gone
        get_response = client.get(f"/tasks/{task_id}")
        assert get_response.status_code == 404
    
    def test_delete_nonexistent_task(self, client):
        """Should return 404 when deleting nonexistent task."""
        response = client.delete("/tasks/999")
        assert response.status_code == 404


class TestTaskDataIntegrity:
    """Tests to ensure data integrity across operations."""
    
    def test_task_ids_are_unique(self, client):
        """Each task should have a unique ID."""
        task_ids = []
        for i in range(5):
            response = client.post("/tasks", json={"title": f"Task {i}"})
            task_ids.append(response.json()["id"])
        
        # All IDs should be unique
        assert len(task_ids) == len(set(task_ids))
    
    def test_created_at_timestamp_is_set(self, client):
        """Each task should have a created_at timestamp."""
        response = client.post("/tasks", json={"title": "Timestamp Test"})
        data = response.json()
        assert "created_at" in data
        assert data["created_at"] is not None
    
    def test_task_modifications_dont_affect_created_at(self, client):
        """Updating a task should not modify created_at."""
        # Create task
        create_response = client.post("/tasks", json={"title": "Original"})
        original_created_at = create_response.json()["created_at"]
        task_id = create_response.json()["id"]
        
        # Update task
        client.put(f"/tasks/{task_id}", json={"title": "Updated"})
        
        # Check created_at is unchanged
        get_response = client.get(f"/tasks/{task_id}")
        assert get_response.json()["created_at"] == original_created_at
