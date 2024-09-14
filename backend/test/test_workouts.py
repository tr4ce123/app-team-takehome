import pytest
from unittest.mock import MagicMock
from datetime import datetime, timedelta
from pytz import timezone
from fastapi import HTTPException
from backend.services.workout import WorkoutService
from backend.models.workout import Workout
from backend.entities.workout import WorkoutEntity

tz = timezone("EST")

# Mock the session and the database model
@pytest.fixture
def mock_session():
    return MagicMock()

@pytest.fixture
def workout_service(mock_session):
    return WorkoutService(session=mock_session)

def test_all_workouts(workout_service, mock_session):
    mock_session.scalars().all.return_value = [
        WorkoutEntity(id=1, name='Morning Run', city="Chapel Hill", distance=3.5, duration=30, date="2024-09-13"),
        WorkoutEntity(id=2, name='Evening Walk', city="Raleigh", distance=2.0, duration=25, date="2024-09-12")
    ]
    result = workout_service.all()
    assert len(result) == 2
    assert result[0].name == 'Morning Run'
    assert result[1].name == 'Evening Walk'


def test_get_workout_by_id(workout_service, mock_session):
    mock_session.get.return_value = WorkoutEntity(
        id=1, name='Morning Run', city="Chapel Hill", distance=3.5, duration=30, date=datetime.now(tz).strftime("%Y-%m-%d")
    )
    result = workout_service.get_workout_by_id(1)
    assert result.id == 1
    assert result.name == 'Morning Run'

def test_get_workout_by_id_not_found(workout_service, mock_session):
    mock_session.get.return_value = None
    with pytest.raises(HTTPException) as err:
        workout_service.get_workout_by_id(999)
    assert err.value.status_code == 404

def test_create_workout(workout_service, mock_session):
    mock_workout = Workout(id=1, city="Chapel Hill", name='Morning Run', distance=3.5, duration=30, date=datetime.now(tz).strftime("%Y-%m-%d"))
    mock_session.query().filter().one_or_none.return_value = None
    result = workout_service.create_workout(mock_workout, weather=None)
    assert result.id == 1
    assert result.name == 'Morning Run'

def test_create_workout_already_exists(workout_service, mock_session):
    mock_workout = Workout(id=1, name='Morning Run', city="Chapel Hill", distance=3.5, duration=30, date=datetime.now(tz).strftime("%Y-%m-%d"))
    mock_session.query().filter().one_or_none.return_value = WorkoutEntity()
    with pytest.raises(HTTPException) as err:
        workout_service.create_workout(mock_workout, weather=None)
    assert err.value.status_code == 400

def test_get_weekly_workouts(workout_service, mock_session):
    mock_session.scalars().all.return_value = [
        WorkoutEntity(id=1, name='Morning Run', city="Chapel Hill", distance=3.5, duration=30, date=(datetime.now(tz) - timedelta(days=2)).strftime("%Y-%m-%d")),
        WorkoutEntity(id=2, name='Evening Walk', city="Raleigh", distance=2.0, duration=25, date=(datetime.now(tz) - timedelta(days=5)).strftime("%Y-%m-%d"))
    ]
    result = workout_service.get_weekly_workouts()
    assert len(result) == 2
    assert all((datetime.now(tz).date() - timedelta(days=7)) <= datetime.strptime(workout.date, "%Y-%m-%d").date() <= datetime.now(tz).date() for workout in result)

def test_get_total_weekly_aggregate_workout_data(workout_service, mock_session):
    mock_session.scalars().all.return_value = [
        WorkoutEntity(distance=3.5, duration=30),
        WorkoutEntity(distance=2.0, duration=25)
    ]
    total_distance = workout_service.get_total_weekly_aggreate_workout_data("distance")
    total_duration = workout_service.get_total_weekly_aggreate_workout_data("duration")
    assert total_distance == 5.5
    assert total_duration == 55

def test_get_total_weekly_aggregate_workout_data_invalid_data_point(workout_service, mock_session):
    with pytest.raises(HTTPException) as err:
        workout_service.get_total_weekly_aggreate_workout_data("invalid_point")
    assert err.value.status_code == 400

def test_get_average_weekly_aggregate_workout_data(workout_service, mock_session):
    mock_session.scalars().all.return_value = [
        WorkoutEntity(distance=3.5, duration=30),
        WorkoutEntity(distance=2.0, duration=25)
    ]
    average_distance = workout_service.get_average_weekly_aggreate_workout_data("distance")
    average_duration = workout_service.get_average_weekly_aggreate_workout_data("duration")
    assert average_distance == 2.75
    assert average_duration == 27.5

def test_get_average_weekly_aggregate_workout_data_invalid_data_point(workout_service, mock_session):
    with pytest.raises(HTTPException) as err:
        workout_service.get_average_weekly_aggreate_workout_data("invalid_point")
    assert err.value.status_code == 400

def test_get_personal_best_distance(workout_service, mock_session):
    mock_session.scalars().first.return_value = WorkoutEntity(distance=5.0)
    result = workout_service.get_personal_best_distance()
    assert result == "Personal best distance: 5.0 miles!"

def test_get_personal_best_duration_per_mile(workout_service, mock_session):
    mock_session.scalars().all.return_value = [
        WorkoutEntity(distance=3.5, duration=30),
        WorkoutEntity(distance=2.0, duration=15)
    ]
    result = workout_service.get_personal_best_duration_per_mile()
    assert result == "Your personal best time per mile is 7.5 minutes per mile!"

def test_update_workout(workout_service, mock_session):
    mock_session.get.return_value = WorkoutEntity(id=1, name='Morning Run', city="Chapel Hill", distance=3.5, duration=30, date="2024-09-13")
    updated_workout = Workout(id=1, name='Morning Run Updated', city="Chapel Hill", distance=4.0, duration=35, date="2024-09-14")
    result = workout_service.update_workout(updated_workout)
    assert result.name == 'Morning Run Updated'
    assert result.distance == 4.0
    assert result.duration == 35

def test_update_workout_not_found(workout_service, mock_session):
    mock_session.get.return_value = None
    updated_workout = Workout(id=999, name='Nonexistent Run', city="Nowhere", distance=0, duration=0, date="2024-09-14")
    with pytest.raises(HTTPException) as err:
        workout_service.update_workout(updated_workout)
    assert err.value.status_code == 404

def test_delete_workout(workout_service, mock_session):
    mock_session.get.return_value = WorkoutEntity(id=1, name='Morning Run')
    workout_service.delete_workout(1)
    mock_session.delete.assert_called_once()

def test_delete_workout_not_found(workout_service, mock_session):
    mock_session.get.return_value = None
    with pytest.raises(HTTPException) as err:
        workout_service.delete_workout(999)
    assert err.value.status_code == 404
