import json
from streamlit_elements import media, mui, sync, lazy
from .dashboard import Dashboard
import streamlit as st


class Player(Dashboard.Item):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._address = ""
        self._serverNames = ""
        self._clientNames = []
        self._serverGPU = ""
        self._clientGPU = []

        if "role" not in st.session_state:
            st.session_state["role"] = "server"

        if "gpu" not in st.session_state:
            st.session_state["gpu"] = "4090"

    def _set_address(self, event):
        sync()
        self._address = event.target.value

    def _set_name(self, event):
        sync()
        if hasattr(st.session_state.role, "props"):
            role = st.session_state.role.props.value
        else:
            role = st.session_state.role
        if hasattr(st.session_state.gpu, "props"):
            gpu = st.session_state.gpu.props.value
        else:
            gpu = st.session_state.gpu

        if role == "server":
            self._serverNames = event.target.value
            self._serverGPU = gpu
        else:
            self._clientNames.append(event.target.value)
            self._clientGPU.append(gpu)

    def get_content(self):
        id = 1
        if self._serverNames == "":
            return json.dumps(
                [
                    {
                        "id": id,
                        "address": "server not found",
                        "name": "server not found",
                        "gpu": "server not found",
                    }
                ]
            )
        result = [
            {
                "id": id,
                "address": self._address,
                "name": self._serverNames+"(server)",
                "gpu": self._serverGPU,
            }
        ]
        for name in self._clientNames:
            id += 1
            result.append(
                {
                    "id": id,
                    "address": self._address,
                    "name": name,
                    "gpu": self._clientGPU[self._clientNames.index(name)],
                }
            )
        return json.dumps(result)

    def __call__(self):
        with mui.Paper(
            key=self._key,
            sx={
                "display": "flexƒ",
                "flexDirection": "column",
                "borderRadius": 3,
                "overflow": "hidden",
            },
            elevation=1,
        ):
            with self.title_bar(padding="10px 15px 10px 15px", dark_switcher=False):
                mui.icon.OndemandVideo()
                mui.Typography("Role:")

            with mui.Box(
                sx={
                    "padding": "10px 15px 10px 15px",
                    "display": "flex",
                    "alignItems": "center",
                }
            ):
                mui.Typography(
                    "Server IP",
                    sx={"marginRight": "10px", "width": "100px", "textAlign": "right"},
                )
                mui.TextField(
                    label="",
                    variant="outlined",
                    fullWidth=True,
                    sx={"flexGrow": 1},
                    onChange=lazy(self._set_address),
                )

            with mui.Box(
                sx={
                    "padding": "10px 15px 10px 15px",
                    "display": "flex",
                    "alignItems": "center",
                    "marginTop": "10px",
                }
            ):
                mui.Typography(
                    "Name",
                    sx={"marginRight": "10px", "width": "100px", "textAlign": "right"},
                )
                mui.TextField(
                    label="",
                    variant="outlined",
                    fullWidth=True,
                    sx={"flexGrow": 1},
                    onChange=lazy(self._set_name),
                )

            # Adding Dropdown (Select) Field
            with mui.Box(
                sx={
                    "padding": "10px 15px 10px 15px",
                    "display": "flex",
                    "alignItems": "center",
                    "marginTop": "10px",
                }
            ):
                mui.Typography(
                    "Role",
                    sx={"marginRight": "10px", "width": "100px", "textAlign": "right"},
                )
                mui.Select(
                    defaultValue="server",
                    fullWidth=True,
                    children=[
                        mui.MenuItem("Server", value="server"),
                        mui.MenuItem("Client", value="client"),
                    ],
                    onChange=sync(None, "role"),
                )

            # Adding Dropdown (Select) Field
            with mui.Box(
                sx={
                    "padding": "10px 15px 10px 15px",
                    "display": "flex",
                    "alignItems": "center",
                    "marginTop": "10px",
                }
            ):
                mui.Typography(
                    "GPU",
                    sx={"marginRight": "10px", "width": "100px", "textAlign": "right"},
                )
                mui.Select(
                    defaultValue="4090",
                    fullWidth=True,
                    children=[
                        mui.MenuItem("NVIDIA GeForce RTX 4090", value="4090"),
                        mui.MenuItem("NVIDIA GeForce RTX 3060", value="3060"),
                        mui.MenuItem("NVIDIA TITAN RTX", value="titan"),
                    ],
                    onChange=sync(None, "gpu"),
                )

            # Adding a Button
            with mui.Box(
                sx={
                    "padding": "10px 15px 10px 15px",
                    "marginTop": "10px",
                    "display": "flex",
                    "justifyContent": "center",
                }
            ):
                mui.Button(
                    "添加设备信息", variant="contained", color="primary", onClick=sync()
                )
