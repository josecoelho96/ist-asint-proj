function getMessages() {
    $.get('/getText', function(data){
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

setInterval(getMessages, 2000);