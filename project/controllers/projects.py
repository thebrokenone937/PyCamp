from flask import Blueprint, render_template, abort, request
from project.lib.template import render_custom_template, isTokenValid
from project.lib.acl import check_acl
from project.models.core.priority_levels import PriorityLevelsService
from project.models.core.projects import ProjectsService
from project.models.core.project_users import ProjectUsersService
from project.models.core.lists import ListsService
from project.models.core.todos import TodosService
from project.models.core.comments import CommentsService
from project.models.core.users import UsersService
from project.models.core.files import FilesService
from project.models.core.todo_assigned_users import TodoAssignedUsersService
from project.models.helpers.projects import *
import datetime
import flask
from flask.ext.login import current_user
from project.models.uploads import *

projects = Blueprint('projects', __name__)

@projects.route('/projects/move-todo/<listId>/<todoId>', methods=["POST", "GET"])
@check_acl('/projects/move-todo')
def move_todo(listId, todoId):
        
    error = False
    canMove = False
    success = False

    (success, error) = move_todo_item(listId, todoId)

    return render_custom_template('projects/move_todo.html', success=success, error=error)

@projects.route('/projects/delete-list/id/<listId>', methods=["POST", "GET"])
@check_acl('/projects/delete-list')
def delete_list(listId):
        
    error = False
    canDelete = False
    success = False

    (success, error) = delete_list_item(listId)

    return render_custom_template('projects/delete_list.html', success=success, error=error)

@projects.route('/projects/delete-todo/id/<todoId>', methods=["POST", "GET"])
@check_acl('/projects/delete-todo')
def delete_todo(todoId):
        
    error = False
    success = False

    (success, error) = delete_todo_item(todoId)

    return render_custom_template('projects/delete_todo.html', success=success, error=error)

@projects.route('/projects/delete-comment/id/<commentId>', methods=["POST", "GET"])
@check_acl('/projects/delete-comment')
def delete_comment(commentId):
        
    error = False
    success = False

    (success, error) = delete_comment_item(commentId)

    return render_custom_template('projects/delete_comment.html', success=success, error=error)


@projects.route('/projects/edit-todo/<todoId>/<listId>', defaults = {'action': False}, methods=["POST", "GET"])
@projects.route('/projects/edit-todo/<todoId>/<listId>/<action>', methods=["POST", "GET"])
@check_acl('/projects/edit-todo')
def edit_todo(todoId, listId, action):
    if request.method == "POST":
        title = request.form["title"] 
        todoUserVal = request.form["todoUser"]
        token = request.form["token"]
        action = request.form["action"]
        titleVal = title
    else:
        title = False
        titleVal = False
        todoUserVal = False
        token = False
    
    error = False
    projectUsers = False
    todoUser = False
    success = False
    
    if request.method == "POST":
        (success, error) = edit_todo_item(todoId, todoUserVal, title, token)
    
    projectUsers = get_project_users_from_todo_item(todoId)
        
    todosService = TodosService()
    todoResult = todosService.first(id=todoId) 

    if not titleVal and todoResult:
        titleVal = todoResult.name
    
    
    todoAssignedUsersService = TodoAssignedUsersService()
    todoAssignedUsers = todoAssignedUsersService.first(todo_id=todoId)

    if todoAssignedUsers:
        todoUser = todoAssignedUsers.user_id
                
    return render_custom_template('projects/edit_todo.html', action=action, listId=listId, todoUser=todoUser, projectUsers=projectUsers, success=success, error=error, title=titleVal, todoId=todoId)


