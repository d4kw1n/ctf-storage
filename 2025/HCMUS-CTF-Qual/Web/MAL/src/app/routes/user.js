const express = require('express');
const cheerio = require('cheerio');
const router = express.Router();
const User = require('../models/user');
const myCache = require('../utils/cache');
const fs = require('fs');
const path = require('path')
const sharp = require('sharp');
const imgToPDF = require('image-to-pdf');
const { v4: uuidv4 } = require('uuid');
const util = require('util');
const execFile = util.promisify(require('child_process').execFile);
const { jakanUsers } = require('../utils/jakan')
const exportsFilePath = path.join(__dirname + '/../exports');

/**
 * Returns the list of users registered on this site
 */

router.get('/users', async (req, res) => {
  let limit = 24, skip = 0, sort = 'created_at';
  if (req.query.limit) limit = parseInt(req.query.limit);
  if (req.query.skip) skip = parseInt(req.query.skip);
  if (req.query.sort && typeof req.query.sort === 'string') sort = req.query.sort;
  const users = await User.find()
    .skip(skip)
    .limit(limit)
    .sort(sort)
    .select('data');
  res.render('community/users', { users });
});

/**
 * Returns the MAL profile of the current user
 *
 *  @param username the myanimelist username of the current user
 */

router.get('/user/:username/profile', async (req, res) => {
  const username = req.params.username;
  if (myCache.has(`user_${username}`)) {
    const user = myCache.get(`user_${username}`);
    res.render('user/userprofile', { data: user.data });
  } else {
    try {
      const existed_user = await jakanUsers.users(username, 'full');
      const user = await User.findByUsername(existed_user.data.username);
      if (!user) {
        throw new Error("No user exist")
      } 
      myCache.set(`user_${username}`, user);
      res.render('user/userprofile', { data: user.data });
    } catch (error) {
      throw new Error(error.message);
    } 
  }
});

/**
 * Export the current user favorite anime to a file
 *
 *  @param username the myanimelist username of the current user
 */

router.get('/user/:username/export', isLoggedIn, async (req, res) => {
  const username = req.params.username;
  const baseURL = `http://localhost:${process.env.PORT}`;
  const data = await execFile('curl', [`${baseURL}/user/${username}/profile`]);
  console.log(data);
  const $ = cheerio.load(data.stdout);
  const imgs = $('img:not(.user-avatar)')
  console.log(`Found ${imgs.length} images`);
  console.log(imgs);
  const imgs_src = []
  imgs.each(function (idx, img) {
    imgs_src.push($(img).attr('src'))
  });
  console.log("Image sources:", imgs_src);
  const promises = imgs_src.map((src) =>
    execFile('curl', [src], { encoding: 'buffer', maxBuffer: 5 * 1024 * 1024 })
  );
  const results = await Promise.all(promises)
  const img_buffers = await Promise.all(
    results.map(async (res) => {
      const img = await sharp(res.stdout).toFormat('png').toBuffer();
      return img
    }
  ));
  const outFile = `${exportsFilePath}/${uuidv4()}.pdf`;
  const pdfBuffers = await imgToPDF(img_buffers, imgToPDF.sizes.A5).toArray()
  fs.writeFileSync(outFile, Buffer.concat(pdfBuffers));
  res.download(outFile, `${username}.pdf`, function (err) {
    if (err) {
      console.log(err);
    }
    fs.unlinkSync(outFile);
  });
});

/**
 * Returns the edit profile page of the current user
 *
 *  @param username the myanimelist username of the current user
 */

router.get('/user/:username/edit', isLoggedIn, async (req, res) => {
  const username = req.params.username;
  if (myCache.has(`user_${username}`)) {
    const user = myCache.get(`user_${username}`);
    if (user.data.username !== req.user.username) {
      throw new Error('No IDOR for u');
    }
    res.render('user/edituser', { data: user.data });
  } else {
    try {
      const existed_user = await jakanUsers.users(username, 'full');
      const user = await User.findByUsername(existed_user.data.username);
      if (!user) {
        throw new Error('No user exist');
      } 
      if (user.data.username !== req.user.username) {
        throw new Error('No IDOR for u');
      }
      myCache.set(`user_${username}`, user);
      res.render('user/edituser', { data: user.data });
    } catch (error) {
      throw new Error(error.message);
    }
  }
});

/**
 * Update the information of the current user
 *
 *  @param username the username of the current user
 */

router.post('/user/:username/edit', isLoggedIn, async (req, res) => {
  const username = req.params.username;
  let user;
  if (myCache.has(`user_${username}`)) {
    user = myCache.get(`user_${username}`);
    if (user.data.username !== req.user.username) {
      throw new Error('No IDOR for u');
    }
  } else {
    const existed_user = await jakanUsers.users(username, 'full');
    user = await User.findByUsername(existed_user.data.username);
    if (!user) {
      throw new Error('No user exist');
    }
    if (user.data.username !== req.user.username) {
      throw new Error('No IDOR for u');
    }
    myCache.set(`user_${username}`, user);
  }
  const userSecret = req.body.secret;
  delete req.body.secret;
  const s = JSON.stringify(req.body).toLowerCase();
  if (s.includes('secret') || s.includes('username') || s.includes('role')) {
    throw new Error("Can't change those fields");
  }
  await User.findOneAndUpdate({ username: user.data.username, 'data.secret': userSecret }, req.body);
  res.sendStatus(204);
});

function isLoggedIn(req, res, next) {
  if (req.isAuthenticated()) {
    return next();
  }
  res.redirect('/login');
}

module.exports = router;
