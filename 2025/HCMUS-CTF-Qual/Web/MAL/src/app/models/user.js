var mongoose = require("mongoose");
var passportLocalMongoose = require("passport-local-mongoose");

var UserSchema = new mongoose.Schema(
  {
    username: {
      type: String,
      unique: true
    },
    password: String,
    role: {
      type: String,
      enum: ['user', 'admin', 'super_admin']
    },
    data: Object
  },
  { timestamps: { createdAt: 'created_at', updatedAt: 'updated_at' } }
);

UserSchema.plugin(passportLocalMongoose, {
  saltlen: 16,
  keylen: 32,
  usernameCaseInsensitive: true
});

module.exports = mongoose.model("User", UserSchema);