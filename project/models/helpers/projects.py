from project.models.core.priority_levels import PriorityLevelsService
from project.models.core.projects import ProjectsService
from project.models.core.project_users import ProjectUsersService
from project.models.core.lists import ListsService
from project.models.core.todos import TodosService
from project.models.core.comments import CommentsService
from project.models.core.users import UsersService
from project.models.core.files import FilesService
from project.models.core.todo_assigned_users import TodoAssignedUsersService
from project.lib.template import render_custom_template, isTokenValid
import flask
from flask.ext.login import current_user
import datetime
from project.models.uploads import *
from project.lib.template import *

def has_access(projectId):
    """This function checks if the current logged in user has access
    to the project.
    
    Params:
    
    projectId: Integer
    
    Result: Boolean"""
    
    projectUsersService = ProjectUsersService()
    projectUsers = projectUsersService.get_project_users(projectId)
                
    hasAccess = False

    for proj, user in projectUsers:
        if current_user.id == user.id:
            hasAccess = True
            break

    return hasAccess

def has_access_to_list(listId):
    
    """This function checks if the current logged in user has access
    to a project list.
    
    Params:
    
    listId: Integer
    
    Result: Tuple(Boolean, String)"""
    
    blockAccess = True
    error = False
    
    if listId:
        listsService = ListsService()
        listResult = listsService.first(id=listId)
        
        if listResult:
            projectUsersService = ProjectUsersService()
            projectUser = projectUsersService.first(project_id=listResult.project_id, user_id=current_user.id)
            
            if not projectUser:
                error = 'You do not have access to this project'
                blockAccess = True
            else:
                blockAccess = False
        else:
            error = 'Could not retrieve list'
            blockAccess = True
    else:
        blockAccess = True
        error = 'No list id provided'
        
    return (blockAccess, error)    

def toggle_todo_item_status(todoId, status, token):

    """This function toggles a todo item's status completed and incompleted.
    
    Params:
    
    todoId: Integer
    status: String
    token: String
    
    Result: Tuple(Boolean, String)"""
    
    result = False
    error = False
        
    if not todoId:
        error = 'No id specified'
    elif not status:
        error = 'No status specified'
    #elif not isTokenValid(token):
    #    error = 'The request did not come from Pycamp'
        
    if not error:
        todosService = TodosService()
        item = todosService.first(id=todoId)
        
        if not item:
            error = 'The to-do item does not exist'
        else:
            listsService = ListsService()
            listResult = listsService.first(id=item.list_id)
            
            if not listResult:
                error = 'No list associated with item'
            else:
                projectsService = ProjectsService()
                project = projectsService.first(id=listResult.project_id)
                
                if not project:
                    error = 'No project associated with item'
                else:
                    projectId = project.id
                    
                    projectUsersService = ProjectUsersService()
                    projectUser = projectUsersService.first(project_id=projectId, user_id=current_user.id)
                
                    if not projectUser:
                        error = 'You do not have access to this project'
                    else:
                        now = datetime.datetime.now()
                        
                        if status == 'complete':
                            todoStatus = 'Closed'
                            created = now.strftime("%Y-%m-%d %H:%M:%S")
                        elif status == 'incomplete':
                            todoStatus = 'Open'
                            created = now.strftime("%Y-%m-%d %H:%M:%S")
                        else:
                            error = 'Invalid Status'
        
        if not error:
            result = True
            todosService.update(item, status=todoStatus, completion_date=created)
            
    if error:
        result = False
        
    return (result, error)

