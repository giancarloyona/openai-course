# OpenAI course and projects

Repo for storing notebooks and/or scripts based on Colt Steele's [course](https://www.udemy.com/course/mastering-openai/).

## How to run the notebooks and scripts?

To run these files, first, you need to install the packages listed in the requirements.txt file.

Also, you should already have an OpenAI account to generate API keys and use them here. To use your key, store it inside a `.env` file in the following format:

```
OPENAI_API_KEY=<your_api_key>
```

The `python-dotenv` package will read the file, and then you should be able to use the key.

For the playlist script, you must resgister as a Spotify Developer account and must provide your client_id and secret - store it in the `.env` file in the following format:

```
SPOTIFY_CLIENT_ID=<your_client_id>
SPOTIFY_CLIENT_SECRET=<your_client_secret>
```