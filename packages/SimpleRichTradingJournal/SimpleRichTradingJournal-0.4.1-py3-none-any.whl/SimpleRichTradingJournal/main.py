try:
    import sys
    from pathlib import Path
    sys.path.append(str(Path(__file__).parent))
except Exception:
    raise

from dash import Dash

import __env__
import layout

__project_name__ = "Simple Rich Trading Journal"


def run():
    app = Dash(
        __project_name__,
        title=__env__.PROFILE or __project_name__,
        update_title="working...",
        assets_folder=__env__.DASH_ASSETS,
        assets_url_path=__env__._folder_profile_assets,
    )
    app.layout = layout.LAYOUT
    app._favicon = ".favicon.ico"
    try:
        import callbacks
    except Exception:
        raise

    app.run(debug=False, host=__env__.appHost, port=__env__.appPort)


if __name__ == "__main__":
    run()
