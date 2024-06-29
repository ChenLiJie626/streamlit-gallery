import json
from streamlit_elements import media, mui, sync, lazy
from .dashboard import Dashboard
import streamlit as st


class Player(Dashboard.Item):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._address, self._serverNames, self._serverGPU = "", "", ""
        self._clientNames, self._clientGPU = [], []
        st.session_state.setdefault("role", "server")
        st.session_state.setdefault("gpu", "4090")

    def _set_address(self, event):
        sync()
        self._address = event.target.value

    def _set_name(self, event):
        sync()
        role = getattr(st.session_state.role, "props", st.session_state.role).value
        gpu = getattr(st.session_state.gpu, "props", st.session_state.gpu).value

        if role == "server":
            self._serverNames, self._serverGPU = event.target.value, gpu
        else:
            self._clientNames.append(event.target.value)
            self._clientGPU.append(gpu)

    def get_content(self):
        id = 1
        if not self._serverNames:
            return json.dumps([{"id": id, "address": "server not found", "name": "server not found", "gpu": "server not found"}])
        result = [{"id": id, "address": self._address, "name": f"{self._serverNames}(server)", "gpu": self._serverGPU}]
        result += [{"id": i+2, "address": self._address, "name": name, "gpu": self._clientGPU[i]} for i, name in enumerate(self._clientNames)]
        return json.dumps(result)

    def __call__(self):
        with mui.Paper(key=self._key, sx={"display": "flex", "flexDirection": "column", "borderRadius": 3, "overflow": "hidden"}, elevation=1):
            with self.title_bar(padding="10px 15px", dark_switcher=False):
                mui.icon.OndemandVideo()
                mui.Typography("Role:")
            self._render_input("Server IP", lazy(self._set_address))
            self._render_input("Name", lazy(self._set_name))
            self._render_select("Role", sync(None, "role"), [("Server", "server"), ("Client", "client")])
            self._render_select("GPU", sync(None, "gpu"), [("NVIDIA GeForce RTX 4090", "4090"), ("NVIDIA GeForce RTX 3060", "3060"), ("NVIDIA TITAN RTX", "titan")])
            self._render_button("添加设备信息")

    def _render_input(self, label, on_change):
        with mui.Box(sx={"padding": "10px 15px", "display": "flex", "alignItems": "center"}):
            mui.Typography(label, sx={"marginRight": "10px", "width": "100px", "textAlign": "right"})
            mui.TextField(label="", variant="outlined", fullWidth=True, sx={"flexGrow": 1}, onChange=on_change)

    def _render_select(self, label, on_change, options):
        with mui.Box(sx={"padding": "10px 15px", "display": "flex", "alignItems": "center", "marginTop": "10px"}):
            mui.Typography(label, sx={"marginRight": "10px", "width": "100px", "textAlign": "right"})
            mui.Select(defaultValue=options[0][1], fullWidth=True, onChange=on_change, children=[mui.MenuItem(text, value=value) for text, value in options])

    def _render_button(self, text):
        with mui.Box(sx={"padding": "10px 15px", "marginTop": "10px", "display": "flex", "justifyContent": "center"}):
            mui.Button(text, variant="contained", color="primary", onClick=sync())
