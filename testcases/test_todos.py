import allure
import pytest

REQUIRED_TODO_FIELDS = {"userId", "id", "title", "completed"}

@allure.feature("待办事项接口")
class TestTodos:
    """测试 /todos 接口。"""

    @allure.story("查询详情")
    @allure.title("通过id查询待办详情")
    @pytest.mark.smoke
    def test_get_todo_by_id(self, api_client):
        response = api_client.get("todos/1")

        # HTTP 层
        assert response.status_code == 200
        assert response.headers.get("Content-Type", "").startswith(
            "application/json"
        )

        # 格式层
        todo = response.json()
        assert isinstance(todo, dict)
        assert REQUIRED_TODO_FIELDS <= todo.keys()

        # 业务层
        assert todo["id"] == 1
        assert isinstance(todo["userId"], int)
        assert isinstance(todo["title"], str)
        assert todo["title"]
        assert isinstance(todo["completed"], bool)

    @allure.story("按用户查询列表")
    @allure.title("通过用户查询一组待办")
    def test_get_todos_by_user(self, api_client):
        response = api_client.get(
            "todos",
            params={"userId": 1},
        )

        # HTTP 层
        assert response.status_code == 200
        assert response.headers.get("Content-Type", "").startswith(
            "application/json"
        )

        # 格式层
        todos = response.json()
        assert isinstance(todos, list)
        assert todos
        for todo in todos:
            assert isinstance(todo, dict)
            assert "userId" in todo
            assert "id" in todo
            assert "title" in todo
            assert "completed" in todo

        # 业务层
        for todo in todos:
            assert todo.get("userId") == 1
            assert isinstance(todo.get("id"), int)
            assert isinstance(todo.get("title"), str)
            assert todo.get("title")
            assert isinstance(todo.get("completed"), bool)

    @allure.story("查询详情")
    @allure.title("按id{todo_id}查询待办详情")
    @pytest.mark.parametrize("todo_id", [1, 2, 5, 10, 20])
    def test_get_todo_variants(self, api_client, todo_id):
        response = api_client.get(f"todos/{todo_id}")
        assert response.status_code == 200
        assert response.headers.get("Content-Type", "").startswith(
            "application/json"
        )

        todo = response.json()
        assert isinstance(todo, dict)
        assert "userId" in todo
        assert "id" in todo
        assert "title" in todo
        assert "completed" in todo

        assert todo.get("id") == todo_id
        todo_title = todo.get("title")
        assert isinstance(todo_title, str)
        assert todo_title
        assert isinstance(todo.get("completed"), bool)

    @allure.story("查询详情")
    @allure.title("查询不存在的待办事项")
    def test_get_todo_not_found(self, api_client):
        response = api_client.get("todos/9999")
        assert response.status_code == 404
        assert response.headers.get("Content-Type", "").startswith(
            "application/json"
        )
        body = response.json()
        assert body == {}

    @allure.story("新建todo")
    @allure.title("新建todo")
    def test_create_todo(self, api_client):
        new_todo = {
            "userId": 1,
            "title": "学习 pytest",
            "completed": False,
        }
        response = api_client.post("todos", payload=new_todo)
        assert response.status_code == 201
        assert response.headers.get("Content-Type", "").startswith(
            "application/json"
        )

        body = response.json()
        assert isinstance(body, dict)
        assert REQUIRED_TODO_FIELDS <= body.keys()

        assert body.get("userId") == new_todo.get("userId")
        assert body.get("title") == new_todo.get("title")
        assert body.get("completed") == new_todo.get("completed")
        assert isinstance(body.get("id"), int)
        assert body.get("id") > 0
