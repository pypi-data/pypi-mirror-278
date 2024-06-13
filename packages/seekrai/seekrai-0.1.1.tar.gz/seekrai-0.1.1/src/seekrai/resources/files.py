from __future__ import annotations

from pathlib import Path

from seekrai.abstract import api_requestor
from seekrai.filemanager import DownloadManager, UploadManager
from seekrai.seekrflow_response import SeekrFlowResponse
from seekrai.types import (
    FileDeleteResponse,
    FileList,
    FileObject,
    FilePurpose,
    FileResponse,
    SeekrFlowClient,
    SeekrFlowRequest,
)
from seekrai.utils import normalize_key


class Files:
    def __init__(self, client: SeekrFlowClient) -> None:
        self._client = client

    def upload(
        self, file: Path | str, *, purpose: FilePurpose | str = FilePurpose.FineTune
    ) -> FileResponse:
        upload_manager = UploadManager(self._client)

        if isinstance(file, str):
            file = Path(file)

        if isinstance(purpose, str):
            purpose = FilePurpose(purpose)

        assert isinstance(purpose, FilePurpose)

        return upload_manager.upload("flow/files", file, purpose=purpose, redirect=True)

    def list(self) -> FileList:
        requestor = api_requestor.APIRequestor(
            client=self._client,
        )

        response, _, _ = requestor.request(
            options=SeekrFlowRequest(
                method="GET",
                url="flow/files",
            ),
            stream=False,
        )

        assert isinstance(response, SeekrFlowResponse)
        files = [
            FileResponse(
                id=file["id"],
                filename=file["filename"],
                created_at=file["created_at"],
                object="file",
            )
            for file in response.data["data"]
        ]
        return FileList(object="list", data=files)

    def retrieve(self, id: str) -> FileResponse:
        requestor = api_requestor.APIRequestor(
            client=self._client,
        )

        response, _, _ = requestor.request(
            options=SeekrFlowRequest(
                method="GET",
                url=f"flow/files/{id}",
            ),
            stream=False,
        )

        assert isinstance(response, SeekrFlowResponse)

        return FileResponse(**response.data)

    def retrieve_content(
        self, id: str, *, output: Path | str | None = None
    ) -> FileObject:
        download_manager = DownloadManager(self._client)

        if isinstance(output, str):
            output = Path(output)

        downloaded_filename, file_size = download_manager.download(
            f"flow/files/{id}/content", output, normalize_key(f"{id}.jsonl")
        )

        return FileObject(
            object="local",
            id=id,
            filename=downloaded_filename,
            size=file_size,
        )

    def delete(self, id: str) -> FileDeleteResponse:
        requestor = api_requestor.APIRequestor(
            client=self._client,
        )

        response, _, _ = requestor.request(
            options=SeekrFlowRequest(
                method="DELETE",
                url=f"flow/files/{id}",
            ),
            stream=False,
        )

        assert isinstance(response, SeekrFlowResponse)

        return FileDeleteResponse(**response.data)


class AsyncFiles:
    def __init__(self, client: SeekrFlowClient) -> None:
        self._client = client

    async def upload(
        self, file: Path | str, *, purpose: FilePurpose | str = FilePurpose.FineTune
    ) -> None:
        raise NotImplementedError()

    async def list(self) -> FileList:
        requestor = api_requestor.APIRequestor(
            client=self._client,
        )

        response, _, _ = await requestor.arequest(
            options=SeekrFlowRequest(
                method="GET",
                url="flow/files",
            ),
            stream=False,
        )

        assert isinstance(response, SeekrFlowResponse)

        return FileList(**response.data)

    async def retrieve(self, id: str) -> FileResponse:
        requestor = api_requestor.APIRequestor(
            client=self._client,
        )

        response, _, _ = await requestor.arequest(
            options=SeekrFlowRequest(
                method="GET",
                url=f"flow/files/{id}",
            ),
            stream=False,
        )

        assert isinstance(response, SeekrFlowResponse)

        return FileResponse(**response.data)

    async def retrieve_content(
        self, id: str, *, output: Path | str | None = None
    ) -> FileObject:
        raise NotImplementedError()

    async def delete(self, id: str) -> FileDeleteResponse:
        requestor = api_requestor.APIRequestor(
            client=self._client,
        )

        response, _, _ = await requestor.arequest(
            options=SeekrFlowRequest(
                method="DELETE",
                url=f"flow/files/{id}",
            ),
            stream=False,
        )

        assert isinstance(response, SeekrFlowResponse)

        return FileDeleteResponse(**response.data)
