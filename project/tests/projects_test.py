#!/usr/bin/python
 
from flask import Blueprint, render_template, abort, request
from project import app
from flask.ext.login import login_user, logout_user, current_user, login_required, current_user
from project.models.helpers.projects import *
from project.models.core.users import *
import unittest
from project.lib.template import *

class ProjectsTest(unittest.TestCase):
    """Sample test case"""
     
    # preparing to test
    def setUp(self):
        """ Setting up for the test """
    
    def login_test_user(self, username):        #with app.app_context():  
        #with app.test_request_context(): 
        usersService = UsersService()
        usernameResult = usersService.first(username=username)
        
        user = load_user(usernameResult.id)    
        login_user(user)
    
     
    # ending the test
    def tearDown(self):
        """Cleaning up after the test"""
     
    # test routine A
    def test_has_access(self):
        """Test routine has_access() function"""
        projectId = 2
        
        with app.test_request_context(): 
            
            #test success
            self.login_test_user('Dan2')
                        
            result = has_access(projectId)
        
            self.assertEqual(True, result, "The user Dan2 has access to project") 
    
            #test failure
            self.login_test_user('Dan')
                        
            result = has_access(projectId)
        
            self.assertEqual(False, result, "The user Dan does not have access to project") 
     
     
    def test_has_access_to_list(self):
        """Test routine has_access() function"""
        listId = 3
        
        with app.test_request_context(): 
            
            #test success
            self.login_test_user('Dan2')
                        
            (result, error) = has_access_to_list(listId)
            
            self.assertEqual(False, result, "The user Dan2 has access to list") 
            
            self.assertEqual(False, error, "has_access_to_list returns no error message") 
            
            #test failure
            self.login_test_user('Dan')
            
            (result, error) = has_access_to_list(listId)
        
            self.assertEqual(True, result, "The user Dan does not have access to list") 
            
            self.assertNotEqual(False, error, "has_access_to_list returns an error message")
            
            
    def test_toggle_todo_item_status(self):
        
        todoId = 41
         
        with app.test_request_context(): 
            
            #test success
            self.login_test_user('Dan2')
            
            (token, session) = generate_test_token()
            
            (result, error) = toggle_todo_item_status(todoId, 'incomplete', token)
            
            self.assertEqual(True, result, "The todo item status has been closed") 
            
            self.assertEqual(False, error, "has_access_to_list returns no error message")
            
             
            (result, error) = toggle_todo_item_status(todoId, 'complete', token)
            
            self.assertEqual(True, result, "The todo item status has been opened") 
            
            self.assertEqual(False, error, "has_access_to_list returns no error message") 
            
            
            
            (result, error) = toggle_todo_item_status(todoId, 'invalid_status', token)
            
            self.assertEqual(False, result, "Invalid status provided to toggle_todo_item_status") 
            
            self.assertNotEqual(False, error, "has_access_to_list returns an error message") 
           
             
            #(result, error) = toggle_todo_item_status(todoId, 'complete', 'invalid_token')
            
            #self.assertEqual(False, result, "Invalid token provided to toggle_todo_item_status") 
            
            #self.assertNotEqual(False, error, "has_access_to_list returns an error message") 
            
           
            self.login_test_user('Dan')
            
            (result, error) = toggle_todo_item_status(todoId, 'complete', token)
            
            self.assertEqual(False, result, "Invalid user provided to toggle_todo_item_status") 
            
            self.assertNotEqual(False, error, "has_access_to_list returns an error message") 
           
           
    def test_add_comment_item(self):
        
        todoId = 41
        listId = 11
        projectId = 4
         
        with app.test_request_context(): 
            
            #test success
            self.login_test_user('Dan2')
            
            (token, session) = generate_test_token()
            
            comment = 'This is a test comment for unit testing'

            (result, error) = add_comment_item(todoId, listId, projectId, comment, "", token)
            
            self.assertEqual(True, result, "The todo comment has been added successfully") 
            
            self.assertEqual(False, error, "add_comment_item returns no error message")
            
              
            self.login_test_user('Dan')
            
            (result, error) = add_comment_item(todoId, listId, projectId, comment, "", token)
            
            self.assertEqual(False, result, "The user cannot add a comment to this todo item.") 
            
            self.assertNotEqual(False, error, "add_comment_item returns an error message")
           
           
    def test_add_list_item(self):
        
        projectId = 4
        priorityLevel = 2
        
        with app.test_request_context(): 
            
            #test success
            self.login_test_user('Dan2')
            
            (token, session) = generate_test_token()
            
            name = 'Test List Item'

            (result, error) = add_list_item(projectId, name, priorityLevel, "", token)
            
            self.assertEqual(True, result, "The list item has been added successfully") 
            
            self.assertEqual(False, error, "add_list_item returns no error message")
            
            
            self.login_test_user('Dan')
            
            name = 'Test List Item'

            (result, error) = add_list_item(projectId, name, priorityLevel, "", token)
            
            self.assertEqual(False, result, "The list item could not be added. Permission Denied.") 
            
            self.assertNotEqual(False, error, "add_list_item returns an error message")
            

    def test_edit_comment_item(self):
        
        commentId = 32
        
        with app.test_request_context(): 
            
            #test success
            self.login_test_user('Dan2')
            
            (token, session) = generate_test_token()
            
            comment = 'Comment edited by unit test'

            (result, error) = edit_todo_comment(commentId, comment, token)
            
            self.assertEqual(True, result, "The comment item has been edited") 
            
            self.assertEqual(False, error, "edit_todo_comment returns no error message")
            
            
            self.login_test_user('Dan')
            
            comment = 'Comment edited by unit test'

            (result, error) = edit_todo_comment(commentId, comment, token)
            
            self.assertEqual(False, result, "The comment item could not be edited. Permission Denied.") 
            
            self.assertNotEqual(False, error, "edit_todo_comment returns an error message")
            
    
    def test_add_todo_item(self):
        
        listId = 13
        priorityLevel = 2
        todoUser = 2
        
        with app.test_request_context(): 
            
            #test success
            self.login_test_user('Dan2')
            
            (token, session) = generate_test_token()
            
            name = 'Test Todo Item'

            (result, error) = add_todo_item(listId, name, priorityLevel, "", todoUser, token)
            
            self.assertEqual(True, result, "The todo item has been added successfully") 
            
            self.assertEqual(False, error, "add_todo_item returns no error message")
            
            
            self.login_test_user('Dan')
            
            name = 'Test Todo Item'

            (result, error) = add_todo_item(listId, name, priorityLevel, "", todoUser, token)
            
            self.assertEqual(False, result, "The todo item could not be added. Permission Denied.") 
            
            self.assertNotEqual(False, error, "add_todo_item returns an error message")
            
    
    def test_delete_list_item(self):
        
        listId = 13
        
        with app.test_request_context(): 
            
            #test success
            self.login_test_user('Dan2')
            
            (result, error) = delete_list_item(listId)
            
            self.assertEqual(True, result, "The list item has been deleted successfully") 
            
            self.assertEqual(False, error, "delete_list_item returns no error message")
            
            
            self.login_test_user('Dan')
            
            (result, error) = delete_list_item(listId)
            
            self.assertEqual(False, result, "The list item could not be deleted. Permission Denied.") 
            
            self.assertNotEqual(False, error, "delete_list_item returns an error message")
            
    def test_edit_list_item(self):
        
        listId = 13
        name = 'Unit Testing'
        priorityLevel = 2
        dueDate = '2014-04-15 12:12:57'
        
        with app.test_request_context(): 
            
            #test success
            self.login_test_user('Dan2')
            
            (result, error) = edit_list_item(listId, name, priorityLevel, dueDate, 'token')
            
            self.assertEqual(True, result, "The list item has been edited successfully") 
            
            self.assertEqual(False, error, "edit_list_item returns no error message")
            
            
            self.login_test_user('Dan')
            
            (result, error) = edit_list_item(listId, name, priorityLevel, dueDate, 'token')
            
            self.assertEqual(False, result, "The list item could not be edited. Permission Denied.") 
            
            self.assertNotEqual(False, error, "edit_list_item returns an error message")
            
    def test_edit_project_item(self):
        
        projectId = 4
        name = 'Unit Testing'
        description = 'Edited by unit test'
        
        with app.test_request_context(): 
            
            #test success
            self.login_test_user('Dan2')
            
            (result, error) = edit_project_item(projectId, name, description, 'token')
            
            self.assertEqual(True, result, "The project has been edited successfully") 
            
            self.assertEqual(False, error, "edit_project_item returns no error message")
            
            
            self.login_test_user('Dan')
            
            (result, error) = edit_project_item(projectId, name, description, 'token')
            
            self.assertEqual(False, result, "The project could not be edited. Permission Denied.") 
            
            self.assertNotEqual(False, error, "edit_project_item returns an error message")
            

    def test_edit_todo_item(self):
        
        todoId = 42
        todoUserVal = 2
        
        with app.test_request_context(): 
            
            #test success
            self.login_test_user('Dan2')
            
            (token, session) = generate_test_token()
            
            title = 'Todo item edited by unit test'

            (result, error) = edit_todo_item(todoId, todoUserVal, title, token)
            
            self.assertEqual(True, result, "The todo item has been edited") 
            
            self.assertEqual(False, error, "edit_todo_item returns no error message")
            
            
            self.login_test_user('Dan')
            
            title = 'Todo item edited by unit test'

            (result, error) = edit_todo_item(todoId, todoUserVal, title, token)
            
            self.assertEqual(False, result, "The todo item could not be edited. Permission Denied.") 
            
            self.assertNotEqual(False, error, "edit_todo_item returns an error message")
            
    
    def test_get_project_users_from_todo_item(self):
        
        todoId = 42
        todoUserVal = 2
        
        with app.test_request_context(): 
            
            #test success
            projectUsers = get_project_users_from_todo_item(todoId)
            
            for project, user in projectUsers:
                self.assertEqual(2, user.id, "The user Dan2 exists in the todo item's project users list.")
                
     
    def test_delete_todo_item(self):
        
        todoId = 43
        
        with app.test_request_context(): 
            
            #test success
            self.login_test_user('Dan2')
            
            (result, error) = delete_todo_item(todoId)
            
            self.assertEqual(True, result, "The todo item has been deleted successfully") 
            
            self.assertEqual(False, error, "delete_todo_item returns no error message")
            
            
            self.login_test_user('Dan')
            
            (result, error) = delete_todo_item(todoId)
            
            self.assertEqual(False, result, "The todo item could not be deleted. Permission Denied.") 
            
            self.assertNotEqual(False, error, "delete_todo_item returns an error message")
            
    def test_delete_comment_item(self):
        
        commentId = 52
        
        with app.test_request_context(): 
            
            #test success
            self.login_test_user('Dan2')
            
            (result, error) = delete_comment_item(commentId)
            
            self.assertEqual(True, result, "The comment has been deleted successfully") 
            
            self.assertEqual(False, error, "delete_comment_item returns no error message")
            
            
            self.login_test_user('Dan')
            
            (result, error) = delete_comment_item(commentId)
            
            self.assertEqual(False, result, "The comment could not be deleted. Permission Denied.") 
            
            self.assertNotEqual(False, error, "delete_comment_item returns an error message")         
    
    def test_move_todo_item(self):
        
        listId = 14
        todoId = 43
        
        with app.test_request_context(): 
            
            #test success
            self.login_test_user('Dan2')
            
            (result, error) = move_todo_item(listId, todoId)
            
            self.assertEqual(True, result, "The todo item has been moved successfully") 
            
            self.assertEqual(False, error, "move_todo_item returns no error message")
            
            
            self.login_test_user('Dan')
            
            (result, error) = move_todo_item(listId, todoId)
            
            self.assertEqual(False, result, "The todo item could not be moved. Permission Denied.") 
            
            self.assertNotEqual(False, error, "move_todo_item returns an error message")