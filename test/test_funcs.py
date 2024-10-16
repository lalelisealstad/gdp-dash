
import pytest
import pandas as pd
from unittest.mock import patch

from src.func import get_country_gdp, get_dict_countries, make_gdp_fig, get_last_gdp

from wbdata import get_countries

def test_get_dict_countries_api_call():
    result = get_dict_countries()

    assert isinstance(result, dict)

    # Check if the dictionary contains specific known countries
    assert 'US' in result  # United States
    assert 'GB' in result  # United Kingdom
    assert 'FR' in result  # France
    assert 'A9' not in result  # non countries should not be in result
    assert result['US'] == 'United States'
    
    
    

def test_get_country_gdp_api_call():
    country_code = 'US'
    
    result = get_country_gdp(country_code)
    
    assert isinstance(result, pd.DataFrame)
    assert not result.empty
    assert not result.isna().any().any()
    assert 'GDP' in result.columns



# Sample data for testing
data = pd.DataFrame({
    'date': [2020, 2019, 2018],
    'GDP': [2_000_000_000_000, 1_800_000_000_000, 1_700_000_000_000]
})

def test_get_last_gdp():
    # Call the function
    last_date, gdp_in_billions = get_last_gdp('Sample Country', data)
    
    # Test that the year is between 1950 and 2025
    assert 1950 <= last_date <= 2025, f"Year {last_date} is not between 1950 and 2025"
    
    # Test that the GDP is greater than 0
    assert gdp_in_billions > 0, f"GDP in billions {gdp_in_billions} should be greater than 0"