# Piolin

Piolin is a Twitter-like toy REST API developed using Flask.
It was developed as an example project as part of teaching the "Massive Data Extraction from the Internet" subject in Universidad de Huelva (MSc in Computer Science, 2023).

It contains three endpoints:
* `/users`
* `/tweets`
* `/messaging`
* `/messages`
* `/messages-stream`

The code should be fairly self-explanatory as to what each endpoint expects and returns.

## Note
It was developed as quick-and-dirty teaching resource, hence it doesn't follow proper REST ettiquete (such as HATEOAS, resource nesting, consistent use of path params vs query params, etc.).

HTTPS is achieved by on-the-fly certificates, authentication is based on a hardcoded string, passwords are encrypted in the clear (though they are useless anyway...).
