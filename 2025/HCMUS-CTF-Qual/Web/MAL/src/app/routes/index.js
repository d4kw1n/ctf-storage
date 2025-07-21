const express = require('express');
const router = express.Router();
const myCache = require('../utils/cache')
const { jakanMisc } = require('../utils/jakan')
const getSeason = (d) => Math.floor((d.getMonth() / 12) * 4) % 4;

/**
 * Returns airing, upcoming anime & current season
 */

router.get('/index', async function (req, res) {
  let data1, data2, data3;
  let year = new Date().getFullYear();
  let season_s = ['winter', 'spring', 'summer', 'fall'][getSeason(new Date())];
  let next_year = year + (getSeason(new Date()) + 1 > 3 ? 1 : 0);
  let next_season_s = ['winter', 'spring', 'summer', 'fall'][
    (getSeason(new Date()) + 1) % 4
  ];

  if (
    myCache.has('currentSeason') &&
    myCache.has('topAnimeAiring') &&
    myCache.has('topAnimeUpcoming')
  ) {
    data1 = myCache.get('currentSeason');
    data2 = myCache.get('topAnimeAiring');
    data3 = myCache.get('topAnimeUpcoming');

    return res.render('index', {
      data1,
      data2,
      data3,
      year,
      season_s,
      next_year,
      next_season_s
    });
  } else {
    const [data1, data2, data3] = await Promise.all([
      jakanMisc.season(year, season_s, { limit: 10 }),
      jakanMisc.top('anime', { filter: 'airing', limit: 10 }),
      jakanMisc.top('anime', { filter: 'upcoming', limit: 10 })
    ]);
    myCache.mset([
      { key: 'currentSeason', val: data1 },
      { key: 'topAnimeAiring', val: data2 },
      { key: 'topAnimeUpcoming', val: data3 }
    ]);
    res.render('index', {
      data1,
      data2,
      data3,
      year,
      season_s,
      next_year,
      next_season_s
    });
  }
});

router.get('/500', (req, res) => {
  res.render('500');
});

/**
 * Redirects to the index page
 */

router.get('/', (req, res) => {
  res.redirect('index');
});

module.exports = router;
