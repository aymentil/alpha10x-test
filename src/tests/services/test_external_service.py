import pytest
from unittest.mock import patch, MagicMock
from src.services.external_service import ExternalService
from fastapi import HTTPException
from src.models.organization import OrganizationBase, OrganizationResponse


@pytest.mark.asyncio
async def test_external_service_get_organizations():
    """Test ExternalService.get_organizations method"""
    service = ExternalService()
    mock_response = {
        "data": [
            {
                "name": "Test Corp",
                "country": "USA",
                "employee_count": 100,
                "industry": "Technology",
                "founded": 2020
            }
        ],
        "total_records": 1
    }

    mock_result = OrganizationResponse(
        organizations=[OrganizationBase(**org)
                       for org in mock_response["data"]],
        average_employees=sum(org["employee_count"]
                              for org in mock_response["data"]) / len(mock_response["data"])
    )

    with patch('httpx.AsyncClient.get') as mock_get:
        # Configure the mock
        mock_get.return_value = MagicMock(
            status_code=200,
            json=lambda: mock_response,
            raise_for_status=lambda: None
        )

        # Call the service method
        result = await service.get_organizations(size=10, offset=0)

        # Verify the result
        assert result == mock_result


@pytest.mark.asyncio
async def test_external_service_error_handling():
    """Test error handling in ExternalService"""
    service = ExternalService()

    with patch('httpx.AsyncClient.get') as mock_get:
        # Configure mock to raise an error
        mock_get.side_effect = HTTPException(
            status_code=500, detail="Error communicating with external service"
        )

        # Verify that the service raises HTTPException
        with pytest.raises(HTTPException) as exc_info:
            await service.get_organizations(size=10, offset=0)

        assert exc_info.value.status_code == 500
        assert "Error communicating with external service" in str(
            exc_info.value.detail)


@pytest.mark.asyncio
async def test_external_service_get_organizations_with_filters():
    """Test ExternalService.get_organizations method with filters"""
    service = ExternalService()
    mock_response = {
        "data": [
            {
                "name": "Test Corp 2",
                "country": "France",
                "employee_count": 200,
                "industry": "Technology",
                "founded": 2020,
            }
        ],
        "total_records": 2
    }

    mock_result = OrganizationResponse(
        organizations=[OrganizationBase(**org)
                          for org in mock_response["data"] if org["employee_count"] >= 150 and org["country"] == "France"],
        average_employees=sum(org["employee_count"]
                                for org in mock_response["data"]) / len(mock_response["data"]) if len(mock_response["data"]) else 0
    )


    with patch('httpx.AsyncClient.get') as mock_get:
        # Configure the mock
        mock_get.return_value = MagicMock(
            status_code=200,
            json=lambda: {
                "data": [org for org in mock_response["data"] if org["employee_count"] >= 150 and org["country"] == "France"],
                "total_records": 1
            },
            raise_for_status=lambda: None
        )

        # Call the service method with filters
        result = await service.get_organizations(
            size=10, offset=0, min_employees=150, country="France")

        # Verify the result
        print(f'result: {result}')
        print(f'mock_result: {mock_result}')
        assert result == mock_result

@pytest.mark.asyncio
async def test_external_service_get_organizations_sort_by_employee_count():
    """Test ExternalService.get_organizations method with sorting by employee_count"""
    service = ExternalService()
    mock_response = {
        "data": [
            {
                "name": "Test Corp 1",
                "country": "USA",
                "employee_count": 100,
                "industry": "Technology",
                "founded": 2020
            },
            {
                "name": "Test Corp 2",
                "country": "France",
                "employee_count": 200,
                "industry": "Technology",
                "founded": 2020
            }
        ],
        "total_records": 2
    }

    mock_result = OrganizationResponse(
        organizations=[OrganizationBase(**org)
                       for org in sorted(mock_response["data"], key=lambda x: x["employee_count"])],
        average_employees=sum(org["employee_count"]
                              for org in mock_response["data"]) / len(mock_response["data"])
    )

    with patch('httpx.AsyncClient.get') as mock_get:
        # Configure the mock
        mock_get.return_value = MagicMock(
            status_code=200,
            json=lambda: mock_response,
            raise_for_status=lambda: None
        )

        # Call the service method with sorting by employee_count
        result = await service.get_organizations(
            size=10, offset=0, sort_by="employee_count")

        # Verify the result
        assert result == mock_result

@pytest.mark.asyncio
async def test_external_service_get_organizations_sort_by_founded():
    """Test ExternalService.get_organizations method with sorting by founded"""
    service = ExternalService()
    mock_response = {
        "data": [
            {
                "name": "Test Corp 1",
                "country": "USA",
                "employee_count": 100,
                "industry": "Technology",
                "founded": 2010
            },
            {
                "name": "Test Corp 2",
                "country": "France",
                "employee_count": 200,
                "industry": "Technology",
                "founded": 2020
            }
        ],
        "total_records": 2
    }

    mock_result = OrganizationResponse(
        organizations=[OrganizationBase(**org)
                       for org in sorted(mock_response["data"], key=lambda x: x["founded"])],
        average_employees=sum(org["employee_count"]
                              for org in mock_response["data"]) / len(mock_response["data"])
    )

    with patch('httpx.AsyncClient.get') as mock_get:
        # Configure the mock
        mock_get.return_value = MagicMock(
            status_code=200,
            json=lambda: mock_response,
            raise_for_status=lambda: None
        )

        # Call the service method with sorting by founded
        result = await service.get_organizations(
            size=10, offset=0, sort_by="founded")

        # Verify the result
        assert result == mock_result