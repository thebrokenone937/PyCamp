from project.models.core.users import UsersService

def validateResetForm(id, hash):    
    error = False
    
    if not hash:
        error = 'No hash passed to page'
    elif not id:
        error = 'No id specified'
    else:
        usersService = UsersService()
        
        userResult = usersService.first(id=int(id))    
        
        if not userResult:
            error = 'No user with that id'
        else:
            if userResult.forgot_password_hash != hash:
                error = 'Hash is not valid'
            else:
                error = False
    return error
                