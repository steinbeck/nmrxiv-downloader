"""nmrxiv API client."""

from pathlib import Path
from typing import Any, Callable

import httpx

from .models import Dataset, Molecule, PaginatedResponse, Project, Study


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

    def list_projects(self, page: int = 1) -> PaginatedResponse:
        """List projects with pagination."""
        data = self._request("GET", f"/list/projects?page={page}")
        items = data.get("data", [])
        meta = data.get("meta", {})
        return PaginatedResponse(
            items=[Project(**item) for item in items],
            total=meta.get("total", len(items)),
            page=meta.get("current_page", page),
            per_page=meta.get("per_page", 100),
            last_page=meta.get("last_page", 1),
        )

    def list_studies(self) -> list[Study]:
        """List all studies."""
        data = self._request("GET", "/list/studies")
        items = data.get("data", data) if isinstance(data, dict) else data
        return [Study(**item) for item in items]

    def list_datasets(self, page: int = 1) -> PaginatedResponse:
        """List datasets with pagination."""
        data = self._request("GET", f"/list/datasets?page={page}")
        items = data.get("data", [])
        meta = data.get("meta", {})
        return PaginatedResponse(
            items=[Dataset(**item) for item in items],
            total=meta.get("total", len(items)),
            page=meta.get("current_page", page),
            per_page=meta.get("per_page", 100),
            last_page=meta.get("last_page", 1),
        )

    def get_item(self, item_id: str) -> dict[str, Any]:
        """Get item by identifier."""
        data = self._request("GET", f"/{item_id}")
        return data.get("data", data) if isinstance(data, dict) else data

    def search_molecules(
        self, query: str | None = None, smiles: str | None = None, page: int = 1
    ) -> PaginatedResponse:
        """Search molecules by name/synonym or SMILES substructure.

        Args:
            query: Search by compound name or synonym
            smiles: Search by SMILES substructure
            page: Page number (default 1)

        Returns:
            PaginatedResponse with Molecule objects
        """
        path = f"/search/{smiles}" if smiles else "/search"
        body = {}
        if query:
            body["query"] = query

        data = self._request("POST", path, json=body if body else None)
        items = data.get("data", [])
        return PaginatedResponse(
            items=[Molecule(**item) for item in items],
            total=data.get("total", len(items)),
            page=data.get("current_page", page),
            per_page=data.get("per_page", 24),
            last_page=data.get("last_page", 1),
        )

    def filter_datasets(
        self, experiment_type: str, page: int = 1
    ) -> PaginatedResponse:
        """Filter datasets by experiment type (client-side filtering).

        Args:
            experiment_type: Experiment type to filter (e.g., "hsqc", "1d-13c", "cosy")
            page: Page number to fetch

        Returns:
            PaginatedResponse with filtered Dataset objects.
            Note: total/last_page reflect the full dataset list, not filtered results.
        """
        response = self.list_datasets(page=page)

        def normalize(s: str) -> str:
            """Normalize string for comparison."""
            return " ".join(s.lower().replace("-", " ").replace("_", " ").split())

        search_term = normalize(experiment_type)
        filtered = [
            item
            for item in response.items
            if item.type and search_term in normalize(item.type)
        ]

        return PaginatedResponse(
            items=filtered,
            total=response.total,  # Note: this is total datasets, not filtered
            page=response.page,
            per_page=response.per_page,
            last_page=response.last_page,
        )

    def get_download_url(self, item_id: str) -> str | None:
        """Get download URL for an item.

        Args:
            item_id: Item identifier (e.g., P5, D410)

        Returns:
            Download URL if available, None otherwise
        """
        item = self.get_item(item_id)
        return item.get("download_url")

    def download_file(
        self,
        url: str,
        dest: Path,
        progress_callback: Callable[[int, int], None] | None = None,
    ) -> Path:
        """Download a file from URL with optional progress callback.

        Args:
            url: URL to download from
            dest: Destination path for the file
            progress_callback: Optional callback(downloaded_bytes, total_bytes)

        Returns:
            Path to the downloaded file
        """
        try:
            # Use a separate client for downloads (no base_url)
            with httpx.stream("GET", url, timeout=300.0, follow_redirects=True) as response:
                response.raise_for_status()
                total = int(response.headers.get("content-length", 0))

                with open(dest, "wb") as f:
                    downloaded = 0
                    for chunk in response.iter_bytes(chunk_size=8192):
                        f.write(chunk)
                        downloaded += len(chunk)
                        if progress_callback:
                            progress_callback(downloaded, total)

            return dest
        except httpx.HTTPStatusError as e:
            raise NmrXivError(
                f"Download failed: HTTP {e.response.status_code}",
                status_code=e.response.status_code,
            ) from e
        except httpx.RequestError as e:
            raise NmrXivError(f"Download failed: {e}") from e
