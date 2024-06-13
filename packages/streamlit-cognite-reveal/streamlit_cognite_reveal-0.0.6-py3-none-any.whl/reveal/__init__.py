import os
import warnings
import dataclasses
import streamlit.components.v1 as components
from .RevealConfig import RevealConfig

# Create a _RELEASE constant. We'll set this to False while we're developing
# the component, and True when we're ready to package and distribute it.
# (This is, of course, optional - there are innumerable ways to manage your
# release process.)
_RELEASE = bool(os.getenv('RELEASE', False))
_RELEASE=True
# Declare a Streamlit component. `declare_component` returns a function
# that is used to create instances of the component. We're naming this
# function "_component_func", with an underscore prefix, because we don't want
# to expose it directly to users. Instead, we will create a custom wrapper
# function, below, that will serve as our component's public API.

# It's worth noting that this call to `declare_component` is the
# *only thing* you need to do to create the binding between Streamlit and
# your component frontend. Everything else we do in this file is simply a
# best practice.

if not _RELEASE:
    warnings.warn("WARNING: Running in development mode.")
    reveal_func = components.declare_component(
        # We give the component a simple, descriptive name ("my_component"
        # does not fit this bill, so please choose something better for your
        # own component :)
        "reveal",
        # Pass `url` here to tell Streamlit that the component will be served
        # by the local dev server that you run via `npm run start`.
        # (This is useful while your component is in development.)
        url="https://localhost:3001/",
    )
else:
    # When we're distributing a production version of the component, we'll
    # replace the `url` param with `path`, and point it to the component's
    # build directory:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend", "build")
    reveal_func = components.declare_component("reveal", path=build_dir)

def reveal(client, scene_external_id: str, scene_space: str, config: RevealConfig = None, key=None):
    """Create a new instance of Reveal.

    Parameters
    ----------
    client: CogniteClient
        The CogniteClient to use
    scene_external_id: string
        External id of the 3D scene
    scene_space: string
        Space id of the 3D scene
    config: RevealConfig
        Instance of a RevealConfig dataclass
    key: str or None
        An optional key that uniquely identifies this component. If this is
        None, and the component's arguments are changed, the component will
        be re-mounted in the Streamlit frontend and lose its current state.

    Returns
    -------
    int
        The number of times the component's "Click Me" button has been clicked.
        (This is the value passed to `Streamlit.setComponentValue` on the
        frontend.)

    """
    # Call through to our private component function. Arguments we pass here
    # will be sent to the frontend, where they'll be available in an "args"
    # dictionary.
    #
    # "default" is a special argument that specifies the initial return
    # value of the component before the user has interacted with it.
    client_config = {
        # TODO replace this with a callback that refeshes token
        # Also; can we get rid of the Bearer evilness?
        "token": client.config.credentials.authorization_header()[1].replace("Bearer ", ""),
        "project": client.config.project,
        "baseUrl": client.config.base_url
    }
    clipping_plane_arguments = []
    for clipping_plane in config.clipping_planes:
        # We only send a list of four numbers, normal + distance
        clipping_plane_arguments.append([*clipping_plane.normal, clipping_plane.distance])
    component_value = reveal_func(
        client_config=client_config, 
        scene_external_id=scene_external_id, 
        selected_asset_ids=config.selected_asset_ids,
        clipping_planes=clipping_plane_arguments,
        scene_space=scene_space, 
        height=config.height,
        default_node_appearance=config.default_node_appearance.value,
        styled_node_collections=[dataclasses.asdict(styled_node_collection) for styled_node_collection in config.styled_node_collections],
        key=key, 
        default={}
    )

    # We could modify the value returned from the component if we wanted.
    # There's no need to do this in our simple example - but it's an option.
    return component_value
