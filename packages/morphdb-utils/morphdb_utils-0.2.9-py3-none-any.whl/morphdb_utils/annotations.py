import base64
import io
from typing import Any, Callable, Dict, Literal, Optional

import matplotlib.figure  # type: ignore
import pandas as pd  # type: ignore
import plotly  # type: ignore
import plotly.io as pio  # type: ignore

# enum type: export format
VISUALIZATION_FORMAT = Literal["png", "html"]


def _get_html_from_mpl_image(
    fig: matplotlib.figure.Figure, format: VISUALIZATION_FORMAT = "html"
) -> str:
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    if format == "png":
        # return in base64 encoded png format
        return base64.b64encode(buf.read()).decode()
    elif format == "html":
        return f'<img src="data:image/png;base64,{base64.b64encode(buf.read()).decode()}" />'


def _get_html_from_plotly_image(fig, format: VISUALIZATION_FORMAT = "html") -> str:
    if format == "png":
        pio.kaleido.scope.chromium_args += ("--single-process",)
        buf = io.BytesIO()
        fig.write_image(buf, format="png")
        buf.seek(0)
        return base64.b64encode(buf.read()).decode()
    elif format == "html":
        buf = io.StringIO()
        fig.write_html(
            buf,
            include_plotlyjs="cdn",
            full_html=False,
            config={
                "modeBarButtonsToRemove": [
                    "zoom",
                    "pan",
                    "select",
                    "zoomIn",
                    "zoomOut",
                    "autoScale",
                    "resetScale",
                    "lasso2d",
                ],
                "displaylogo": False,
            },
        )
        buf.seek(0)
        return buf.getvalue()


def transform(output: Optional[str] = None):
    """Decorator for main functions of Morph's Python Cell.
    This decorator indicates that the function performs some tabular transformation
    and returns a pandas DataFrame.
    """

    def decorator(func: Callable):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            assert isinstance(result, pd.DataFrame)
            extras: Dict[str, Any] = {"output": output}
            return result, extras

        return wrapper

    return decorator


def visualize(library: Literal["matplotlib", "plotly"], output: Optional[str] = None):
    """decorator for main functions of morph's Python Cell.
    This decorator indicates that the function perform some visualization and returns Figure object.
    the Figure object will be converted to HTML string and returned.

    Args:
        library (Literal["matplotlib", "plotly"]): library used for visualization. either "matplotlib" or "plotly"
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            extras: Dict[str, Any] = {"output": output}

            # post process
            # format = os.getenv("MORPH_VISUALIZATION_FORMAT", "html")
            if library == "matplotlib":
                assert isinstance(result, matplotlib.figure.Figure)
                return [
                    _get_html_from_mpl_image(result, "html"),
                    _get_html_from_mpl_image(result, "png"),
                ], extras
            elif library == "plotly":
                assert isinstance(result, plotly.graph_objs._figure.Figure)
                return [
                    _get_html_from_plotly_image(result, "html"),
                    _get_html_from_plotly_image(result, "png"),
                ], extras
            else:
                raise ValueError("library should be either 'matplotlib' or 'plotly'")

        return wrapper

    return decorator


def report(output: Optional[str] = None):
    """decorator for main functions of morph's Python Cell.
    This decorator indicates that the function perform some reporting and returns markdown string.
    """

    def decorator(func: Callable):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            assert isinstance(result, str)
            extras: Dict[str, Any] = {"output": output}
            return result, extras

        return wrapper

    return decorator


def api(output: Optional[str] = None):
    """decorator for main functions of morph's Python Cell.
    This decorator indicates that the function perform some API call and returns JSON string.
    """

    def decorator(func: Callable):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            assert isinstance(result, dict)
            extras: Dict[str, Any] = {"output": output}
            return result, extras

        return wrapper

    return decorator
