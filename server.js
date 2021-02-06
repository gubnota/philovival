const http = require('http'); // 1 - Import Node.js core module
const fs = require('fs');
function getfile(req, res){
    if (typeof(res)=='undefined'){
        name = 'index.html';
    }
    else {
        name = req.url.substr(1);
    }
    if(name.substr(name.length-2)=='/' || name=='') name = name+'index.html';
    try {
        
    if(fs.existsSync(name)) {
        res.writeHead(200, {"Content-Type" : "text/html; charset=utf-8"});
        res.write(getfile('index.html'));
        res.end();
        return fs.readFileSync(name);
        // console.log("The file exists.");
    } else {
        console.log('The file does not exist.');
        return 'The file does not exist.';
    }

} catch (err) {
    console.error(err);
}
}

const server = http.createServer(function (req, res) {   // 2 - creating server
    // getfile(req, res);
    if (typeof(res)=='undefined'){
        name = 'index.html';
    }
    else {
        name = req.url.substr(1);
    }
    if(name.substr(name.length-2)=='/' || name=='') name = name+'index.html';
    try {
    if(fs.existsSync(name)) {
        ext = name.substr(name.lastIndexOf('.')+1).toLowerCase();
        switch (ext) {
            case 'html':
            res.writeHead(200, {"Content-Type" : "text/html; charset=utf-8"});
            break;
            case 'css':
            res.writeHead(200, {"Content-Type" : "text/css; charset=utf-8"});
            break;
            case 'js':
            res.writeHead(200, {"Content-Type" : "application/javascript; charset=utf-8"});
            break;
            case 'json':
            res.writeHead(200, {"Content-Type" : "application/json; charset=utf-8"});
            break;
            case 'mp4':
            res.writeHead(200, {"Content-Type" : "video/mp4; charset=utf-8"});
            break;
            case 'png':
            res.writeHead(200, {"Content-Type" : "image/png; charset=utf-8"});
            break;
            case 'webp':
            res.writeHead(200, {"Content-Type" : "image/webp; charset=utf-8"});
            break;
            case 'jpeg':
            res.writeHead(200, {"Content-Type" : "image/jpeg; charset=utf-8"});
            break;
            case 'jpg':
            res.writeHead(200, {"Content-Type" : "image/jpeg; charset=utf-8"});
            break;
            case 'gif':
            res.writeHead(200, {"Content-Type" : "image/gif; charset=utf-8"});
            break;
            case 'mp3':
            res.writeHead(200, {"Content-Type" : "audio/mp3; charset=utf-8"});
            break;
            case 'm4a':
            res.writeHead(200, {"Content-Type" : "audio/m4a; charset=utf-8"});
            break;
            case 'ico':
            res.writeHead(200, {"Content-Type" : "image/x-icon; charset=utf-8"});
            break;
            case 'svg':
            res.writeHead(200, {"Content-Type" : "image/svg+xml; charset=utf-8"});
            break;
            default:
            res.writeHead(200, {"Content-Type" : "text/plain; charset=utf-8"});
            break;
        }
        res.write(fs.readFileSync(name));
        res.end();
        console.log([name,"The file exists."]);
    } else {
        console.log([name,'The file does not exist.']);
    }

} catch (err) {
    console.error(err);
}

});
server.listen(80); //3 - listen for any incoming requests
console.log('Node.js web server at port 80 is running..')