const User = require('../models/user');
const myCache = require('../utils/cache');
const randomstring = require('randomstring');
const { jakanUsers } = require('../utils/jakan');

module.exports = async () => {
  await User.deleteMany({});
  let data;
  const username = 'Dat2Phit'
  try {
    data = await jakanUsers.users(username, 'full');
  } catch (error) {
    data = { data: {} };
  };
  const Dat2Phit = new User({
    username: username,
    role: 'admin'
  });
  const password = randomstring.generate({
    length: 5,
    charset: 'numeric'
  });
  console.log(`Password: ${password}`);
  User.register(Dat2Phit, password, async function (err, user) {
    if (err) {
      throw new Error('Failed to initialize');
    }
    data.data.secret = randomstring.generate(20);
    const userdata = await User.findOneAndUpdate(
      { username: username },
      { data: data.data },
      { new: true }
    );
    if (!myCache.has(`user_${username}`)) {
      myCache.set(`user_${username}`, userdata);
    }
    await User.findOneAndUpdate(
      { username: username },
      { 'data.secret': process.env.FLAG_1 || 'HCMUS-CTF{fake-flag}' }
    );
  });
}
