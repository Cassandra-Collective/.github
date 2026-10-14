"""Minimal stdio MCP client for VectorCraft's headless engine.

VectorCraft ships `vectorcraft-cli mcp --headless`, a Model Context Protocol server that
speaks newline-delimited JSON-RPC 2.0 on stdin/stdout. This module starts one engine
session and exposes two calls:

    VC.tool(name, **args)        an MCP tool (draw_path, export, pathfinder, ...)
    VC.cmd(command, **params)    any engine command by id (file.new, text.setStyle, ...)

Contract
--------
* Inputs: the engine's executable path (VECTORCRAFT_CLI env var or the default install
  path) and one folder that confines every file the engine may read or write.
* Outputs: the parsed JSON result of each call.
* Side effects: one child process for the life of the VC object; files written only
  inside the confined folder.
* Errors: a JSON-RPC error or a tool result flagged isError raises RuntimeError with the
  call that failed, so a broken build stops instead of producing partial assets.
"""
import json
import os
import subprocess

DEFAULT_EXE = r"C:\Program Files\VectorCraft\vectorcraft-cli.exe"


class VC:
    def __init__(self, root, exe=None):
        exe = exe or os.environ.get("VECTORCRAFT_CLI", DEFAULT_EXE)
        self.p = subprocess.Popen(
            [exe, "mcp", "--headless", "--automation-read-root", root, "--automation-write-root", root],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            text=True, encoding="utf-8")
        self.i = 0
        self.server = self._rpc("initialize", {
            "protocolVersion": "2024-11-05", "capabilities": {},
            "clientInfo": {"name": "cassandra-brand", "version": "1"}})
        self._send({"jsonrpc": "2.0", "method": "notifications/initialized"})

    def _send(self, msg):
        self.p.stdin.write(json.dumps(msg) + "\n")
        self.p.stdin.flush()

    def _rpc(self, method, params):
        self.i += 1
        self._send({"jsonrpc": "2.0", "id": self.i, "method": method, "params": params})
        while True:
            line = self.p.stdout.readline()
            if not line:
                raise RuntimeError("VectorCraft engine exited: " + self.p.stderr.read())
            msg = json.loads(line)
            if msg.get("id") == self.i:
                break
        if "error" in msg:
            raise RuntimeError(f"{method} {params}: {msg['error']}")
        return msg["result"]

    def tool(self, name, **args):
        res = self._rpc("tools/call", {"name": name, "arguments": args})
        texts = [c["text"] for c in res.get("content", []) if c.get("type") == "text"]
        if res.get("isError"):
            raise RuntimeError(f"{name} {args}: {texts}")
        out = texts[0] if texts else None
        try:
            return json.loads(out) if out else None
        except json.JSONDecodeError:
            return out

    def cmd(self, command, **params):
        return self.tool("run_command", command=command, params=params)

    def close(self):
        try:
            self.p.stdin.close()
            self.p.wait(timeout=20)
        except Exception:
            self.p.kill()

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()
