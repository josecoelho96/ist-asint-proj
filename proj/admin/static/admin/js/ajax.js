function getMessages() {
    $.get('/admin/get_messages', {room:$("#room-id").val()} ,function(data){
        messages = data.messages;

        var table = $('#messages')
        $("#messages tr").remove();

        $.each(messages, function(key, value) { 
            var row = $("<tr/>");
            row.append($("<td/>").append('<h6>' + value.date + '</h6>'));
            row.append($("<td/>").append('<h6>' + value.content + '</h6>'));
            table.append(row);
        });

        users = data.users;
        var table_users = $('#users')
        $("#users tr").remove();
        for (var i = 0; i < users.length; i++) {
            var row = $("<tr/>");
            row.append($("<td/>").append('<h6>' + users[i] + '</h6>'));
            table_users.append(row);
        }
    });
}

setInterval(getMessages, 1000);

$(document).ready(function() {
    $("#send-btn").on('click', function(event){
            event.preventDefault();
            $.ajax({
                 type:"POST",
                 url:"/admin/send_message",
                 data: {
                    'content': $('#send-txt').val(),
                    'room_id': $('#room-id').val(),
                    'csrfmiddlewaretoken':document.getElementsByName('csrfmiddlewaretoken')[0].value,
                },
                success: function(data){
                     $('#message').html(data.message); 
                     
                    }
            });
            $("#send-txt").val('');
            return false;
        });

    $("#send-txt").on('keyup', function (e) {
        if (e.keyCode == 13) {
            event.preventDefault();
            $.ajax({
                 type:"POST",
                 url:"/admin/send_message",
                 data: {
                    'content': $('#send-txt').val(),
                    'room_id': $('#room-id').val(),
                    'csrfmiddlewaretoken':document.getElementsByName('csrfmiddlewaretoken')[0].value,
                },
                success: function(data){
                     $('#message').html(data.message); 
                     
                    }
            });
            $("#send-txt").val('');
            return false;
        }
    });
});