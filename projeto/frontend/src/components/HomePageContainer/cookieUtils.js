export function getCookie(name) {
    const cookies = document.cookie.split(';');
    console.log('Cookies:', cookies); // Adicione esta linha para imprimir os cookies no console
    for (let cookie of cookies) {
        const [cookieName, cookieValue] = cookie.trim().split('=');
        if (cookieName === name) {
            console.log('Cookie Value:', cookieValue); // Adicione esta linha para imprimir o valor do cookie no console
            return cookieValue;
        }
    }
    return null; // Retorna null se o cookie não for encontrado
}