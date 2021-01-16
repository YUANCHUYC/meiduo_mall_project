# jwt拓展中自定义的响应参数构造函数
def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'user_id': user.id,
        'username': user.username,
        'token': token
    }
