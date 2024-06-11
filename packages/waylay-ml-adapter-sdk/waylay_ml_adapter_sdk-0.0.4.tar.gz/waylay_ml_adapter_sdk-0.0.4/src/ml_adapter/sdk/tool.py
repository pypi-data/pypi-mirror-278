"""Service tool for the ml-adapters."""

import contextlib
import logging
from collections.abc import AsyncIterator
from functools import cached_property
from typing import Any, cast

from ml_adapter.api.data.common import V1_PROTOCOL
from ml_adapter.base.assets.manifest import ManifestSpec, WithManifest
from pydantic import TypeAdapter
from tenacity import retry, stop_after_delay, wait_exponential
from waylay.sdk import WaylayTool
from waylay.sdk.exceptions import WaylayError
from waylay.services.registry.api import PlugsApi, WebscriptsApi
from waylay.services.registry.service import RegistryService
from waylay.services.rules.service import RulesService

LOG = logging.getLogger(__name__)

# unlimited read timeout
STREAM_TIMEOUTS = (5.0, None, 5.0, 5.0)


class MLTool(WaylayTool):
    """MLAdapter utility service for the waylay client.

    Helps creating waylay webscripts and plugs that wrap a machine learning model.

    Loaded as tool with name `ml_tool` in the python sdk.

    #### Example
    ```python
    # create and test a simple model
    import numpy as np
    test_data = [1,2,3]
    expected_result = [2,4,6]
    doubler = lambda x: x*2
    assert np.array_equal(
        np.array(expected_result),
        doubler(np.array(test_data))
    )

    # wrap in an adapter, test remoting
    from ml_adapter.numpy import V1NumpyModelAdapter
    adapter=V1NumpyModelAdapter(model=doubler)
    test_resp == await adapter.call({"instances": test_data.tolist()})
    assert test_resp['predictions'] = expected_result.tolist()

    # use the ml_tool to deploy and test a webscript
    # configure logging to see what is happening
    import logging
    logging.basicConfig(level='INFO')
    from waylay.sdk import WaylayClient
    client = WaylayClient.from_profile('demo')

    ref = await client.ml_tool.create_webscript(
        adapter, name='MyMLWebscript', draft=True
    )
    ref = await client.ml_tool.wait_until_ready(ref)
    result = await client.ml_tool.test_webscript(ref, test_data)
    if expected_result.to_list() == result:
        await client.ml_tool.publish(ref)
    else:
        await client.ml_tool.remove(ref)
    ```
    """

    name = "ml_tool"
    title: str = "ML Adapter Tool"
    description: str | None = """
Helps creating waylay webscripts and plugs that wrap a machine learning model.
"""

    @cached_property
    def registry(self) -> RegistryService:
        """Get the registry SDK."""
        return self._services.require(RegistryService)

    @cached_property
    def rules(self) -> RulesService:
        """Get the registry SDK."""
        return self._services.require(RulesService)

    @cached_property
    def webscripts(self) -> WebscriptsApi:
        """Get the registry SDK."""
        return self.registry.webscripts

    @cached_property
    def plugs(self) -> PlugsApi:
        """Get the registry SDK."""
        return self.registry.plugs

    async def python_runtimes(self):
        """Check registry version."""
        resp = await self.registry.runtimes.list(
            query={"archiveFormat": ["python"]}, response_type=Any
        )
        return {r["functionType"]: r for r in resp["runtimes"]}

    async def create_webscript(
        self,
        adapter: WithManifest,
        manifest: ManifestSpec | None = None,
        name: str | None = None,
        version: str | None = None,
        runtime: str | None = None,
        comment: str = "",
        draft: bool = False,
        var_async: bool = True,
    ):
        """Create a webscript function from the given ml adapter.

        Parameters
        ----------
        adapter
            The _ml adapter_ object that holds the webscript definitions (assets).
        manifest
            Overrides for the _manifest_ of the webscript.
        name
            An override for the _name_ of the webscript
        version
            An override for the _version_ of the webscript.
        runtime
            An override for the _runtime_ used to create the webscript.
        comment
            A creation comment that is stored in the webscripts metadata.
        draft
            When `False` (default), once this call is succesfull, the webscript will be
            a _published_ webscript that can be used in the normal way,
            but its definition (script, deployment settings, ...)
            can only be changed through a new version (or name).

            When `True`, the webscript remains in the _draft_ phase,
            and you can only test it with an explicit _version_ mentioned.
            The definition of a _draft_ webscript version
            can still be replaced or updated.

            Use the `publish` command to afterwards _publish_
            a completed `draft` webscript.
        var_async
            When `True` (default), this call only _initiates_ the create of a webscript,
            and you should the seperate `wait_until_ready` call
            to follow up the deployment.

            When `False`, the calls blocks until the deployment is
            completed (without notification of any intermediate events).

        """
        manifest = manifest or {}
        if name:
            manifest = {**manifest, "name": name}
        if version:
            manifest = {**manifest, "version": version}
        if runtime:
            manifest = {**manifest, "runtime": runtime}
        adapter = adapter.as_webscript(manifest)
        await adapter.save()
        with contextlib.ExitStack() as stack:
            # uses ExitStack.enter_context to close files afterwards.
            files = {
                asset.full_path: stack.enter_context(open(asset.location, "br"))
                for asset in adapter.assets.iter(
                    recursive=True,
                    include_dir=False,
                    exclude_empty=True,
                )
            }
            result = await self.webscripts.create(
                files=files,
                query={"draft": draft, "comment": comment, "async": var_async},
                response_type=Any,
            )
        return result

    async def create_plug(
        self,
        adapter: WithManifest,
        manifest: ManifestSpec | None = None,
        states: list | None = None,
        inputs: dict | None = None,
        outputs: dict | None = None,
        name: str | None = None,
        version: str | None = None,
        runtime: str | None = None,
        comment: str = "",
        draft: bool = False,
        var_async: bool = True,
    ):
        """Create a plug function from the given ml adapter.

        Parameters
        ----------
        adapter
            The _ml adapter_ object that holds the webscript definitions (assets).
        manifest
            Overrides for the _manifest_ of the webscript.
        states
            The interface documentation of the possible output states.
        inputs
            The interface documentation of the input properties.
        outputs
            The interface documentation of the possible outputs properties (_rawData_).
        name
            An override for the _name_ of the webscript
        version
            An override for the _version_ of the webscript.
        runtime
            An override for the _runtime_ used to create the webscript.
        comment
            A creation comment that is stored in the webscripts metadata.
        draft
            When `False` (default), once this call is succesfull, the webscript will be
            a _published_ webscript that can be used in the normal way,
            but its definition (script, deployment settings, ...)
            can only be changed through a new version (or name).

            When `True`, the webscript remains in the _draft_ phase,
            and you can only test it with an explicit _version_ mentioned.
            The definition of a _draft_ webscript version
            can still be replaced or updated.

            Use the `publish` command to afterwards _publish_
            a completed `draft` webscript.
        var_async
            When `True` (default), this call only _initiates_ the create of a webscript,
            and you should the seperate `wait_until_ready` call
            to follow up the deployment.

            When `False`, the calls blocks until the deployment is
            completed (without notification of any intermediate events).

        """
        manifest = manifest or {}
        if name:
            manifest = {**manifest, "name": name}
        if version:
            manifest = {**manifest, "version": version}
        if runtime:
            manifest = {**manifest, "runtime": runtime}
        interface = manifest.get("interface") or {}
        interface_doc = manifest.get("metadata", {}).get("interface", {})
        if states:
            interface["states"] = states
            manifest["interface"] = interface
            interface_doc.pop("states", None)
        if inputs:
            interface["inputs"] = inputs
            manifest["interface"] = interface
            interface_doc.pop("inputs", None)
        if outputs:
            interface["outputs"] = outputs
            manifest["interface"] = interface
            interface_doc.pop("outputs", None)
        adapter = adapter.as_plug(manifest)
        await adapter.save()
        with contextlib.ExitStack() as stack:
            # uses ExitStack.enter_context to close files afterwards.
            files = {
                asset.full_path: stack.enter_context(open(asset.location, "br"))
                for asset in adapter.assets.iter(
                    recursive=True,
                    include_dir=False,
                    exclude_empty=True,
                )
            }
            result = await self.plugs.create(
                files=files,
                query={"draft": draft, "comment": comment, "async": var_async},
                response_type=Any,
            )
        return result

    async def wait_until_ready(
        self,
        resp: dict,
        logger: logging.Logger | None = None,
        success_states=("running",),
    ):
        """Wait for a webscript to be running.

        Parameters
        ----------
        resp
            The output of `create_plug` or `create_webscript`
            as a reference to the webscript.
            If not available, use the result of
            `await client.webscript.get(name, version, response_type=Any)`.
        logger:
            The logger on which to report progress events.
            Uses a default logger of this package if not set.
        success_states
            The function entity states that is considered successfull
            (normally `running`).
            Set e.g. to `('running', 'unhealthy', 'failed')`
            to always return when completed.

        """
        entity = resp["entity"]
        status = entity["status"]
        as_webscript = entity.get("webscript", False)
        as_plug = entity.get("plug", False)
        event_href = resp.get("_links", {}).get("event", {}).get("href", None)
        ref = as_webscript or as_plug
        name = ref["name"]
        version = ref["version"]
        logger = logger or LOG
        if status not in success_states:
            if not event_href:
                if as_plug:
                    jobs_resp = await self.plugs.get(name, version, response_type=Any)
                else:
                    jobs_resp = await self.webscripts.get(
                        name, version, response_type=Any
                    )
                event_href = (
                    jobs_resp.get("_links", {}).get("event", {}).get("href", None)
                )
            logger.info("Waiting for %s@%s to be ready:", name, version)
            if not event_href:
                raise WaylayError("no event link available")
            logger.info("listening on %s", event_href)
            _last_event = await self.log_events(event_href, logger)
            result: dict[str, Any] = {}
            if as_webscript:
                result = await self.webscripts.get(name, version, response_type=Any)
            else:
                result = await self.plugs.get(name, version, response_type=Any)
            status = result["entity"]["status"]
        logger.info("function %s@%s has status %s", name, version, status)
        if status in success_states:
            return result
        raise WaylayError(
            f"Deployment failed: {result['entity'].get('failureReason','')}"
        )

    def _log_event(self, event: dict, logger: logging.Logger | None = None):
        logger = logger or LOG
        event_type = event.get("event")
        if event_type is None:
            logger.warning("%s", event)
            return None
        event_data = event.get("data", {})
        event_info = event_data
        if not isinstance(event_info, dict):
            logger.info("%s: %s", event_type, event_info)
            return event_type
        job = event_info.get("job", {})
        job_type = job.get("type", "")
        if job_type == "":
            logger.info("%s: %s", event_type, event_info)
            return event_type
        func = event_info.get("function", {})
        func_name = func.get("name", "")
        func_version = func.get("version", "")
        func_ref = f"{func_name}@{func_version}" if func else ""
        event_log = f"{func_ref} {job_type}: {event_type}"
        if event_type in ["completed", "failed"]:
            event_log += f"\n{event_info}"
        logger.info("%s", event_log)
        return event_type

    async def log_events(
        self,
        query_or_url: str | dict,
        logger: logging.Logger | None = None,
        close_on_event: tuple[str] = ("close",),
    ):
        """Log job events for the given url or query.

        Parameters
        ----------
        query_or_url
            The events query, or event url to poll.
            See [events API](https://docs.waylay.io/openapi/public/redocly/registry.html#tag/Jobs/operation/events_jobs)
        logger
            The logger to use to report events.
        close_on_event
            The event types that will terminate polling.

        """
        iter_events = await self.iter_events(query_or_url)
        async for event in iter_events:
            event_type = self._log_event(event, logger)
            if event_type in close_on_event:
                return event

    async def iter_events(self, query_or_url: str | dict) -> AsyncIterator:
        """Iterate over job events.

        Parameters
        ----------
        query_or_url
            The events query, or event url to poll.
            See [events API](https://docs.waylay.io/openapi/public/redocly/registry.html#tag/Jobs/operation/events_jobs)

        """
        if isinstance(query_or_url, str):
            return cast(
                AsyncIterator,
                await self.registry.api_client.request(
                    "GET",
                    query_or_url,
                    stream=True,
                    timeout=STREAM_TIMEOUTS,
                    response_type=Any,
                ),
            )
        else:
            return await self.registry.jobs.events(
                query=query_or_url,
                stream=True,
                timeout=STREAM_TIMEOUTS,
                validate_request=False,
                response_type=Any,
            )

    async def test_webscript(self, ref: dict, instances, **kwargs):
        """Test invocation of a deployed ml function.

        Parameters
        ----------
        ref
            The output of `create_plug`, `create_webscript` or
            `wait_until_ready` as a reference to the webscript.
            If not available, use the result of
            `await client.webscript.get(name, version, response_type=Any)`.
        instances
            the tensor data that will be provided as `instances`
        kwargs
            any request arguments passed on to the `api_client.request` call, e.g.
            a `timeout` or `headers`.

        """
        invoke_link = ref["_links"]["invoke"]
        if not invoke_link:
            raise WaylayError("No invocation link available")
        resp = await self.api_client.request(
            "POST",
            invoke_link["href"],
            json={"instances": instances},
            raw_response=True,
            response_type=Any,
            **kwargs,
        )
        data = resp.json()
        data = data.get("predictions", data)
        return data

    async def test_plug(self, ref: dict, data, protocol=V1_PROTOCOL, **kwargs):
        """Test invocation of a deployed ml function.

        ref
            The output of `create_plug`, `create_webscript` or
            `wait_until_ready` as a reference to the webscript.
            If not available, use the result of
            `await client.webscript.get(name, version, response_type=Any)`.
        data
            the tensor data that will be provided as `instances` (V1) or `inputs` (V2)
        protocol
            the _dataplane_ protocol used (default `V1`)
        kwargs
            any request arguments passed on to the
            `rules.plugs_execution.execute_sensor_version` call, e.g.
            a `timeout` or `headers`.
        """
        if not isinstance(data, dict) or (
            "instances" not in data and "inputs" not in data
        ):
            key = "instances" if protocol == V1_PROTOCOL else "inputs"
            data = {key: data}
        plug = ref["entity"]["plug"]
        invoke_resp: dict = await self.rules.plugs_execution.execute_sensor_version(
            plug["name"],
            plug["version"],
            json={"properties": data},
            response_type=Any,
            **kwargs,
        )
        resp_data = invoke_resp.get("rawData", {})
        for key in ["predictions", "outputs"]:
            if key in resp_data:
                return resp_data[key]
        return resp_data

    async def publish(self, ref: dict):
        """Publish a deployed function."""
        entity = ref["entity"]
        as_webscript = entity.get("webscript", False)
        as_plug = entity.get("plug", False)
        if as_webscript:
            return await self.webscripts.publish(
                as_webscript["name"], as_webscript["version"], response_type=Any
            )
        if as_plug:
            return await self.plugs.publish(
                as_plug["name"], as_plug["version"], response_type=Any
            )

    @retry(reraise=True, stop=stop_after_delay(30), wait=wait_exponential(max=10))
    async def remove(self, ref: dict, force=True):
        """Remove a deployed function."""
        entity = ref["entity"]
        as_webscript = entity.get("webscript", False)
        as_plug = entity.get("plug", False)
        if as_webscript:
            return await self.webscripts.remove_version(
                as_webscript["name"],
                as_webscript["version"],
                query={"force": force},
                response_type=Any,
            )
        if as_plug:
            return await self.plugs.remove_version(
                as_plug["name"],
                as_plug["version"],
                query={"force": force},
                response_type=Any,
            )


def _as_model(ref, _type):
    return TypeAdapter(_type).validate_python(ref)
