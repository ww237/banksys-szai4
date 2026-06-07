"""测试 Streamlit 主入口模块."""


class TestAppImports:
    """验证核心模块可正常导入."""

    def test_main_module_imports(self):
        import app.main  # noqa: F401

    def test_utils_module_imports(self):
        from app.utils import data_loader  # noqa: F401

    def test_model_package_imports(self):
        from app.model import __init__  # noqa: F401

    def test_pages_package_imports(self):
        from app.pages import __init__  # noqa: F401
