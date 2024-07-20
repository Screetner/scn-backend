import json

import bcrypt
from faker import Faker
from geoalchemy2 import WKTElement

fake = Faker()


def generate_valid_polygon():
    # Generate 4 random points
    points = [(fake.latitude(), fake.longitude()) for _ in range(4)]
    # Close the polygon by adding the first point at the end
    points.append(points[0])
    # Create the POLYGON string
    polygon_str = ', '.join(f'{lat} {lon}' for lat, lon in points)
    return f'POLYGON(({polygon_str}))'


def generate_mock_organization():
    return {
        'Name': fake.company(),
        # 'Border': WKTElement(generate_valid_polygon(), srid=4326),  # Ensure SRID is specified
    }


def generate_mock_role(org_id: int):
    ability_scope = {
        "create": True,
        "read": True,
        "update": True,
        "delete": True
    }
    return {
        'roleName': 'Owner',
        'OrganizationId': org_id,
        'abilityScope': json.dumps(ability_scope),
    }


def generate_mock_user(role_id: int):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw('admin'.encode('utf-8'), salt)
    return {
        'username': 'admin',
        'email': 'admin@admin.com',
        'password': hashed,
        'roleId': role_id
    }


def generate_mock_asserType():
    return {
        'assetType': 'billboard'
    }