@projects.route('/projects/show-list/<listId>')
@check_acl('/projects/show-list')
def show_list(listId):
    
    error = False
    projectId = False
    todos = {}
    todosDone = {}
    todoComments = {}

    listsService = ListsService()
    lists = listsService.find(id=listId, is_del=0)
    
    for listVal in lists:
        if listVal.project_id:
            projectId = listVal.project_id
            break

    projectUser = False

    if projectId:
        projectUsersService = ProjectUsersService()
        projectUser = projectUsersService.first(project_id=projectId, user_id=current_user.id)
    
    if not projectUser:
        error = 'You do not have access to this project'
        projectTitle = 'Access Denied'
        description = error
        projectId = False
        lists = False
    else:
        error = False
        projectsService = ProjectsService()
        project = projectsService.first(id=projectId)
        projectTitle = project.name
        description = project.description
        projectId = project.id

    projectsService = ProjectsService()
    items = projectsService.get_list_items(listId)
        
    (todos, todosDone, todoComments) = parse_list_items(items)

    return render_custom_template('projects/display_list.html', projectTitle=projectTitle, description=description, todosDone=todosDone, todoComments=todoComments, todos=todos,error=error, lists=lists, projectId=projectId)


@projects.route('/projects/show-lists/<projectId>')
@check_acl('/projects/show-lists')
def show_lists(projectId):
    projectUsersService = ProjectUsersService()
    projectUser = projectUsersService.first(project_id=projectId, user_id=current_user.id)
    
    todos = {}
    todosDone = {}
    todoComments = {}
    projectComments = False
    projectUsers = False
    
    if not projectUser:
        error = 'You do not have access to this project'
        projectTitle = 'Access Denied'
        description = error
        projectId = False
        lists = False
    else:
        error = False
        projectsService = ProjectsService()
        project = projectsService.first(id=projectId)
        projectTitle = project.name
        description = project.description
        projectId = project.id
        
        projectUsers = projectUsersService.get_project_users(projectId)
        
        listsService = ListsService()
        lists = listsService.find(project_id=project.id, is_del=0)
    
        items = projectsService.get_project_items(projectId)
        
        (todos, todosDone, todoComments) = parse_project_items(items)
        
        commentsService = CommentsService()
        filesService = FilesService()
         
        projectComments = commentsService.get_project_comments(projectId, 5)
        projectFiles = filesService.get_project_files(projectId, 5)
        
    return render_custom_template('projects/display_lists.html', projectFiles=projectFiles, projectUsers=projectUsers, todosDone=todosDone, projectComments=projectComments, todoComments=todoComments, todos=todos, projectId=projectId, projectTitle=projectTitle, description=description, error=error, lists=lists)

@projects.route('/projects/list-projects')
@check_acl('/projects/list-projects')
def list_projects():
    projectsService = ProjectsService()
    projects = projectsService.get_projects(current_user.id)
    
    return render_custom_template('projects/list.html', projects=projects)


@projects.route('/projects/list-user-items/<userId>')
@check_acl('/projects/list-user-items')
def list_user_items(userId):
    projectsService = ProjectsService()
    items = projectsService.get_user_items(userId)
   
    usersService = UsersService()
    user = usersService.first(id=userId)
     
    projects = {}
    lists = {}
    todos = {}
    todosDone = {}
    todoComments = {}
    error = False
     
    commentsService = CommentsService()
    
    for project, listItem, item, assignedUser in items:
        projects[project.id] = project
        
        if project.id not in lists:
            lists[project.id] = {}
        
        lists[project.id][listItem.id] = listItem
        
        if project.id not in todos and item.status == 'Open':
            todos[project.id] = {}
        
        if item.status == 'Open':
            if listItem.id not in todos[project.id]:
                todos[project.id][listItem.id] = {}
        
            todos[project.id][listItem.id][item.id] = item
        
        if project.id not in todosDone and item.status == 'Closed':
            todosDone[project.id] = {}
        
        if item.status == 'Closed':
            if listItem.id not in todosDone[project.id]:
                todosDone[project.id][listItem.id] = {}
        
            todosDone[project.id][listItem.id][item.id] = item
        
        numComments = commentsService.get_num_comments(item.id)
            
        todoComments[item.id] = numComments
    
    return render_custom_template('projects/list_user_items.html', user=user, error=error, todosDone=todosDone, todoComments=todoComments, projects=projects, lists=lists, todos=todos)

