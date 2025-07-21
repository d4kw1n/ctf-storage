const express = require('express');
const router = express.Router();
const fs = require('fs');
const path = require('path');
const isBinaryPath = require('is-binary-path');
const User = require('../models/user');
const myCache = require('../utils/cache');
const archiveFolder = '/archive';

/**
 * Returns the list of users registered on this site
 */

router.get('/admin/users', isAdmin, async (req, res) => {
  let limit = 24,
    skip = 0,
    sort = 'created_at';
  if (req.query.limit) limit = parseInt(req.query.limit);
  if (req.query.skip) skip = parseInt(req.query.skip);
  if (req.query.sort && typeof req.query.sort === 'string')
    sort = req.query.sort;
  const users = await User.find()
    .skip(skip)
    .limit(limit)
    .sort(sort);
  res.render('admin/users', { users });
});

/**
 * Delete a user on the site
 */

router.get('/admin/users/delete/:username', isAdmin, async (req, res) => {
  const username = req.params.username;
  if (username === req.user.username) {
    throw new Error('Can\'t delete yourself');
  }
  await User.findOneAndDelete({ username: username })
  res.redirect('/admin/users');
});

/**
 * Returns the list cached data
 */

router.get('/admin/cache', isAdmin, async (req, res) => {
  const keys = myCache.keys();
  const caches = Object.assign(
    ...keys.map((key) => ({ [key]: JSON.stringify(myCache.get(key)).substring(0, 100) }))
  );
  res.render('admin/cache', { caches });
});


function fileSize(b) {
  var u = 0,
    s = 1024;
  while (b >= s || -b >= s) {
    b /= s;
    u++;
  }
  return (u ? b.toFixed(1) + ' ' : b) + ' KMGTPEZY'[u] + 'B';
}

/**
 * View the archive
 */

router.get('/admin/archive', isAdmin, async (req, res) => {
  const files = {}
  fs.readdirSync(archiveFolder).forEach((file) => {
    const stat = fs.statSync(path.join(archiveFolder, file));
    const size = fileSize(stat.size);
    const mtime = stat.mtime.toLocaleDateString();
    files[file] = { size, mtime }
  });
  res.render('admin/archive', { files });
});


/**
 * View the file in archive
 */

router.get('/admin/archive/:filename', isAdmin, async (req, res) => {
  const filename = req.params.filename;
  const file_path = x.join(archiveFolder, filename);
  if (
    file_path.includes('app') ||
    file_path.includes('proc') ||
    file_path.includes('environ') ||
    isBinaryPath(file_path)
  ) {
    throw new Error('Invalid path');
  }
  const content = fs.readFileSync(file_path, 'utf-8');
  if (content.includes('HCMUS-CTF')) {
    throw new Error('Sensitive information');
  }
  res.render('admin/archivefile', { content });
});

/**
 * Update the file in archive
 */
function isAscii(str) {
  for (let i = 0; i < str.length; i++) {
    if (str.charCodeAt(i) > 127) {
      return false;
    }
  }
  return true;
}

router.post('/admin/archive/:filename', isAdmin, async (req, res) => {
  const filename = req.params.filename;
  const content = req.body.content;
  const file_path = path.join(archiveFolder, filename);
  if (
    file_path.includes('app') ||
    file_path.includes('proc') ||
    file_path.includes('environ') ||
    isBinaryPath(file_path)
  ) {
    throw new Error('Invalid path');
  }
  if (!isAscii(content)) {
    throw new Error('Content must be ASCII');
  }
  fs.writeFileSync(file_path, content);
  res.redirect(`/admin/archive/${filename}`);
});

/**
 * Returns the flag if requested from localhost
 */

router.get('/admin/flag', async (req, res) => {
  console.log('Flag requested from:', req.socket.remoteAddress);
  if (req.socket.remoteAddress === '127.0.0.1') {
    res.json({ data: { flag: process.env.FLAG_2 || 'HCMUS-CTF{fakeflag}' } });
    return;
  }
  res.json({ data: { flag: {} } });
});

/**
 * Returns the flag if requested by super admin
 */

router.get('/super_admin/flag', isSuperAdmin, async (req, res) => {
  res.json({ data: { flag: process.env.FLAG_3 || 'HCMUS-CTF{fakeflag}' } });
});

function isAdmin(req, res, next) {
  if (req.isAuthenticated() && (req.user.role === 'admin' || req.user.role === 'super_admin')) {
    return next();
  }
  return res.redirect('/login');
}

function isSuperAdmin(req, res, next) {
  if (req.isAuthenticated() && req.user.role === 'super_admin') {
    return next();
  }
  return res.redirect('/login');
}

module.exports = router;
