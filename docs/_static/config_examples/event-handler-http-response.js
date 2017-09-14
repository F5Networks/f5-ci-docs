// A HTTP Response event handler that appends a header to the server response

module.exports = (res, next) => {
  res.headers['x-my-bar'] = 'foo';
  next();
}
