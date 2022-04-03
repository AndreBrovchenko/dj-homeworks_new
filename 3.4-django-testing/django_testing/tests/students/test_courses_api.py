import pytest
from rest_framework.test import APIClient
from model_bakery import baker
from students.models import Course, Student


DATA_COURSE = {
        "name": "first course"
    }


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)

    return factory


@pytest.fixture
def student_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)

    return factory


@pytest.mark.django_db
def test_get_first_course(client, course_factory):
    # Arrange
    courses = course_factory(_quantity=1)
    course_id = courses[0].id
    # Act
    response = client.get(f'/api/v1/courses/{course_id}/')
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data['name'] == courses[0].name


@pytest.mark.django_db
def test_get_list_course(client, course_factory):
    # Arrange
    courses = course_factory(_quantity=10)
    # Act
    response = client.get('/api/v1/courses/')
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert len(data) == len(courses)
    for i, item in enumerate(data):
        assert item['name'] == courses[i].name


@pytest.mark.django_db
def test_filter_list_id_course(client, course_factory):
    # Arrange
    courses = course_factory(_quantity=10)
    filter_id = 2
    course_id = courses[filter_id].id
    # Act
    response = client.get(f'/api/v1/courses/{course_id}/')
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data['id'] == course_id


@pytest.mark.django_db
def test_filter_list_name_course(client, course_factory):
    # Arrange
    courses = course_factory(_quantity=10)
    filter_id = 2
    course_name = courses[filter_id].name
    # Act
    response = client.get(f'/api/v1/courses/?search={course_name}')
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data[0]['name'] == course_name


@pytest.mark.django_db
def test_create_course(client, course_factory):
    # Arrange
    courses = client.post('/api/v1/courses/', DATA_COURSE)
    course_id = courses.data['id']
    # Act
    response = client.get(f'/api/v1/courses/{course_id}/')
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data['name'] == courses.data['name']


@pytest.mark.django_db
def test_update_course(client, course_factory):
    # Arrange
    courses = course_factory(_quantity=1)
    course_id = courses[0].id
    courses = client.patch(f'/api/v1/courses/{course_id}/', DATA_COURSE)
    # Act
    response = client.get(f'/api/v1/courses/{course_id}/')
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data['name'] == courses.data['name']


@pytest.mark.django_db
def test_delete_course(client, course_factory):
    # Arrange
    courses = client.post('/api/v1/courses/', DATA_COURSE)
    course_id = courses.data['id']
    # Act
    response = client.delete(f'/api/v1/courses/{course_id}/')
    # Assert
    assert courses.status_code == 201
    assert response.status_code == 204
