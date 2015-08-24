# PB4Py

A python API for Interface with PushBullet

## Installation

You can use pip or easy_install to install PB4Py. Alternatively you could check
out the repo and then use it directly like that but that's only recommended if
you are doing development on the project.

## Configuration

You can use the following options to configure PB4Py.

### auth

#### type

There are two types of authentication that are provided with PB4Py: `basic` and
`oauth`.

##### basic

The first and easiest is `basic`. Basic authentication uses a `access_token` that
you can find on your PushBullet profile page. This is unique to each PushBullet
user and should be kept secret. If you are working on behalf of another user or
you are working in an environment where you can't use a personal `access_token`
consider using the `oauth` authenticator.

###### Usage

	{
		"auth": {
			"type": "basic",
			"auth_token": <auth-token>
		}
	}

##### oauth

The second type is `oauth`. OAuth is great when you are working on behalf of
a different person or you are working in a setting where you don't want your
personal `access_token` visible to users of the software. For this method of
authentication you set the `access_token` setting to be the OAuth token that
is generated for you. You'll need to have the user approve the application
first.

###### Usage

	{
		"auth": {
			"type": "oauth",
			"auth_token": <oauth-token>,
			"client_id": <client-id>,
			"client_secret": <client_secret>,
			"request_uri": <request_uri>
		}
	}

