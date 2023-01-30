
import streamlit.components.v1 as components
from typing import Optional

# Create a function _component_func which will call the frontend component when run
_component_func = components.declare_component(
    "button_card",
    url="http://localhost:3001",  # Fetch frontend component from local webserver
)


def st_button_card(
    body: str, 
    title: str, 
    image: Optional[str] = None,
    ) -> bool:
    component_value = _component_func(body=body, title=title, image=image)
    return component_value

