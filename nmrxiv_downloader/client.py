"""nmrxiv API client."""

from typing import Any

import httpx

from .models import Dataset, Project, Study


class NmrXivError(Exception):
    """Exception for nmrxiv API errors."""

    def __init__(self, message: str, status_code: int | None = None):
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class NmrXivClient:
    """Client for nmrxiv.org REST API."""

    BASE_URL = "https://nmrxiv.org/api/v1"

    def __init__(self, timeout: float = 30.0):
        """Initialize client with configurable timeout."""
        self._timeout = timeout
        self._client: httpx.Client | None = None

    @property
    def client(self) -> httpx.Client:
        """Get or create httpx client."""
        if self._client is None:
            self._client = httpx.Client(
                base_url=self.BASE_URL,
                timeout=self._timeout,
                headers={"Accept": "application/json"},
            )
        return self._client

    def __enter__(self) -> "NmrXivClient":
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Context manager exit - cleanup client."""
        self.close()

    def close(self) -> None:
        """Close the HTTP client."""
        if self._client is not None:
            self._client.close()
            self._client = None

    def _request(self, method: str, path: str, **kwargs) -> Any:
        """Make HTTP request with error handling."""
        try:
            response = self.client.request(method, path, **kwargs)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise NmrXivError(
                f"HTTP {e.response.status_code}: {e.response.text}",
                status_code=e.response.status_code,
            ) from e
        except httpx.RequestError as e:
            raise NmrXivError(f"Request failed: {e}") from e

    def list_projects(self) -> list[Project]:
        """List all projects."""
        data = self._request("GET", "/list/projects")
        # Response is {"data": [...]}
        items = data.get("data", data) if isinstance(data, dict) else data
        return [Project(**item) for item in items]

    def list_studies(self) -> list[Study]:
        """List all studies."""
        data = self._request("GET", "/list/studies")
        items = data.get("data", data) if isinstance(data, dict) else data
        return [Study(**item) for item in items]

    def list_datasets(self) -> list[Dataset]:
        """List all datasets."""
        data = self._request("GET", "/list/datasets")
        items = data.get("data", data) if isinstance(data, dict) else data
        return [Dataset(**item) for item in items]

    def get_item(self, item_id: str) -> dict[str, Any]:
        """Get item by identifier."""
        data = self._request("GET", f"/{item_id}")
        # Response is {"data": {...}}
        return data.get("data", data) if isinstance(data, dict) else data
