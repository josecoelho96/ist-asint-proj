function getMessages() {
    $.get('/get_messages', function(data){
        messages = data.messages;
        var table = $('#messages')
        $("#messages tr").remove();
        for (var i = 0; i < messages.length; i++) {
            var row = $("<tr/>");
            row.append($("<td/>").append('<h6>' + messages[i].date + '</h6>'));
            row.append($("<td/>").append('<h6>' + messages[i].content + '</h6>'));
            table.append(row);
        }
    });
}

setInterval(getMessages, 15000);

$(document).ready(function() {
    $("#send-btn").on('click', function(event){
            event.preventDefault();
            $.ajax({
                 type:"POST",
                 url:"/send_message",
                 data: {
                        'content': $('#send-txt').val(),
                        'csrfmiddlewaretoken':document.getElementsByName('csrfmiddlewaretoken')[0].value 
                    },
                success: function(data){
                     $('#send').find('input:text').val('');
                     $('#message').html(data.message); 
                     
                    }             
            });
            return false;
        });

});