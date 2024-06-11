# jrnl2tumblr

## Description

`jrnl2tumblr` is a tool that allows you to import journal entries from [jrnl](https://jrnl.sh/) to your Tumblr blog.

## Features
- Imports journal entries from a JSON file exported by jrnl.
- Posts entries to a specified Tumblr blog.
- Ensures privacy and security by requiring OAuth authentication.

## Installation

```bash
$ pip install jrnl2tumblr
```

## Usage
1. Export your journal entries from jrnl to a JSON file:

   ```bash
   jrnl --export json > journal.json
   ```

3. Create a new Tumblr app at [https://www.tumblr.com/oauth/apps](https://www.tumblr.com/oauth/apps) and obtain your OAuth credentials.

4. Run `jrnl2tumblr` and provide the path to the JSON file and your Tumblr blog name.

   ```bash
   jrnl2tumblr journal.json my-tumblr-blog
   ```

5. Follow the prompts to enter your Tumblr OAuth credentials.

6. Your journal entries will be imported and posted to your Tumblr blog.

## Contributing
Contributions are welcome! Please feel free to submit a pull request or open an issue if you encounter any bugs or have suggestions for improvements.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
