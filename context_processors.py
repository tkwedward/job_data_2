def userdata(request):
    user = request.user
    userdata ={
        'username': None,
        'user_id': None
    }
    try:
        userdata={
            'username': user.username,
            'user_id':user.social_auth.get(provider='facebook').uid
        }
    except Exception as AttributeError:
        pass
    return userdata
