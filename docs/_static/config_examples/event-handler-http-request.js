// A HTTP Request event handler that filters the incoming request on method type.
// It sends back a `503` if requested method is POST else lets the request go through

module.exports = (req, res, next) => {
  if (req.method === 'POST') {
    res.statusCode = 503;
    res.end('POST Method not supported');
  } else { 
    next(); 
  } 
}
