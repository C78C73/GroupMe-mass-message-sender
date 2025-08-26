# GroupMe mass message sender

Send a message (with an image) to multiple GroupMe groups by using GroupMe bots.

Important: GroupMe bots can only post to the single group they were created for. To post to multiple groups, you must create one bot per group.

## What you need

- A GroupMe account
- GroupMe access token (used to list groups and upload images)
- One bot per target group (each bot has its own bot_id)

## 1) Get your GroupMe access token

1. Go to https://dev.groupme.com/session/new and sign in.
2. Copy the “Access Token”. You’ll use it in Postman and/or to upload images.

## 2) Find your Group (optional) and Bot IDs (required)

You only need the bot IDs to send messages via the bot API, but here’s how to find both.

- Group IDs (optional, for reference):
  1. In Postman, create a GET request to:
	  - `https://api.groupme.com/v3/groups?token=YOUR_ACCESS_TOKEN`
  2. Send the request. You’ll get a JSON response. Each `group` object contains an `id`.

- Bot IDs (required):
  1. Go to https://dev.groupme.com/bots
  2. Click “Create Bot”.
  3. Choose the group the bot will live in (DO NOT check the direct-messages box if you want group posts).
  4. Give it a name; leave Callback URL empty unless you need webhooks.
  5. Submit and copy the bot’s `bot_id`.
  6. Repeat for each group you want to send to. You’ll end up with one `bot_id` per group.

## 3) Upload your image to GroupMe using Postman

GroupMe messages require images to be hosted by GroupMe (i.groupme.com). Upload first to get a `picture_url`.

1. In Postman, create a POST request to: `https://image.groupme.com/pictures`
2. Headers:
	- `X-Access-Token: YOUR_ACCESS_TOKEN`
3. Body:
	- Choose `form-data`
	- Add a key named `file` and change its type to `File`
	- Choose your local image file
4. Send the request. The JSON response includes:
	```json
	{
	  "payload": {
		 "picture_url": "https://i.groupme.com/..."
	  }
	}
	```
5. Copy the `picture_url` (must start with `https://i.groupme.com/`).

## 4) Send a message with the image

You can test directly from Postman, or run the included Python script.

### A) Postman (quick test)

1. Create a POST request to: `https://api.groupme.com/v3/bots/post`
2. Body: Raw, JSON (application/json):
	```json
	{
	  "bot_id": "YOUR_BOT_ID",
	  "text": "Here is an image!",
	  "attachments": [
		 { "type": "image", "url": "https://i.groupme.com/..." }
	  ]
	}
	```
3. Send. A 202 Accepted means GroupMe queued the message successfully.

Repeat for each bot (each target group).

### B) Python script (this repo)

1. Install Python 3.10+ and the `requests` package:
	```powershell
	pip install requests
	```
2. Open `sender.py` and set:
	- The list of bot IDs you want to post to (one per group)
	- The `MESSAGE_TEXT`
	- The `IMAGE_URL` (the `picture_url` you copied from Postman)
3. Run the script:
	```powershell
	python .\sender.py
	```

Notes:
- The script uses the GroupMe Bot API endpoint `https://api.groupme.com/v3/bots/post`.
- Status code 202 means success (message accepted).
- A 500 error usually means a bad payload (e.g., wrong endpoint, missing `bot_id`, or image URL not from `i.groupme.com`).

## Common pitfalls

- Trying to post an image with a non-GroupMe URL. Always upload first and use the returned `picture_url` from `i.groupme.com`.
- Using the user messages endpoint (`/v3/messages`) instead of the bot endpoint (`/v3/bots/post`). Image attachments are for bots.
- Creating the bot with the “direct messages” option checked. Leave it unchecked for group posts.
- Reusing one bot across multiple groups. You must create one bot per group.

