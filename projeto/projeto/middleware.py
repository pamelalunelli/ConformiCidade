class LogAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Verifica se o usuário está autenticado
        if request.user.is_authenticated:
            print(f'Usuário autenticado: {request.user}')
        else:
            print('Usuário não autenticado')
        
        # Continua o fluxo normal da requisição
        response = self.get_response(request)
        return response