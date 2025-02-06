# Example Usage

Adding a Contact:

``` bash
uv run cli.py add-contact "John Doe" --telephone "+1-800-5551234" --email "<john.doe@example.com>"
```

Listing All Contacts:

``` bash
uv run cli.py list-contacts
```

Searching for a Contact:

``` bash
uv run cli.py search-contact "John Doe"
```

Editing a Contact:

``` bash
uv run cli.py edit-contact "John Doe" "John Doe Jr." --telephone "+1-800-5559876" --email "<john.jr@example.com>"
```

Deleting a Contact:

``` bash
uv run cli.py delete-contact "John Doe Jr."
```
