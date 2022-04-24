import express from "express";
import quotes from "./quotes.mjs";

const app = express();

function getRandomInt(max) {
  return Math.floor(Math.random() * max);
}

app.use(express.json());

const port = process.env.PORT || 3000;

app.use(express.json());

app.listen(port, () => console.log(`Server is listening on port ${port}`));

app.get("/quotes", (req, res) => {
  let random = getRandomInt(quotes.length);
  res.send(quotes[random]);
  console.log(`Somebody got the image with id ${random + 1}`);
});