@projects.route('/projects/create-todo/<listId>')
@check_acl('/projects/create-todo')
def create_todo(listId):
    priorityLevelsService = PriorityLevelsService()
    priorityLevels = priorityLevelsService.all()
    
    projectUsers = get_project_users_from_list_item(listId) 
    
    error = False
    blockAccess = False
    
    (blockAccess, error) = has_access_to_list(listId)
     
    return render_custom_template('projects/add_todo.html', projectUsers=projectUsers, blockAccess=blockAccess, error=error, listId=listId, priorityLevels=priorityLevels)

@projects.route('/projects/add-todo', methods=["POST"])
@check_acl('/projects/add-todo')
def add_todo():
    name = request.form["name"]
    listId = request.form["listId"]
    priorityLevel = request.form["priorityLevel"]
    dueDate = request.form["dueDate"]
    token = request.form["token"]
    todoUser = request.form["todoUser"]
    
    projectUsers = get_project_users_from_list_item(listId) 
    
    priorityLevelsService = PriorityLevelsService()
    priorityLevels = priorityLevelsService.all()

    (success, error) = add_todo_item(listId, name, priorityLevel, dueDate, todoUser, token)
       
    return render_custom_template('projects/add_todo.html', projectUsers=projectUsers, success=success, error=error, priorityLevels=priorityLevels, name=name, listId=listId, priorityLevel=priorityLevel, dueDate=dueDate)


@projects.route('/projects/edit-comment/<commentId>', methods=["POST", "GET"])
@check_acl('/projects/edit-comment')
def edit_comment(commentId):
    if request.method == "POST":
        comment = request.form["comment"]
        token = request.form["token"]
        commentVal = comment
    else:
        comment = False
        commentVal = False
        
    error = False
    success = False
    
    if request.method == "POST":
        (success, error) = edit_todo_comment(commentId, commentVal, token) 
    
    
    if not commentId:
        error = 'No comment specified'    
    else:
        commentsService = CommentsService()
        commentResult = commentsService.first(id=commentId)
        
        if not commentVal and commentResult:
            commentVal = commentResult.comment
    
    return render_custom_template('projects/edit_comment.html', success=success, error=error, comment=commentVal, commentId=commentId)


@projects.route('/projects/create-list/<projectId>')
@check_acl('/projects/create-list')
def create_list(projectId):
    priorityLevelsService = PriorityLevelsService()
    priorityLevels = priorityLevelsService.all()
    
    if has_access(projectId):
        blockAccess = False
        error = False
    else:
        blockAccess = True
        error = 'You do not have access to this project'
    
    return render_custom_template('projects/add_list.html', blockAccess=blockAccess, error=error, projectId=projectId, priorityLevels=priorityLevels)

@projects.route('/projects/add-list', methods=["POST"])
@check_acl('/projects/add-list')
def add_list():
    name = request.form["name"]
    projectId = request.form["projectId"]
    priorityLevel = request.form["priorityLevel"]
    dueDate = request.form["dueDate"]
    token = request.form["token"]
    
    priorityLevelsService = PriorityLevelsService()
    priorityLevels = priorityLevelsService.all()
    
    (success, error) = add_list_item(projectId, name, priorityLevel, dueDate, token)
     
    return render_custom_template('projects/add_list.html', success=success, error=error, priorityLevels=priorityLevels, name=name, projectId=projectId, priorityLevel=priorityLevel, dueDate=dueDate)

