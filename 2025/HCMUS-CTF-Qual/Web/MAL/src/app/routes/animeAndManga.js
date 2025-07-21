const express = require('express');
const router = express.Router();
const normalizeUrl = require('normalize-url');
const myCache = require('../utils/cache');
const { jakanSearch, jakanMisc } = require('../utils/jakan');

/**
 * Returns top anime of all time
 *
 *  @param page page number
 */

router.get('/top/anime/:page', async (req, res) => {
  const limit = 24;
  const page = req.params.page;
  let data;
  if (myCache.has(`topAnime${page}`)) {
    data = myCache.get(`topAnime${page}`);
  } else {
    data = await jakanMisc.top('anime', { limit, page });
    myCache.set(`topAnime${page}`, data);
  }
  res.render('anime/topanime', {
    data: data.data,
    page,
    limit,
    last_visible_page: data.pagination.last_visible_page
  });
});

/**
 * Redirects to page 1 of top anime
 */

router.get('/top/anime/', (req, res) => {
  res.redirect('/top/anime/1');
});

/**
 * Returns top manga of all time
 *
 *  @param page page number
 */

router.get('/top/manga/:page', async (req, res) => {
  const limit = 24;
  const page = req.params.page;
  let data;
  if (myCache.has(`topManga${page}`)) {
    data = myCache.get(`topManga${page}`);
  } else {
    data = await jakanMisc.top('manga', { limit, page });
    myCache.set(`topManga${page}`, data);
  }
  res.render('manga/topmanga', {
    data: data.data,
    page,
    limit,
    last_visible_page: data.pagination.last_visible_page
  });
});

/**
 * Redirects to page 1 of top manga
 */

router.get('/top/manga/', (req, res) => {
  res.redirect('/top/manga/1');
});

/**
 * Returns details of a anime
 *
 *  @param mal_id id of the anime
 */

router.get('/anime/:mal_id', async (req, res) => {
  const mal_id = req.params.mal_id;
  const data = await jakanSearch.anime(parseInt(mal_id), 'full');
  res.render('anime/animedata', {
    data: data.data
  });
});

/**
 * Returns details of a manga
 *
 *  @param mal_id id of the manga
 */

router.get('/manga/:mal_id', async (req, res) => {
  const mal_id = req.params.mal_id;
  const data = await jakanSearch.manga(parseInt(mal_id), 'full');
  res.render('manga/mangadata', {
    data: data.data
  });
});

/**
 * Returns details of a person
 *
 *  @param mal_id id of the person
 */

router.get('/person/:mal_id', async (req, res) => {
  const mal_id = req.params.mal_id;
  const data = await jakanSearch.people(parseInt(mal_id), 'full');
  res.render('person/persondata', {
    data: data.data
  });
});

/**
 * Redirects to page 1 of schedule
 */

router.get('/schedule', (req, res) => {
  res.redirect('/schedule/1');
});

/**
 * Returns anime weekly schedule
 */

router.get('/schedule/:page', async (req, res) => {
  let weekday = [
    'sunday',
    'monday',
    'tuesday',
    'wednesday',
    'thursday',
    'friday',
    'saturday'
  ][new Date().getDay()];
  const page = req.params.page;
  let data;
  if (myCache.has(`schedule_${weekday}_${page}`)) {
    data = myCache.get(`schedule_${weekday}_${page}`);
  } else {
    data = await jakanMisc.schedules({ filter: weekday, page });
    myCache.set(`schedule_${weekday}_${page}`, data);
  }

  res.render('anime/schedule', {
    data: data.data,
    weekday,
    page,
    last_visible_page: data.pagination.last_visible_page
  });
});

/**
 * Returns recommendations for a anime
 *
 *  @param mal_id id of the anime
 */

router.get('/anime/:mal_id/recommendations', async (req, res) => {
  const mal_id = req.params.mal_id;
  let data;
  if (myCache.has(`anime_${mal_id}_recommendations`)) {
    data = myCache.get(`anime_${mal_id}_recommendations`);
  } else {
    data = await jakanSearch.anime(parseInt(mal_id), 'recommendations');
    myCache.set(`anime_${mal_id}_recommendations`, data);
  }
  res.render('anime/animerecommendations', {
    data: data.data
  });
});

/**
 * Returns recommendations for a manga
 *
 *  @param mal_id id of the manga
 */

router.get('/manga/:mal_id/recommendations', async (req, res) => {
  const mal_id = req.params.mal_id;
  let data;
  if (myCache.has(`manga_${mal_id}_recommendations`)) {
    data = myCache.get(`manga_${mal_id}_recommendations`);
  } else {
    data = await jakanSearch.manga(parseInt(mal_id), 'recommendations');
    myCache.set(`manga_${mal_id}_recommendations`, data);
  }
  res.render('manga/mangarecommendations', {
    data: data.data
  });
});

/**
 * Returns details of a studio/producer
 *
 *  @param producerId id of the studio/producer
 */

router.get('/studio/:producerId', async (req, res) => {
  const mal_id = req.params.producerId;
  let data;
  if (myCache.has(`studio_${mal_id}`)) {
    data = myCache.get(`studio_${mal_id}`);
  } else {
    // The libray hasn't implemented a wrapper for producers
    const request = jakanMisc.infoRequestBuilder(
      'http://api.jikan.moe/v4/producers',
      mal_id,
      'full'
    );
    data = await jakanMisc.makeRequest(normalizeUrl(request));
    myCache.set(`studio_${mal_id}`, data);
  }
  res.render('producer/studio', {
    data: data.data
  });
});

/**
 * Returns episodes of an anime
 *
 *  @param mal_id if of the anime
 *  @param page page number
 */

router.get('/anime/:mal_id/episodes', async (req, res) => {
  const mal_id = req.params.mal_id;
  let data;
  if (myCache.has(`anime_${mal_id}_episodes`)) {
    data = myCache.get(`anime_${mal_id}_episodes`);
  } else {
    data = await jakanSearch.anime(parseInt(mal_id), 'episodes');
    myCache.set(`anime_${mal_id}_episodes`, data);
  }
  res.render('anime/episodes', {
    data: data.data,
    mal_id: mal_id
  });
});

module.exports = router;