def add_comment_item(todoId, listId, projectId, comment, file, token):
    
    """This function adds a comment to a todo item and attaches a file if provided.
    
    Params:
    
    todoId: Integer
    listId: Integer
    projectId: Integer
    comment: String
    file: File
    token: String
    
    Result: Tuple(Boolean, String)"""
    result = False
    error = False 
        
    if comment:
        if not isTokenValid(token):
            error = 'The request did not come from Pycamp'
            success = False
        elif not has_access(projectId):
            error = 'You do not have permission to add comments to this project'
            success = False
        else:
            now = datetime.datetime.now()
        
            commentsService = CommentsService()
            comment = commentsService.create(todo_id=todoId, comment=comment, created=now.strftime("%Y-%m-%d %H:%M:%S"), user_id=current_user.id, is_del=0)
        
            if file and allowed_file(file.filename):     
                filename = secure_filename(file.filename)
                file.save(os.path.join(UPLOAD_FOLDER, filename))
                
                saveFilename = RELATIVE_UPLOAD_FOLDER + filename
                
                
                filesService = FilesService()               
                filesService.create(user_id=current_user.id, comment_id=comment.id, url=saveFilename, is_del=0, name=file.filename, todo_id=todoId, list_id=listId, project_id=projectId)
        
            result = True
    else:
        result = False
    
    if error:
        result = False
    
    return (result, error)

def add_project_item(name, description, priorityLevel, dueDate, token):
        
    """This function creates a new project.
    
    Params:
    
    name: String
    description: String
    priorityLevel: Integer
    dueDate: String
    token: String
    
    Result: Tuple(Boolean, String)"""
    
    result = False
    error = False
        
    if not name:
        error = 'Please enter a project name'
    elif not priorityLevel:
        error = 'Please choose a priority level'
    elif not isTokenValid(token):
        error = 'The request did not come from Pycamp'    
    else:
        error = False
        
    if not dueDate:
        dueDate = '0000-00-00 00:00:00'    
    
    now = datetime.datetime.now()
    
    if not error:
        projectsService = ProjectsService()
        project = projectsService.create(name=name, description=description, due_date=dueDate, created=now.strftime("%Y-%m-%d %H:%M:%S"), completion_date='0000-00-00 00:00:00', status='Open', priority_level=int(priorityLevel), user_id=current_user.id, is_del=0)
        
        projectUsersService = ProjectUsersService()
        projectUsersService.create(project_id=project.id, user_id=current_user.id)
        
        result = True
    else:
        result = False
        
    if error:
        result = False
    
    return (result, error)

def add_list_item(projectId, name, priorityLevel, dueDate, token):
        
    """This function adds a new todo list to a project.
    
    Params:
    
    projectId: Integer
    name: String
    priorityLevel: Integer
    dueDate: String
    token: String
    
    Result: Tuple(Boolean, String)"""
    
    error = False
    result = False
    
    if not name:
        error = 'Please enter a list name'
    elif not projectId:
        error = 'No project specified'
    elif not priorityLevel:
        error = 'Please choose a priority level'
    elif not isTokenValid(token):
        error = 'The request did not come from Pycamp'    
    else:
        error = False
        
    if projectId:
        projectsService = ProjectsService()
        project = projectsService.first(id=projectId)
        
        if not project:
            error = 'The project does not exist'
        
        if not has_access(projectId):
            error = 'You do not have access to this project'
        
    if not dueDate:
        dueDate = '0000-00-00 00:00:00'    
    
    now = datetime.datetime.now()
    
    if not error:
        listsService = ListsService()
        project = listsService.create(name=name, project_id=projectId, due_date=dueDate, created=now.strftime("%Y-%m-%d %H:%M:%S"), completion_date='0000-00-00 00:00:00', status='Open', priority_level=int(priorityLevel), user_id=current_user.id, is_del=0)
    
        result = True
    else:
        result = False
        
    if error:
        result = False
    
    return (result, error)

