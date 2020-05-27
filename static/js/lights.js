// this worked!!!!!
// //Create the XHR Object
    // let xhttp = new XMLHttpRequest;
    // //Call the open function, GET-type of request, url, true-asynchronous
    // xhttp.open('GET', '/api/v1/resources/lightstatus?light=5', true)
    // //call the onload 
    // xhttp.onload = function() 
    //     {
    //         //check if the status is 200(means everything is okay)
    //         if (this.status === 200) 
    //             {
    //                 //return server response as an object with JSON.parse
    //                 console.log(JSON.parse(this.responseText));
    //     }
    //             }
    // //call send
    // xhttp.send();
    // //Common Types of HTTP Statuses
    // // 200: OK
    // // 404: ERROR
    // // 403: FORBIDDEN

const lightstatus = (light) => {
    let xhttp = new XMLHttpRequest;
    xhttp.open('GET', '/api/v1/resources/lightstatus?light=' + light, true)
    xhttp.onload = function () {
        if (this.status === 200){
            console.log(JSON.parse(this.responseText));
        }
    }
    xhttp.send();
}
