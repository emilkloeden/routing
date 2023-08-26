import inspect
from pathlib import Path
import os
import importlib.util
from typing import Generator, Callable, Optional

HttpMethod = str
ResponseFn = Callable
RouteStr = str


class RouteBuilder:
    PROJECT_DIR = Path(__file__).parent
    DEFAULT_ROUTES_DIR = PROJECT_DIR / "routes"
    REQUEST_METHODS = ("get", "post", "put", "patch", "delete")
    VALID_FILE_NAMES = [f"{method}.py" for method in REQUEST_METHODS]

    def __init__(self, routes_dir: Path = DEFAULT_ROUTES_DIR) -> None:
        self.routes_dir = routes_dir
        self.routes = self.construct_routes()

    def load_response_handler(self, file_path: str) -> Optional[Callable]:
        """Returns the `respond` function at file_path or None"""
        spec = importlib.util.spec_from_file_location(
            "module_name", self.routes_dir.joinpath(file_path)
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        fns = inspect.getmembers(module, inspect.isfunction)
        response_handlers = [fn for fn in fns if fn[0] == "respond"]
        if len(response_handlers):
            return response_handlers[0][1]
        return None

    def find_route_file_paths(
        self,
        routes_dir_path: Path = DEFAULT_ROUTES_DIR,
    ) -> Generator[Path, None, None]:
        """Yields all paths to all files in VALID_FILE_NAMES in any subdirectory
        of ROUTES_DIR"""
        if routes_dir_path.exists() and routes_dir_path.is_dir():
            for dirpath, _, filenames in os.walk(routes_dir_path):
                for filename in filenames:
                    if filename in self.VALID_FILE_NAMES:
                        full_file_path = Path(dirpath).joinpath(filename)
                        yield full_file_path

    def construct_routes(
        self,
    ) -> dict[RouteStr, dict[HttpMethod, ResponseFn]]:
        """Creates and returns a dictionary of path to route to a
        dictionary of HttpMethod to Response function."""
        routes = {}
        for route_file_path in self.find_route_file_paths(self.routes_dir):
            relative_posix_path_str = route_file_path.relative_to(
                self.routes_dir
            ).as_posix()
            for filename in self.VALID_FILE_NAMES:
                if relative_posix_path_str.endswith(filename):
                    route = "/" + relative_posix_path_str.removesuffix(
                        filename
                    ).removesuffix("/")
                    method = filename.removesuffix(".py")
                    if route not in routes:
                        routes[route] = {}
                    routes[route][method] = self.load_response_handler(
                        relative_posix_path_str
                    )
        return routes


def main() -> None:
    """Demo function, creates routes, then just calls the get route function for each"""
    route_builder = RouteBuilder()
    print(route_builder.routes)


if __name__ == "__main__":
    main()