def edit_list_item(listId, name, priorityLevel, dueDate, token):
        
    """This function edits a new todo list to a project.
    
    Params:
    
    listId: Integer
    name: String
    priorityLevel: Integer
    dueDate: String
    token: String
    
    Result: Tuple(Boolean, String)"""
    
    error = False
    result = False
    
    if not name:
        error = 'Please enter a list name'
    elif not listId:
        error = 'No list specified'
    elif not priorityLevel:
        error = 'Please choose a priority level'
    elif not isTokenValid(token):
        error = 'The request did not come from Pycamp'    
    else:
        error = False
        
    if listId:
        listsService = ListsService()
        listResult = listsService.first(id=listId)
        
        if not listResult:
            error = 'The list does not exist'
        
        if not has_access(listResult.project_id):
            error = 'You do not have access to this project'
        
    if not dueDate:
        dueDate = '0000-00-00 00:00:00'    
    
    now = datetime.datetime.now()
    
    if not error:
        project = listsService.update(listResult, name=name, due_date=dueDate, priority_level=int(priorityLevel))
    
        result = True
    else:
        result = False
        
    if error:
        result = False
    
    return (result, error)

def edit_project_item(projectId, name, description, token):
        
    """This function edits a project.
    
    Params:
    
    projectId: Integer
    name: String
    description: String
    token: String
    
    Result: Tuple(Boolean, String)"""
    
    error = False
    result = False
    
    if not name:
        error = 'Please enter a list name'
    elif not projectId:
        error = 'No project specified'
    elif not isTokenValid(token):
        error = 'The request did not come from Pycamp'    
    else:
        error = False
        
    if projectId:
        projectsService = ProjectsService()
        projectsResult = projectsService.first(id=projectId)
        
        if not projectsResult:
            error = 'The project does not exist'
        
        if not has_access(projectId):
            error = 'You do not have access to this project'
        
    if not error:
        project = projectsService.update(projectsResult, name=name, description=description)
    
        result = True
    else:
        result = False
        
    if error:
        result = False
    
    return (result, error)

def edit_todo_comment(commentId, comment, token):
    
    """This function edits an existing todo comment.
    
    Params:
    
    commentId: Integer
    comment: String
    token: String
    
    Result: Tuple(Boolean, String)"""

    commentVal = comment
    result = False
    error = False
        
    if not commentId:
        error = 'No comment specified'    
    else:
        commentsService = CommentsService()
        commentResult = commentsService.first(id=commentId)
        
        if not commentVal and commentResult:
            commentVal = commentResult.comment
        
        if not commentResult:
            error = 'This comment does not exist'
        elif current_user.id != commentResult.user_id:
            error = 'This comment does not belong to you'
        else:
            if comment and not isTokenValid(token):
                error = 'The request did not come from Pycamp'
                
            if comment and not error:
                commentsService.update(commentResult, comment=comment)
                result = True
            else:
                result = False

    if error:
        result = False
        
    return (result, error)

def add_todo_item(listId, name, priorityLevel, dueDate, todoUser, token):
    
    """This function creates a new todo item.
    
    Params:
    
    listId: Integer
    name: String
    priorityLevel: Integer
    dueDate: String
    token: String
    
    Result: Tuple(Boolean, String)"""
    
    error = False
    result = False
        
    #copy code below into function, keep priorityLevels though    
    if not name:
        error = 'Please enter an item name'
    elif not listId:
        error = 'No list specified'
    elif not priorityLevel:
        error = 'Please choose a priority level'
    elif not isTokenValid(token):
        error = 'The request did not come from Pycamp'
    else:
        error = False
        
    if listId:
        listsService = ListsService()
        listResult = listsService.first(id=listId)
        
        if listResult:
            projectsService = ProjectsService()
            project = projectsService.first(id=listResult.project_id)
        
            if not project:
                error = 'The project does not exist'
            else:    
                projectUsersService = ProjectUsersService()
                projectUser = projectUsersService.first(project_id=listResult.project_id, user_id=current_user.id)
    
                if not projectUser:
                    error = 'You do not have access to this project'
        else:
            error = 'The list does not exist'
    
    if not dueDate:
        dueDate = '0000-00-00 00:00:00'    
    
    now = datetime.datetime.now()
    
    if not error:
        todosService = TodosService()
        project = todosService.create(name=name, list_id=listId, due_date=dueDate, created=now.strftime("%Y-%m-%d %H:%M:%S"), completion_date='0000-00-00 00:00:00', status='Open', priority_level=int(priorityLevel), user_id=current_user.id, is_del=0)
        
        if todoUser:
            todoAssignedUsersService = TodoAssignedUsersService()
            todoAssignedUsersService.create(user_id=todoUser, todo_id=project.id)
        result = True
    else:
        result = False
    
    return (result, error)

