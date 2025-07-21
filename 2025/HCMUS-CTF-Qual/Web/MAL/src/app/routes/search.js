const express = require('express');
const router = express.Router();
const { jakanSearch } = require('../utils/jakan')

/**
 * Returns anime of a specified genre
 *
 *  @param queryType type of query anime/manga/person/character
 *  @param query the search query
 */

router.get('/search', async (req, res) => {
  const queryType = req.query.type;
  const query = req.query.search;

  if (queryType === 'anime') {
    const data = await jakanSearch.anime({ q: query });
    return res.render('search/search', {
      data: data.data
    });
  } else if (queryType === 'manga') {
    const data = await jakanSearch.manga({ q: query });
    return res.render('search/search', {
      data: data.data
    });
  } else if (queryType === 'people') {
    const data = await jakanSearch.people({ q: query });
    return res.render('search/search', {
      data: data.data
    });
  } else {
    res.redirect('/');
  }
});

module.exports = router;
