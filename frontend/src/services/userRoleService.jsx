const API_BASE_URL = 'http://127.0.0.1:8000/api';

export async function getUserRoles() {
    const accessToken = localStorage.getItem('access_token');

    if (!accessToken) {
        throw new Error('You are not logged in.');
    }

    const response = await fetch(
        `${API_BASE_URL}/user-roles/`,
        {
            method: 'GET',
            headers: {
                Authorization: `Bearer ${accessToken}`,
                'Content-Type': 'application/json',
            },
        }
    );

    const data = await response.json();

    if (!response.ok) {
        throw new Error(
            data.detail || 'Failed to load user roles'
        );
    }

    return data;
}