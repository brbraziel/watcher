document.addEventListener('DOMContentLoaded', function(){
    document.querySelector('#tab').addEventListener('click', analyzeTab)
} );

document.addEventListener('DOMContentLoaded', function(){
    document.querySelector('#opendiv').addEventListener('click', specificURL)
} );

document.addEventListener('DOMContentLoaded', function(){
    document.querySelector('#url').addEventListener('click', analyzeURL)
} );

function specificURL() {
    var x = document.getElementById("specURL");
    if (x.style.display === "none") {
      x.style.display = "block";
    } else {
      x.style.display = "none";
    }
}

const postData =  async (url = '', data = {}) => {
    const config = {
        method: 'POST', // *GET, POST, PUT, DELETE, etc.
        // mode: 'cors', // no-cors, *cors, same-origin
        body: JSON.stringify(data), // body data type must match "Content-Type" header,
        headers: new Headers({
            "Content-Type": "body/json",
            'Access-Control-Allow-Origin': '*',
            // "Access-Control-Allow-Headers": "Content-Type"
        })
    }
    const response = await fetch(url, config);

    return response.json(); // parses JSON response into native JavaScript objects
}

async function analyzeTab(){ 
    chrome.tabs.query({currentWindow: true, active: true}, async function (tabs) {
        var tabURL = "" + tabs[0].url;
        const response = await postData("http://127.0.0.1:5000/", { param: tabURL})
        const firstKey = Object.keys(response)[0]
        
        document.getElementById("result").innerHTML = "Este link e " + response[firstKey]
        document.getElementById("link").innerHTML = "" + tabURL
    });
}

async function analyzeURL(){ 
    var url = "" + document.getElementById('linkurl').value
    document.getElementById("link").innerHTML = url

    const response = await postData("http://127.0.0.1:5000/", { param: url})
    const firstKey = Object.keys(response)[0]    

    document.getElementById("result").innerHTML = "Este link e " + response[firstKey]
    document.getElementById("link").innerHTML = "" + tabURL
}