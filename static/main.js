document.getElementById('form').onsubmit = function(e) {
    e.preventDefault();
    fetch('/todos/create', {
        method: 'POST',
        body: JSON.stringify({
            'description': document.getElementById('description').value
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(function(response) {
        return response.json();
    })
    .then(function(jsonResponse) {
        console.log('response', jsonResponse);
        var liItem = document.createElement('li');
        liItem.innerHTML = jsonResponse['description'];
        document.getElementById('todos').appendChild(liItem);
        document.getElementById('error').className = 'hidden';
    })
    .then(function() {
        document.getElementById('description').value='';
    })
    .catch(function(error) {
        console.log("Error: " + error);
        document.getElementById('error').className = '';
    })
}