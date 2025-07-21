const crypto = require("crypto");

const salt = "fad7b27ddb4ca4ed85868470abddd212";
const target_hash =
    "88e4dda36f803a18e4435f0e9097636d55f934e1f39e7fd34366f27c6017ba8c";

for (let i = 0; i <= 99999; i++) {
    const password = i.toString().padStart(5, "0");
    const hash = crypto
        .pbkdf2Sync(password, salt, 25000, 32, "sha256")
        .toString("hex");
    if (hash === target_hash) {
        console.log("Found password:", password);
        process.exit(0);
    }
    if (i % 1000 === 0) {
        console.log("Tried:", password);
    }
}
console.log("Password not found");
