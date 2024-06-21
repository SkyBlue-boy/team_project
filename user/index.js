function submitCode() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const code = document.getElementById('code').value;

    fetch('http://172.17.67.79:8000/submission', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            username: username,
            password: password,
            code: code
        })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('result').innerText = 'Submission ID: ' + data.id;
    })
    .catch(error => console.error('Error:', error));
}

function checkResult() {
    const username = document.getElementById('result-username').value;
    const password = document.getElementById('result-password').value;
    const id = document.getElementById('submission-id').value;

    fetch(`http://172.17.67.79:8000/submission?username=${username}&password=${password}&id=${id}`)
    .then(response => response.json())
    .then(data => {
        document.getElementById('result-output').innerText = 'Status: ' + data.status;
    })
    .catch(error => console.error('Error:', error));
}
