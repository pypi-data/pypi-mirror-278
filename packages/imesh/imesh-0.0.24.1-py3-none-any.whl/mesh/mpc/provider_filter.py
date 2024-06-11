#
# Copyright (c) 2000, 2099, trustbe and/or its affiliates. All rights reserved.
# TRUSTBE PROPRIETARY/CONFIDENTIAL. Use is subject to license terms.
#
#

from typing import Any, Dict

import mesh.log as log
import mesh.telemetry as telemetry
import mesh.tool as tool
from mesh.cause import MeshCode, Codeable, MeshException
from mesh.context import Mesh
from mesh.macro import spi
from mesh.mpc.digest import Digest
from mesh.mpc.filter import Filter, Invoker, Invocation, PROVIDER
from mesh.prsim import Metadata
from mesh.prsim.context import RunMode


@spi(name="provider", pattern=PROVIDER, priority=0x7fffff00)
class ProviderFilter(Filter):

    def invoke(self, invoker: Invoker, invocation: Invocation) -> Any:
        attachments: Dict[str, str] = invocation.get_parameters().get_attachments()
        if not attachments:
            attachments = {}
        Mesh.context().decode(attachments)

        digest = Digest()
        try:
            ret = invoker.run(invocation)
            digest.write("P", MeshCode.SUCCESS.get_code())
            return ret
        except BaseException as e:
            if isinstance(e, Codeable):
                digest.write("P", e.get_code())
            else:
                digest.write("P", MeshCode.SYSTEM_ERROR.get_code())
            if isinstance(e, MeshException):
                log.error(f"{digest.trace_id},{Mesh.context().get_urn()},{e.get_message}")
            raise e


@spi(name="telemetryProvider", pattern=PROVIDER, priority=0x7ffffff0)
class TelemetryProviderFilter(Filter):
    """
    recover telemetry context via mesh context for tracing
    """

    def invoke(self, invoker: Invoker, invocation: Invocation) -> Any:
        if not RunMode.TRACE.match(Mesh.context().get_run_mode()):
            return invoker.run(invocation)

        attachments: Dict[str, str] = invocation.get_parameters().get_attachments()
        if not telemetry.if_rebuild_span():
            return invoker.run(invocation)
        trace_id = attachments.get(Metadata.MESH_TRACE_ID.key(), tool.new_trace_id())
        with telemetry.build_via_remote(attachments, invocation.get_urn().string()):
            current_span = telemetry.get_current_span()
            current_span.set_attribute('mesh-trace-id', trace_id)
            return invoker.run(invocation)
