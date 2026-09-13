import os
import json
import pytest
import requests
import responses
from dotenv import load_dotenv, find_dotenv

# Loads the hidden API key
load_dotenv(find_dotenv())
API_KEY = os.getenv("TCGGO_API_KEY")

SEARCH_ENDPOINT = "https://riftbound-prices-api.p.rapidapi.com/cards/search"

HEADERS = {
	"x-rapidapi-key": API_KEY,
	"x-rapidapi-host": "riftbound-prices-api.p.rapidapi.com",
}

def load_mock_data():
    # Reads mock_data.json
    with open("tests/mock_data.json", "r") as file:
        return json.load(file)

@responses.activate
def test_mocked_card_search_success():
    mock_payload = load_mock_data()

    # Intercepts calls to live API
    responses.add(responses.GET, SEARCH_ENDPOINT, json=mock_payload, status=200)

    # Send the request
    response = requests.get(SEARCH_ENDPOINT, headers=HEADERS)
    data = response.json()

    # Assertions
    assert response.status_code == 200
    assert isinstance(data, dict)

@responses.activate
def test_mocked_rate_limit_handling():
    responses.add(responses.GET, SEARCH_ENDPOINT, json={"message": "You have exceeded your rate limit"}, status=429)

    response = requests.get(SEARCH_ENDPOINT, headers=HEADERS)

    assert response.status_code == 429
    assert "exceeded" in response.json()["message"]

# Live Test ( Costs 1 Request )
@pytest.mark.live
def test_live_api_authentication():
    if not API_KEY:
        pytest.fail("TCGGO_API_KEY is not set in the .env file")

    response = requests.get(SEARCH_ENDPOINT, headers=HEADERS)
    assert response.status_code == 200



    