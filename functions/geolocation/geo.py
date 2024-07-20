from routes.models.geoModel import LocationModel, PostGeoModel


# def format_polygon(geo_model: PostGeoModel) -> str:
#     coordinates = ', '.join(f"{loc.lat} {loc.long}" for loc in geo_model.border)
#     return f'POLYGON(({coordinates}))'

def format_polygon(geo_model: PostGeoModel) -> str:
    if len(geo_model.border) < 3:
        raise ValueError("A polygon must have at least 3 points")

    # Format coordinates as "lat long" (keeping the original order)
    coordinates = [f"{loc.lat} {loc.long}" for loc in geo_model.border]
    if coordinates[0] != coordinates[-1]:
        coordinates.append(coordinates[0])

    formatted_coords = ', '.join(coordinates)
    return f'POLYGON(({formatted_coords}))'
