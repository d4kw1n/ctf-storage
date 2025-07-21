const express = require('express');
require('express-async-errors');
const app = express(),
  bodyParser = require('body-parser'),
  mongoose = require('mongoose'),
  flash = require('connect-flash'),
  passport = require('passport'),
  LocalStrategy = require('passport-local'),
  bbobHTML = require('@bbob/html'),
  presetHTML5 = require('@bbob/preset-html5'),
  DOMPurify = require("isomorphic-dompurify"),
  User = require('./models/user'),
  init = require('./utils/init')
  methodOverride = require('method-override'),
  dotenv = require('dotenv');
dotenv.config();

const seasonRoutes = require('./routes/season');
const userRoutes = require('./routes/user');
const genreRoutes = require('./routes/genre');
const searchRoutes = require('./routes/search');
const authRoutes = require('./routes/auth');
const indexRoutes = require('./routes/index');
const animeAndMangaRoutes = require('./routes/animeAndManga');
const adminRoutes = require('./routes/admin');

app.use(bodyParser.urlencoded({ extended: true }));
app.set('view engine', 'ejs');
app.use(express.static(__dirname + '/public'));
app.use(methodOverride('_method'));
app.use(flash());
app.use(
  require('cookie-session')({
    secret: process.env.SECRET_KEY || 'lmaolmao',
  })
);

app.use(passport.initialize());
app.use(passport.session());
passport.use(new LocalStrategy(User.authenticate()));
passport.serializeUser(User.serializeUser());
passport.deserializeUser(User.deserializeUser());
app.use((req, res, next) => {
  res.locals.bbobHTML = bbobHTML;
  res.locals.presetHTML5 = presetHTML5;
  res.locals.DOMPurify = DOMPurify;
  res.locals.currentUser = req.user;
  next();
});
app.use(indexRoutes);
app.use(animeAndMangaRoutes);
app.use(searchRoutes);
app.use(seasonRoutes);
app.use(genreRoutes);
app.use(authRoutes);
app.use(userRoutes);
app.use(adminRoutes);

app.use((err, req, res, next) => {
  // if (err?.response?.data) console.error(err?.response?.data);
  // else console.error(err);
  res.render('500', { message: err?.message });
});

const PORT = process.env.PORT || 80;

mongoose.connection.on('error', (err) => {
  console.log(err);
});

mongoose.connection.on('connecting', () => {
  console.log('Connecting to DB...');
});

mongoose.connection.once('open', async () => {
  console.log('Connected to DB');
  await init();
  console.log('Initialized');
  app.listen(PORT, '0.0.0.0' , () => console.log(`Server started on port ${PORT}`));
});

mongoose.connect(String(process.env.MONGO_URI || 'mongodb://localhost:27017/MAL'), {
  useNewUrlParser: true,
  useUnifiedTopology: true
});
