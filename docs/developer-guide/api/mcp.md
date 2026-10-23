# Model Context Protocol (MCP)

PhotoPrism includes a read-only server for the [Model Context Protocol](https://modelcontextprotocol.io/) (MCP), a JSON-RPC 2.0 protocol that lets AI assistants and agents use external tools and data sources in a standardized way. MCP-compatible clients can use it to look up reference information such as config options, search filters, CLI commands, and supported file formats, and to search and browse the library with the permissions of the signed-in account, for example to find pictures, see which albums a picture is in, or list the people and labels to search by.

| Transport       | Endpoint / Command     | Authentication                                                                | Typical Use                                 |
|-----------------|------------------------|-------------------------------------------------------------------------------|---------------------------------------------|
| Streamable HTTP | `/api/v1/mcp`          | [Connected app](#connecting-clients) or [access token](auth.md#access-tokens) | Remote MCP clients, assistants, and agents  |
| stdio           | `photoprism mcp serve` | none (local process)                                                          | Development, testing, and the MCP Inspector |

Both transports serve the reference tools and resources. The [library tools](#library-tools) are only available over HTTP to authenticated users and clients, not in [public mode](#authorization) or with `photoprism mcp serve`.

## Available Tools

| Tool                   | Inputs                                 | Returns                                                                                            |
|------------------------|----------------------------------------|----------------------------------------------------------------------------------------------------|
| `list_config_keys`     | `section`, `query`, `edition`, `limit` | Matching config options with environment variable, CLI flag, default value, and description        |
| `find_search_filters`  | `query`, `type`, `limit`               | Matching [search filters](search.md) with type, examples, and notes                                |
| `list_cli_commands`    | `query`, `limit`, `offset`             | Commands of the running edition with usage, description, arguments, aliases, and their own flags   |
| `list_file_formats`    | `query`, `type`, `limit`, `offset`     | Supported file formats with type, extensions, and description, e.g. for `image`, `raw`, or `video` |
| `list_metadata_fields` | `query`, `limit`, `offset`             | Metadata fields with type and the matching Exiftool, XMP, and Dublin Core tags                     |
| `list_thumbnail_sizes` | `type` (`image`, `video`, or `all`)    | Thumbnail sizes with width, height, aspect ratio, and usage, or only the standard video sizes      |

These reference tools return the same information as the matching [`photoprism show`](../../getting-started/docker-compose.md#command-line-interface) commands of the running edition, so Plus, Pro, and Portal include their own commands. Results of tools with a `limit` input include `items`, `total`, `limit`, `offset`, and `truncated`; `limit` defaults to 20 and can be at most 50.

### Library Tools

| Tool               | Inputs                                                                                                       | Returns                                                                             | Scope               |
|--------------------|--------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------|---------------------|
| `search_media`     | `query`, `type`, `collection`, `person`, `taken_after`, `taken_before`, `order`, `limit`, `offset`, `detail` | Pictures and videos found with the web app's [search](search.md), in the same order | `photos`            |
| `get_media`        | `uid`                                                                                                        | One picture or video with its details, files, labels, people, and albums            | `photos`            |
| `list_collections` | `type`, `query`, `limit`, `offset`                                                                           | Albums, folders, moments, months, or states with their picture count and cover      | `albums` and others |
| `get_collection`   | `uid`                                                                                                        | One album or other collection                                                       | `albums` and others |
| `list_people`      | `query`, `limit`, `offset`                                                                                   | People with their picture count and cover                                           | `people`            |
| `list_labels`      | `query`, `all`, `limit`, `offset`                                                                            | Labels with their picture count, categories, and the slug for the `label:` filter   | `labels`            |

The library tools only return what the account sees in the web app: private and archived pictures follow its role, and private albums, hidden people, and private labels stay hidden from accounts that cannot see them. They cannot change anything.

Results of `search_media` contain up to `limit` pictures (at most 50) and no total. To get the next page, pass back the `next_offset` of the previous result as `offset`; it is omitted on the last page. Pictures added or removed between two calls can shift the position, so a picture may then repeat or be skipped, as when scrolling in the web app.

A token needs the scope of the tool's resource besides `mcp`, for example `mcp read photos`. Collections of other types need the scope of their resource: `folders`, `moments`, `calendar` (months), or `places` (states). If the token lacks the scope, the endpoint answers `403 Forbidden` with an `insufficient_scope` error that names the scopes to request, and connected apps ask the user to approve the additional access.

## Available Resources

| Resource URI                   | Content                                  |
|--------------------------------|------------------------------------------|
| `photoprism://config-options`  | All config options as JSON               |
| `photoprism://search-filters`  | All search filters as JSON               |
| `photoprism://cli-commands`    | All CLI commands and their flags as JSON |
| `photoprism://file-formats`    | All supported file formats as JSON       |
| `photoprism://metadata-fields` | All metadata fields as JSON              |
| `photoprism://thumbnail-sizes` | All thumbnail sizes as JSON              |

## Connecting Clients

### OAuth Sign-In

MCP clients that support OAuth, such as remote connectors in AI assistants, can be [connected by users](oauth2.md#connecting-apps) without copying a token: when a client calls `/api/v1/mcp` without a valid access token, the `401 Unauthorized` response includes a `WWW-Authenticate` header that points to the [protected resource metadata](index.md#oauth2-protected-resource) at `/.well-known/oauth-protected-resource/api/v1/mcp`. The client then finds the authorization server, sends the user to the consent page, and receives an access token for the MCP endpoint.

For this, the client must either be [registered with its redirect URIs](auth.md#app-clients) or publish a client metadata document that the [`--oauth-apps`](oauth2.md#configuration) option allows:

```bash
photoprism clients add -n "My Assistant" --redirect-uri https://assistant.example.com/oauth/callback
```

Users can see and disconnect their connected clients under *Settings > Account > Connected Apps*.

### Access Tokens

Alternatively, you can create an [access token](auth.md#access-tokens) or [client credentials](auth.md#client-credentials) whose scope includes `mcp` and enter the token in the client config:

```bash
photoprism clients add -n "MCP Client" -s mcp
```

Most MCP clients support Streamable HTTP with custom headers:

```json
{
  "mcpServers": {
    "photoprism": {
      "url": "https://photos.example.com/api/v1/mcp",
      "headers": {
        "Authorization": "Bearer <token>"
      }
    }
  }
}
```

Clients that only support stdio servers can use [`mcp-remote`](https://www.npmjs.com/package/mcp-remote) as a bridge:

```json
{
  "mcpServers": {
    "photoprism": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "https://photos.example.com/api/v1/mcp", "--header", "Authorization:${AUTH_HEADER}"],
      "env": {
        "AUTH_HEADER": "Bearer <token>"
      }
    }
  }
}
```

### Local Testing

To try the server locally, start it via stdio with the [MCP Inspector](https://github.com/modelcontextprotocol/inspector), for example in the [development environment](../setup.md):

```bash
npx @modelcontextprotocol/inspector ./photoprism mcp serve
```

## Authorization

The HTTP endpoint is available to admins in all editions, to users and viewers in PhotoPrism® Plus and Pro, to managers in PhotoPrism® Pro, and to API clients. Contributors, guests, and visitors cannot use it. Access tokens of API clients must include the `mcp` scope, plus the scope of each [library tool](#library-tools) they call; we recommend adding `read`, e.g. `mcp read photos albums people labels`, since a resource scope without `read` also permits changes through the REST API. Add `places` only if the client should receive the coordinates of pictures.

MCP is enabled by default for every account whose role may use it. Admins can turn it off for a single account in the user settings or with `photoprism users mod --mcp=false <username>` (`--mcp` turns it on again). Turning it off disconnects the account's apps and signs out its other sessions; it also applies to API clients that belong to the account.

In [public mode](../../getting-started/config-options.md#authentication), the endpoint can be used without authentication and only offers the reference tools.

## Configuration

| Environment Variable     | CLI Flag        | Description                                                                                 |
|--------------------------|-----------------|---------------------------------------------------------------------------------------------|
| `PHOTOPRISM_DISABLE_MCP` | `--disable-mcp` | Disables the `/api/v1/mcp` endpoint and the `photoprism mcp serve` command for all accounts |
| `PHOTOPRISM_OAUTH_APPS`  | `--oauth-apps`  | Controls which apps and MCP clients users can [connect with OAuth](oauth2.md#configuration) |

## Contributing

We welcome contributions that extend the MCP server. Every tool declares the resource and action it needs, which the server checks for each call against the role, the account's MCP setting, and the token scope; tools that read library data apply the same visibility rules as the matching REST API endpoints. Please open an issue or a discussion before you start, so we can agree on the tool names and behavior. The source code is in [`internal/mcp`](https://github.com/photoprism/photoprism/tree/develop/internal/mcp), and the issue that tracks MCP support is [#5024](https://github.com/photoprism/photoprism/issues/5024).

## Related Issues

- [AI: Add support for Model Context Protocol (MCP) #5024](https://github.com/photoprism/photoprism/issues/5024)
- [Auth: Add `authorize` API endpoint to implement the authorization code flow #4368](https://github.com/photoprism/photoprism/issues/4368)
- [MCP: Add `--disable-mcp` flag to optionally disable the MCP API endpoint #5536](https://github.com/photoprism/photoprism/issues/5536)
- [MCP: Add reference tools for CLI commands, file formats, metadata, and thumbnails #5910](https://github.com/photoprism/photoprism/issues/5910)
- [MCP: Add tools to search and browse the library with the user's permissions #5911](https://github.com/photoprism/photoprism/issues/5911)

## Protocol References

- https://modelcontextprotocol.io/specification/
- https://modelcontextprotocol.io/specification/draft/basic/authorization
- https://datatracker.ietf.org/doc/html/rfc9728
