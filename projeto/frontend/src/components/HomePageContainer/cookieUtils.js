export function getCookie(name) {
    const cookies = document.cookie.split(';');
    console.log('Cookies:', cookies);
    for (let cookie of cookies) {
        const [cookieName, cookieValue] = cookie.trim().split('=');
        if (cookieName === name) {
            console.log('Cookie Value:', cookieValue);
            return cookieValue;
        }
    }
    return null;
}