# Thundermail Python SDK
A Python package for the Thunder Mail API.

## Install

```bash
pip install thundermail
```

## Setup

First, you need to get an API key, which is available in the [Thunder Mail Dashboard](https://thundermail.vercel.app/dashboard).

```python
 from thundermail import ThunderMail;
thundermail = Thundermail('tim_12345678');
```

## Usage

Send your first email:

```python
response = thundermail.send(
    from_email = 'you@example.com',
    to = 'user@google.com',
    subject = 'hello world',
    html = '<strong>it works!</strong>'
)
```


## License

MIT License
