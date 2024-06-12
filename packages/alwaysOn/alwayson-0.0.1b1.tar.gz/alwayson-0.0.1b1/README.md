# alwaysOn

<p align="center">
  <img src="https://raw.githubusercontent.com/balestek/hashtray/master/media/alwaysOn-logo.png">
</p>

## Intro

_alwaysOn_ is an email checker for Onoff.app.

It grabs a token from Onoff.app used to retrieve the information about the email. The token is valid several hours.

If it can't get the token, it opens a browser to manually solve the captcha.

## Installation

### Using pipx

```bash
pipx install alwaysOn
alwaysOn install
```

`alwaysOn install` installs the required browser in the alwaysOn pipx virtual environment.

### Using pip

```bash
pip install alwaysOn
playwright install firefox
```

## Usage

```bash
alwaysOn email@example.com
```

## Requirements

```
httpx
python-dotenv
playwright-stealth
playwright
rich
```

## License

GPLv3
