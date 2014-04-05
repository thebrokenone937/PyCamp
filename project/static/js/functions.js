function toggleTodoStatus(todoId)
 {
 	var isChecked = $('#todoCheck_' + todoId).is(":checked");
 		
 	if ( isChecked ) {
 		$('#todoTitle_' + todoId).css("text-decoration", "line-through");
 		$('#todoTitle_' + todoId).css("color", "#ccc");
 		var status = "complete";
 	} else {
 		$('#todoTitle_' + todoId).css("text-decoration", "none");
 		$('#todoTitle_' + todoId).css("color", "#369");
 		var status = "incomplete"; 
 	}
 	
 	
 	$.ajax({
	  url: "/projects/toggle-todo-status/id/" + todoId + "/status/" + status + "/token/{{ token }}",
	  context: document.body
	}).done(function(data) {
	  alert("done:" + data);
	});
 }
 
 function displayList(listId)
 {
 	$('#list_' + listId).html("Refreshing list...");
 	
 	$.ajax({
	  url: "/projects/display-single-list/id/" + listId,
	  context: document.body
	}).done(function(data) {
	  $('#list_' + listId).html(data);
	});
 }

 function deleteComment(commentId)
 {
    var r = confirm("Are you sure you want to delete this comment?");
    
    if ( r==false ) {
        return false;
    } 
    
    $.ajax({
	  url: "/projects/delete-comment/id/" + commentId,
	  context: document.body
	}).done(function(data) {
        if ( data.trim() == "Success" ) {
            alert("Comment deleted successfully");
	        $('#commentDiv_' + commentId).hide();
        } else {
            alert(data);
        }
	});
 }

 function deleteTodo(todoId)
 {
    var r = confirm("Are you sure you want to delete this todo item?");
    
    if ( r==false ) {
        return false;
    } 
    
    $.ajax({
	  url: "/projects/delete-todo/id/" + todoId,
	  context: document.body
	}).done(function(data) {
        if ( data.trim() == "Success" ) {
            alert("Todo item deleted successfully");
	        $('#todo_' + todoId).hide();
        } else {
            alert(data);
        }
	});
 }


 function deleteList(listId)
 {
    var r = confirm("Are you sure you want to delete this todo list?");
    
    if ( r==false ) {
        return false;
    } 
    
    $.ajax({
	  url: "/projects/delete-list/id/" + listId,
	  context: document.body
	}).done(function(data) {
        if ( data.trim() == "Success" ) {
            alert("Todo list deleted successfully");
	        $('#list_' + listId).hide();
	        $('#addTodoLink_' + listId).hide();
        } else {
            alert(data);
        }
	});
 }

 function showCompletedTodos(listId)
 {
    $('#todosDoneLink_' + listId).hide();
    $('#todosDone_' + listId).show();
 }


 function hideCompletedTodos(listId)
 {
    $('#todosDoneLink_' + listId).show();
    $('#todosDone_' + listId).hide();
 }

 function allowDrop(ev, listId)
 {
    $('#list_' + listId).css('background-color', '#ccc'); 
    ev.preventDefault();
 }


 function changeListColor(ev, listId)
 {
    $('#list_' + listId).css('background-color', '#fff'); 
    ev.preventDefault();
 }

 function drag(ev)
 {
    ev.dataTransfer.setData("Text",ev.target.id);
 }

 function drop(ev, listId)
 {
    ev.preventDefault();

    var dataId = ev.dataTransfer.getData("Text");
    
    var parts = dataId.split("_");

    var fromListId = parts[1];
    var todoId = parts[2];

    $('#list_' + listId).css('background-color', '#fff'); 
    
    $.ajax({
	  url: "/projects/move-todo/" + listId + "/" + todoId,
	  context: document.body
	}).done(function(data) {
        if ( data.trim() == "Success" ) {
            alert("Todo item moved successfully");
            displayList(listId);
            displayList(fromListId);
        } else {
            alert(data);
        }
	});
 }
