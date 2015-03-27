// http://localhost:8080/

var http = require("http");

http.createServer(function ( req, res ) {
    res.writeHead( 200, { "Content-Type": "text/plain" } );
    res.write( "fechado" );
    // res.write( "aberto" );
    res.end();
}).listen( 8080 );