@projects.route('/projects/edit-list/<listId>', methods=["POST", "GET"])
@check_acl('/projects/edit-list')
def edit_list(listId):
    
    error = False
    
    if request.method == "POST":
        name = request.form["name"]
        listId = request.form["listId"]
        priorityLevel = request.form["priorityLevel"]
        dueDate = request.form["dueDate"]
        token = request.form["token"]
    else:
        if listId:
            listsService = ListsService()
            listResult = listsService.first(id=listId)
        else:
            listResult = False
            
        success = False
        
        if listResult:
            priorityLevel = listResult.priority_level
            dueDate = listResult.due_date
            name = listResult.name
        else:
            error = 'The list does not exist'
    
    priorityLevelsService = PriorityLevelsService()
    priorityLevels = priorityLevelsService.all()
    
    if request.method == "POST":
        (success, error) = edit_list_item(listId, name, priorityLevel, dueDate, token)
     
    return render_custom_template('projects/edit_list.html', success=success, error=error, priorityLevels=priorityLevels, name=name, listId=listId, priorityLevel=priorityLevel, dueDate=dueDate)

@projects.route('/projects/edit-project/<projectId>', methods=["POST", "GET"])
@check_acl('/projects/edit-project')
def edit_project(projectId):
    
    error = False
    
    if request.method == "POST":
        name = request.form["name"]
        projectId = request.form["projectId"]
        description = request.form["description"]
        token = request.form["token"]
    else:
        if projectId:
            projectsService = ProjectsService()
            projectsResult = projectsService.first(id=projectId)
        else:
            projectsResult = False
            
        success = False
        
        if projectsResult:
            description = projectsResult.description
            name = projectsResult.name
        else:
            error = 'The project does not exist'
            name = False
            description = False
    
    if request.method == "POST":
        (success, error) = edit_project_item(projectId, name, description, token)
     
    return render_custom_template('projects/edit_project.html', success=success, error=error, description=description, name=name, projectId=projectId)


@projects.route('/projects/create')
@check_acl('/projects/create')
def create():
    priorityLevelsService = PriorityLevelsService()
    priorityLevels = priorityLevelsService.all()
    
    return render_custom_template('projects/add.html', priorityLevels=priorityLevels)

@projects.route('/projects/add', methods=["POST"])
@check_acl('/projects/add')
def add():
    name = request.form["name"]
    description = request.form["description"]
    priorityLevel = request.form["priorityLevel"]
    dueDate = request.form["dueDate"]
    token = request.form["token"]
    
    priorityLevelsService = PriorityLevelsService()
    priorityLevels = priorityLevelsService.all()
    
    (success, error) = add_project_item(name, description, priorityLevel, dueDate, token)
        
    return render_custom_template('projects/add.html', success=success, error=error, priorityLevels=priorityLevels, name=name, description=description, priorityLevel=priorityLevel, dueDate=dueDate)

@projects.route('/projects/show-todo/<todoId>', methods=["POST", "GET"])
@check_acl('/projects/show-todo')
def show_todo(todoId):
    if request.method == "POST":
        todoId = request.form["todoId"]
        comment = request.form["comment"]
        token = request.form["token"]
        file = request.files['file']
    else:
        comment = False
        
    todoTitle = False
    listTitle = False
    listId = False
    projectId = False
    projectTitle = False
    error = False
    blockAccess = True
    commentFiles = {}
    
    filesService = FilesService()               
    
    if not todoId:
        error = 'No item specified'
    else:
        todosService = TodosService()
        item = todosService.first(id=todoId)
        
        todoTitle = item.name
        status = item.status
        
        if not item:
            error = 'The to-do item does not exist'
        else:
            listsService = ListsService()
            listResult = listsService.first(id=item.list_id)
            
            if not listResult:
                error = 'No list associated with item'
            else:
                listTitle = listResult.name
                listId = listResult.id
                
                projectsService = ProjectsService()
                project = projectsService.first(id=listResult.project_id)
                
                if not project:
                    error = 'No project associated with item'
                else:
                    projectTitle = project.name
                    projectId = project.id
                    
                    if not has_access(projectId):
                        error = 'You do not have access to this project'
                        blockAccess = True
                    else:
                        blockAccess = False
                        
                    
    commentsService = CommentsService()
    
    if not error and comment:
        (success, error) = add_comment_item(todoId, listId, projectId, comment, file, token)
    else:
        success  = False
         
    comments = commentsService.get_comments(todoId)
    
    files = filesService.find(todo_id=todoId)
                        
    for f in files:
        commentFiles[f.comment_id] = f;
    
    return render_custom_template('projects/show_todo.html', commentFiles=commentFiles, blockAccess=blockAccess, status=status, comments=comments, success=success, error=error, projectId=projectId, projectTitle=projectTitle, listTitle=listTitle, listId=listId, todoTitle=todoTitle, todoId=todoId)

