# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from geopandas import GeoDataFrame
from shapely.geometry import Polygon

from spikeless.utils import functs, geo_process

from flask import Flask

geo_app = Flask(__name__)
# geo_app.run(debug=True)

# def print_hi(name):
#     # Use a breakpoint in the code line below to debug your script.
#     print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


def main(filename: str, angle: float, distance: float, output: str):
    """
    A command-line tool used to remove spikes from polygons stored in
    Geopackage format.
    """
    data = functs.load_geopackage(filename)

    if not functs.validate_crs(data):
        # raise click.UsageError(
        raise (
            """The input file doesn't have a valid CRS or it does not have a
            geographic CRS."""
        )

    geod = utils.extract_crs_geod(data)
    processor = geo_process.GeometryProcessor(angle, distance)
    results = []

    for entry in data.itertuples():
        geometry = entry.geometry

        exterior = processor.process_sequence(geod, geometry.exterior.coords)

        interiors = []
        for interior_ring in geometry.interiors:
            processed_interior_ring = processor.process_sequence(
                geod,
                interior_ring.coords,
            )

            interiors.append(processed_interior_ring)

        results.append((entry.name, Polygon(exterior, interiors)))

    cleaned_data = GeoDataFrame(
        results,
        columns=["name", "geometry"],
        crs=data.crs
    )
    functs.save_geopackage(output, cleaned_data)

@geo_app.route("/", methods=['GET'])
def index():
    return "GIS Application!!! - Removing spikes from a polygon..."


# Entrypoint
@geo_app.route("/start", methods=["GET"])
def start():
    return "Spike Removal..."

@geo_app.errorhandler(404)
def page_not_found(e):
    return "Error 404"


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    geo_app.run(debug=True)
    # return 'PyCharm'

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
