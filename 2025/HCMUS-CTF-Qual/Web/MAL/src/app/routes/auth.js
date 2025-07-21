const express = require('express');
const router = express.Router();
const passport = require('passport');
const randomstring = require('randomstring');
const User = require('../models/user');
const myCache = require('../utils/cache');
const { jakanUsers } = require('../utils/jakan')
const { rateLimit } =  require('express-rate-limit')

const limiter = rateLimit({
  windowMs: 60 * 1000, // 15 minutes
  limit: 5, // Limit each IP to 100 requests per `window` (here, per 15 minutes).
  standardHeaders: 'draft-8', // draft-6: `RateLimit-*` headers; draft-7 & draft-8: combined `RateLimit` header
  legacyHeaders: false, // Disable the `X-RateLimit-*` headers.
})

/**
 * Returns the login page
 */

router.get('/login', (req, res) => {
  res.render('auth/login', { error: req.flash('error') });
});

router.post(
  '/login',
  limiter,
  passport.authenticate('local', {
    failureRedirect: '/login',
    failureFlash: true
  }),
  (req, res) => {
    if (req.user.role !== 'super_admin') {
      return res.redirect('/index')
    }
    req.logout();
    return res.redirect('/login');
  }
);

/**
 * Returns the register page
 */

router.get('/register', (req, res) => {
  res.render('auth/register');
});

router.post('/register', limiter, async (req, res) => {
  if (!req.body.username || typeof req.body.username !== 'string') {
    throw new Error('Invalid username');
  }
  if (!req.body.password || typeof req.body.password !== 'string') {
    throw new Error('Invalid password');
  }
  const username = req.body.username.trim();
  let data;
  try {
    data = await jakanUsers.users(username, 'full');
  } catch (err) {
    return res.render('auth/register', {
      error: "This username doesn't exist on MyAnimeList"
    });
  }
  const newUser = new User({
    username: data.data.username,
    role: 'user'
  });
  User.register(newUser, req.body.password, async function (err, user) {
    if (err) {
      return res.render('auth/register', { error: err.message });
    }
    data.data.secret = randomstring.generate(20);
    const userdata = await User.findOneAndUpdate({ username: data.data.username }, { data: data.data }, { new: true });
    if (!myCache.has(`user_${username}`)) {
      myCache.set(`user_${username}`, userdata);
    }
    passport.authenticate('local')(req, res, function () {
      res.redirect('/index');
    });
  });
});

/**
 * Logout route
 */

router.get('/logout', (req, res) => {
  req.logout();
  res.redirect('/index');
});

module.exports = router;