@projects.route('/projects/toggle-todo-status/id/<todoId>/status/<status>/token/<token>', methods=["POST", "GET"])
@check_acl('/projects/toggle-todo-status')
def toggle_todo_status(todoId, status, token):
    
    error = False
    
    (success, error) = toggle_todo_item_status(todoId, status, token)
     
    return render_custom_template('projects/toggle_todo_status.html', error=error)

@projects.route('/projects/add-users-to-project/id/<projectId>', methods=["POST", "GET"])
@check_acl('/projects/add-users-to-projects')
def add_users_to_project(projectId):
    #grab emails from post data
    #check user email exists
    #check email not equal to current user
    #check project belongs to user
    #add users to project
    error = False
    
    if request.method == "POST":
        projectId = request.form["projectId"]
        count = int(request.form["count"])
        token = request.form["token"]
        
        emails = {}
        
        if not isTokenValid(token):
            error = 'The request did not come from Pycamp' 
        
        if count > 0:
            for i in range(count):
                name = "email_" + str(i+1)
                #print name
                if name in request.form:
                    if request.form[name]:
                        emails[name] = request.form[name]
        else:
            error = 'Please enter at least one email address'
    else:
        emails = False
        
    usersToAdd = {}
    usersNotAdded = {}
      
    projectsService = ProjectsService()
    project = projectsService.first(id=projectId)
       
    blockAccess = True
                
    if not project:
        error = 'No project associated with this id'
        blockAccess = True
    elif project.user_id != current_user.id:
        error = 'This project does not belong to you'
        blockAccess = True
    else:
        blockAccess = False 
           
    if emails and not error:
        usersService = UsersService()
        projectUsersService = ProjectUsersService()
        
        for key, value in emails.iteritems():
            if value != current_user.email:
                #check if user exists
                user = usersService.first(email=value)
                
                if user:
                    projectUserExists = projectUsersService.first(project_id=projectId, user_id=user.id)
                
                    if not projectUserExists:
                        projectUsersService.create(project_id=projectId, user_id=user.id)
                        usersToAdd[user.id] = user.email
                else:
                    usersNotAdded[value] = value    
                
            
    return render_custom_template('projects/add_users_to_project.html', blockAccess=blockAccess, project=project, error=error, usersToAdd=usersToAdd, usersNotAdded=usersNotAdded)

@projects.route('/projects/display-single-list/id/<listId>', methods=["POST", "GET"])
@check_acl('/projects/display-single-list')
def display_single_list(listId):
    todos = {}
    todosDone = {}
    todoComments = {}
    error = False
    
    listsService = ListsService()
    listRecord = listsService.first(id=listId, is_del=0)
    
    if not listRecord:
        error = 'The list does not exist'
    else:
        projectUsersService = ProjectUsersService()
        projectUser = projectUsersService.first(project_id=listRecord.project_id, user_id=current_user.id)
        
        if not projectUser:
            error = 'You do not have access to this list'
    
    if not error:
        items = listsService.get_list_items(listRecord.id)
        
        commentsService = CommentsService()
        
        for lis, item in items:
            if item.status == "Open":    
                todos[item.id] = item
            elif item.status == "Closed":    
                todosDone[item.id] = item
            
            numComments = commentsService.get_num_comments(item.id)
            
            todoComments[item.id] = numComments
    
    return render_custom_template('projects/display_single_list.html', todoComments=todoComments, error=error, list=listRecord, todos=todos, todosDone=todosDone)