def delete_list_item(listId):
       
    """This function deletes a list item.
    
    Params:
    
    todoId: Integer
    
    Result: Tuple(Boolean, String)"""
    
    error = False
    result = False
     
    if not listId:
        error = 'No todo list specified'    
    else:

        listsService = ListsService()
        listResult = listsService.first(id=listId)
        
        if listResult: 
            canDelete = has_access(listResult.project_id)
        
        if not listResult:
            error = 'This todo list does not exist'
        elif not canDelete:
            error = 'You do not have permission to delete this list'
        else:
            if canDelete and not error:
                listsService.update(listResult, is_del=1)

                result = True
            else:
                result = False
                
    if error:
        result = False
        
    return (result, error)


def edit_todo_item(todoId, todoUserVal, title, token):
   
    """This function edits a todo item
    
    Params:
    
    todoId: Integer
    todoUserVal: Integer
    title: String
    token: String
    
    Result: Tuple(Boolean, String)"""
    
    error = False
    result = False
    
    titleVal = title
        
    if not todoId:
        error = 'No todo item specified'    
    else:
        todosService = TodosService()
        todoResult = todosService.first(id=todoId) 

        if not titleVal and todoResult:
            titleVal = todoResult.name
        
        if not todoResult:
            error = 'This todo item does not exist'
        elif current_user.id != todoResult.user_id:
            error = 'This todo item does not belong to you'
        else:

            listsService = ListsService()
            listResult = listsService.first(id=todoResult.list_id)
            
            if not listResult.project_id:
                error = 'Could not retrieve project'
            else:
                projectUsersService = ProjectUsersService()
                projectUsers = projectUsersService.get_project_users(listResult.project_id)

                todoAssignedUsersService = TodoAssignedUsersService()
                todoAssignedUsers = todoAssignedUsersService.first(todo_id=todoId)

                if todoAssignedUsers:
                    todoUser = todoAssignedUsers.user_id

            if title and not isTokenValid(token):
                error = 'The request did not come from Pycamp'
                
            if title and not error:
                todosService.update(todoResult, name=title)

                if todoUserVal:
                    if todoAssignedUsers:
                        todoAssignedUsersService.delete(todoAssignedUsers)
                    print "here"    
                    todoAssignedUsersService.create(user_id=todoUserVal, todo_id=todoId)

                result = True
            else:
                result = False
    
    if error:
        result = False
        
    return (result, error)

def get_project_users_from_list_item(listId):
    
    listsService = ListsService()
    listResult = listsService.first(id=listId)
    
    projectUsersService = ProjectUsersService()
    
    if listResult:
        projectUsers = projectUsersService.get_project_users(listResult.project_id)
    else:
        projectUsers = False
        
    return projectUsers

def get_project_users_from_todo_item(todoId):
        
    """This function retrieves a list of project users linked to the todo item.
    
    Params:
    
    todoId: Integer
    
    Result: Tuple(Boolean, String)"""
    
    if not todoId:
        return False
    
    todosService = TodosService()
    todoResult = todosService.first(id=todoId) 
    
    if not todoResult:
        return False
    
    listsService = ListsService()
    listResult = listsService.first(id=todoResult.list_id)
            
    if not listResult.project_id:
        return False
    else:
        projectUsersService = ProjectUsersService()
        projectUsers = projectUsersService.get_project_users(listResult.project_id)
        
    return projectUsers

