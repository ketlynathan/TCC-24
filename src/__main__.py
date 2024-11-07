from rich import print as rprint

from src.lib.http import create_authenticated_client

http_client = create_authenticated_client()


get_activities_response = http_client.get("/api/v3/athlete/activities")
rprint(get_activities_response.json())
