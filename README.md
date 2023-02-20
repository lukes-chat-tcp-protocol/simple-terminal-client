# Simple Terminal Client
Very basic client, does not do much else other than sending and recieving from the server.
* To pass payload to the server, surrounding the cleartext payload with <> automatically encodes it with base64. (ex. LOGIN \<luke> \<some secure password>)
* For FROM modes, the client will decode the payload and surround it in <>. (ex. RECV \<luke> \<Hello, World!>)
