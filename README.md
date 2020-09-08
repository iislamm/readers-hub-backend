# Readers Hub Backend

This API is intended to serve the clients of Readers Hub application.

## Authentication

### `POST /auth/signup`

- Adds a new user
- **Request** arguments: None
- Authorization: Not required
- Request body:

```json
{
	"name": "String: User's display name",
	"email": "String: User's email",
	"password": "String: User's password",

}
```

- Response body:

```json
{
	"user": {
		"uid": "Integer: User's unique id",
		"email": "String: User's email",
		"name": "String: User's name"
	},
	"access_token": "JWT token"
}
```

### `POST /auth/signup`

- Authenticate the user
- Request arguments: None
- Authorization: Not required
- Request body:

```json
{
	"email": "String: User's email",
	"password": "User's password"
}
```

- Response body:

```json
{
	"access_token": "String: JWT Token"
}
```

## Books

### `GET /books/search`

- Gets books matching search query
- Request arguments: `q=search_query`
- Authorization: Not required
- Response body:

```json
{
	"books": "Array of books"
}
```

### `GET /books/<book_id>`

- Gets a specific book
- Request arguments: None
- Request parameters: `book_id: The unique identifier of the book`
- Authorization: Not required
- Response body:

```json
{
	"book": {/* book data */}
}
```

### `PUT /books/<book_id>/progress`

- Updates the reading progress of the reader for this book
- Request arguments: None
- Request parameters: `book_id: The unique identifier for the book`
- Authorization: Required
- Request body:

```json
{
	"progress": "Integer: The percentage of the reading progress"
}
```

- Response body:

```json
{
	"book_id": "Integer: The id of the book",
	"uid": "Integer: The unique identifier of the user"
	"progress": "Integer: The new progress after modification"
}
```

### `POST /books/<book_id>/reviews`

- Adds a review to the book
- Request arguments: None
- Request parameters: `book_id: The unique identifier for the book`
- Authorization: Required
- Request body:

```json
{
	"rating": "Integer: Rating on the scale from 1 to 5",
	"comment": "String: Review comment"
}
```

- Response body:

```json
{
	"book_id": "Integer: Book id",
	"uid": "Integer: The unique identifier of the user",
	"review": {
		"rating": "The new rating",
		"comment": "The new review comment"
	}
}
```

## Lists

### `GET /users/<int:user_id>/lists`

- Gets all the lists of a user
- Request arguments: None
- Request parameters: `user_id=the unique id of the user`
- Authorization: Optional
- Response body:

```json
{
	"lists": "Array of lists",
	"uid": "User id"
}
```

### `POST /lists`

- Creates a new list
- Request arguments: None
- Authorization: Required
- Request body:

```json
{
	"name": "String: The name of the list"
}
```

- Response body:

```json
{
	"list": {
		"id": "Integer: the id of the list",
		"name": "The name of list",
		"owner_id": "Integer: the unique id of the user owning the list",
		"list_type": "String: The type of the list"
	}
}
```

### `PATCH /lists/<list_id>`

- Updates the info of a list
- Request arguments: None
- Request parameters: `list_id: the unique id of the list`
- Authorization: Required
- Request body:

```json
{
	"list": {/* The object contains new data */}
}
```

- Response body:

```json
{
	"list": {/* List data after modification */}
}
```

### `DELETE /lists/<list_id>`

- Deletes a list
- Request arguments: None
- Request parameters: `list_id: the unique id of the list`
- Authorization: Required
- Response body:

```json
{
	"list_id": "Integer: The id of the deleted list"
}
```

### `GET /lists/<list_id>/books`

- Gets all the books of a list
- Request arguments: None
- Request parameters: `list_id: The unique identifier of the list`
- Authorization: Required
- Response body:

```json
{
	"list_id": "Integer: The unique id of the list",
	"books": "Array: The books in the list"
}
```

### `POST /lists/<list_id>/books`

- Adds a book to a list
- Request arguments: None
- Request parameters: `list_id: The unique identifier of the list`
- Authorization: Required
- Response body:

```json
{
	"list_id": "Integer: The unique identefier of the list",
	"book_id": "Integer: The id of the added book"
}
```

## Challenges

### `GET /user/<int:user_id>/challenges`

- Get the challenges of the user
- Request arguments: None
- Request parameters: `user_id: The unique of the user`
- Authorization: Required
- Response body:

```json
{
	"challenges": "Array of the challenges of the user"
}
```

### `POST /challenges`

- Creates a new challenge
- Request arguments: None
- Request parameters: None
- Authorization: Required
- Request body:

```json
{
	"name": "String: The name of the challenge",
	"start_time": "DateTime: The start time of the challenge",
	"end_time": "DateTime: The time the challenge ends",
	"target_books": "Integer: The target of the books read the participants have to reach",
	"type": "Enum('public', 'private')"
}
```

- Response body:

```json
{
	"challenge": {
		"id": "Integer: The unique id of the challenge",
		"creator_id": "Integer: The unique id of the user created it".
		"name": "String: The name of the challenge",
		"start_time": "DateTime: The start time of the challenge",
		"end_time": "DateTime: The time the challenge ends",
		"target_books": "Integer: The target of the books read the participants have to reach",
		"chhallenge_type": "Enum('public', 'private')
	}
}
```

### `POST /challenges/<challenge_id>/join`

- Joins the user who made the request the challenge
- Request arguments: None
- Request parameters: `challenge_id: The unique id of the challenge`
- Authorization: Required
- Request body:

```json
{}
```

- Response body:

```json
{
	"uid": "Integer: The unique id of the user",
	"challenge_id": "Integer: The unique id of the challenge"
}
```