def delete_comment_item(commentId):
        
    """This function deletes a comment item.
    
    Params:
    
    commentId: Integer
    
    Result: Tuple(Boolean, String)"""
    
    error = False
    result = False
    
    if not commentId:
        error = 'No comment item specified'    
    else:
        commentsService = CommentsService()
        commentsResult = commentsService.first(id=commentId) 

        if not commentsResult:
            error = 'This comment does not exist'
        elif current_user.id != commentsResult.user_id:
            error = 'This comment does not belong to you'
        else:
            commentsService.update(commentsResult, is_del=1)

            result = True
    
    if error:
        result = False
    
    return (result, error)

def delete_todo_item(todoId):
        
    """This function deletes a todo item.
    
    Params:
    
    todoId: Integer
    
    Result: Tuple(Boolean, String)"""
    
    error = False
    result = False
    
    if not todoId:
        error = 'No todo item specified'    
    else:
        todosService = TodosService()
        todoResult = todosService.first(id=todoId) 

        if not todoResult:
            error = 'This todo item does not exist'
        else:

            listsService = ListsService()
            listResult = listsService.first(id=todoResult.list_id)
            
            if not listResult.project_id:
                error = 'Could not retrieve project'
            else:
                canDelete = has_access(listResult.project_id)

            if canDelete and not error:
                todosService.update(todoResult, is_del=1)
                
                result = True
            else:
                error = 'You do not have permission to delete this todo item'
                
                result = False
    
    if error:
        result = False
    
    return (result, error)

def move_todo_item(listId, todoId):

    """This function moves a todo item into a new list
    
    Params:
    
    listId: Integer
    todoId: Integer
    
    Result: Tuple(Boolean, String)"""

    error = False
    result = False
        
    if not listId:
        error = 'No todo list specified'    
    elif not todoId:
        error = 'No todo item specified'
    else:

        listsService = ListsService()
        listResult = listsService.first(id=listId)
        
        todosService = TodosService()
        todoResult = todosService.first(id=todoId)

        if listResult: 
            canMove = has_access(listResult.project_id)
        
        if not listResult:
            error = 'This todo list does not exist'
        elif not canMove:
            error = 'You do not have permission to move this todo item'
        elif not todoResult:
            error = 'The todo item does not exist'
        else:
            if canMove and not error:
                todosService.update(todoResult, list_id=listId)

                result = True
            else:
                result = False
    
    if error:
        result = False
    
    return (result, error)

def parse_project_items(items):

    """This function extracts incomplete todos, complete todos and todo comment counts
    into a tuple.
        
    Params:
    
    items: ResultSet
    
    Result: Tuple(Dictionary, Dictionary, Dictionary)"""

    commentsService = CommentsService()

    todos = {}
    todosDone = {}
    numComments = False
    todoComments = {}

    for proj, lis, item in items:
        if item.list_id not in todos and item.status == "Open":
            todos[item.list_id] = {}
        elif item.list_id not in todosDone and item.status == "Closed":
            todosDone[item.list_id] = {}
                
        if item.status == "Open":    
            todos[item.list_id][item.id] = item
        elif item.status == "Closed":    
            todosDone[item.list_id][item.id] = item
            
        numComments = commentsService.get_num_comments(item.id)
            
        todoComments[item.id] = numComments

    return (todos, todosDone, todoComments)

def parse_list_items(items):

    """This function extracts incomplete todos, complete todos and todo comment counts
    into a tuple.
        
    Params:
    
    items: ResultSet
    
    Result: Tuple(Dictionary, Dictionary, Dictionary)"""
   
    commentsService = CommentsService()

    todos = {}
    todosDone = {}
    numComments = False
    todoComments = {}

    for lis, item in items:
        if item.list_id not in todos and item.status == "Open":
            todos[item.list_id] = {}
        elif item.list_id not in todosDone and item.status == "Closed":
            todosDone[item.list_id] = {}
                
        if item.status == "Open":    
            todos[item.list_id][item.id] = item
        elif item.status == "Closed":    
            todosDone[item.list_id][item.id] = item
            
        numComments = commentsService.get_num_comments(item.id)
            
        todoComments[item.id] = numComments

    return (todos, todosDone, todoComments)