# todo-api-tests

基于 Python、pytest 和 requests 的接口自动化测试练习项目。

## 当前范围

- `GET /todos/1`：获取单条待办事项。
- `GET /todos?userId=1`：按用户查询待办列表，逐项校验字段和业务数据。
- `GET /todos/{id}`：使用参数化覆盖多个待办 ID。
- `GET /todos/9999`：验证资源不存在时的 404 异常场景。
- `POST /todos`：创建待办事项，验证状态码、字段结构和响应回显。

当前共收集 9 条测试，覆盖 HTTP、响应结构和业务数据三层断言。

## 本地运行

```bash
cd /Users/mhj/TestLearning/todo-api-tests
source /Users/mhj/TestLearning/.venv/bin/activate
python -m pytest
```

只运行冒烟测试：

```bash
python -m pytest -m smoke
```

## 环境变量

```bash
export API_BASE_URL="https://jsonplaceholder.typicode.com"
export API_TIMEOUT="10"
```

没有设置环境变量时，项目会使用上面的默认值。

## Allure 报告

生成原始结果：

```bash
python -m pytest \
  --alluredir=test-results/allure-results \
  --clean-alluredir
```

生成并打开 HTML 报告：

```bash
allure generate test-results/allure-results \
  -o test-results/allure-report \
  --clean
allure open test-results/allure-report
```

## 项目结构

```text
config/settings.py       # 地址和超时配置
utils/api_client.py      # 统一请求封装
conftest.py              # 客户端 fixture
testcases/test_todos.py  # 待办事项接口测试
pytest.ini               # pytest 配置
.github/workflows/       # GitHub Actions CI
```

## 设计说明

- `ApiClient` 统一处理 URL、超时、Session 和日志，测试用例只负责业务断言。
- `api_client` fixture 使用 `function` 作用域，优先保证测试之间的状态隔离。
- `pytest.ini` 负责测试发现、日志、命令行参数和 `smoke` marker 注册。
- 测试数据通过 `parametrize` 与测试逻辑分离，每个参数生成独立测试节点。
- Allure 使用 `feature`、`story` 和 `title` 组织报告，参数化标题会显示实际 ID。

## CI/CD

GitHub Actions 在向 `main` 分支 push 或创建 Pull Request 时执行 CI：

1. 安装 Python 3.11、Java 17、Node.js 和项目依赖。
2. 执行 pytest，生成 JUnit 与 Allure 原始结果。
3. 使用 Allure CLI 生成 HTML 报告。
4. 上传 `test-results/` 作为可下载产物。

当 `main` 分支上的测试成功后，工作流继续执行 CD：

1. 将 Allure HTML 报告上传为 GitHub Pages 产物。
2. 自动部署到 GitHub Pages。
3. 通过仓库的 Pages 地址访问最新测试报告。

首次使用前，需要在 GitHub 仓库的 `Settings > Pages` 中把发布来源设置为
`GitHub Actions`。

JSONPlaceholder 的创建接口是模拟实现，不会真正持久化数据，因此本测试不验证创建后的再次查询。
