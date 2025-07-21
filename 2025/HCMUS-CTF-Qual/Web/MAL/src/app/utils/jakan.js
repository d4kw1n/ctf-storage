const { Jakan } = require('jakan');

const jakanSearch = new Jakan()
  .withMemory(parseInt(process.env.CACHE_TTL) * 1000 || 86400000)
  .forSearch();
const jakanUsers = new Jakan()
  .withMemory(parseInt(process.env.CACHE_TTL) * 1000 || 86400000)
  .forUsers();
const jakanMisc = new Jakan()
  .withMemory(parseInt(process.env.CACHE_TTL) * 1000 || 86400000)
  .forMisc();

module.exports = {
  jakanSearch,
  jakanUsers,
  jakanMisc
};