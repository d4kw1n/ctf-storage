const NodeCache = require('node-cache');

module.exports = new NodeCache({
  stdTTL: parseInt(process.env.CACHE_TTL) || 86400,
  checkperiod: 6000
});
