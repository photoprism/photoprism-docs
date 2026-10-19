# Model Context Protocol (MCP)

PhotoPrism includes a read-only server for the [Model Context Protocol](https://modelcontextprotocol.io/) (MCP), a JSON-RPC 2.0 protocol that lets AI assistants and agents use external tools and data sources in a standardized way. MCP-compatible clients can use it to look up reference information such as config options, search filters, CLI commands, and supported file formats, for example to help users configure an instance, build search queries, or find the right command for the edition they run.

| Transport       | Endpoint / Command     | Authentication                                                                | Typical Use                                 |
|-----------------|------------------------|-------------------------------------------------------------------------------|---------------------------------------------|
| Streamable HTTP | `/api/v1/mcp`          | [Connected app](#connecting-clients) or [access token](auth.md#access-tokens) | Remote MCP clients, assistants, and agents  |
| stdio           | `photoprism mcp serve` | none (local process)                                                          | Development, testing, and the MCP Inspector |

Both transports serve the same tools and resources.

## Available Tools

| Tool                   | Inputs                                 | Returns                                                                                            |
|------------------------|----------------------------------------|----------------------------------------------------------------------------------------------------|
| `list_config_keys`     | `section`, `query`, `edition`, `limit` | Matching config options with environment variable, CLI flag, default value, and description        |
| `find_search_filters`  | `query`, `type`, `limit`               | Matching [search filters](search.md) with type, examples, and notes                                |
| `list_cli_commands`    | `query`, `limit`, `offset`             | Commands of the running edition with usage, description, arguments, aliases, and their own flags   |
| `list_file_formats`    | `query`, `type`, `limit`, `offset`     | Supported file formats with type, extensions, and description, e.g. for `image`, `raw`, or `video` |
| `list_metadata_fields` | `query`, `limit`, `offset`             | Metadata fields with type and the matching Exiftool, XMP, and Dublin Core tags                     |
| `list_thumbnail_sizes` | `type` (`image`, `video`, or `all`)    | Thumbnail sizes with width, height, aspect ratio, and usage, or only the standard video sizes      |

All tools are read-only and return the same information as the matching [`photoprism show`](../../getting-started/docker-compose.md#command-line-interface) commands of the running edition, so Plus, Pro, and Portal include their own commands. Results of tools with a `limit` input include `items`, `total`, `limit`, `offset`, and `truncated`; `limit` defaults to 20 and can be at most 50.

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

For this, the client must either be [registered with its callback URLs](auth.md#app-clients) or publish a client metadata document that the [`--oauth-apps`](oauth2.md#configuration) option allows:

```bash
photoprism clients add -n "My Assistant" --callback https://assistant.example.com/oauth/callback
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

The HTTP endpoint is available to admins and API clients in all editions, and to managers in PhotoPrism® Pro. Access tokens of API clients must include the `mcp` scope or a wildcard.

In [public mode](../../getting-started/config-options.md#authentication), the endpoint can be used without authentication, since the tools and resources it currently provides only return reference information and no library data.

## Configuration

| Environment Variable     | CLI Flag        | Description                                                                                 |
|--------------------------|-----------------|---------------------------------------------------------------------------------------------|
| `PHOTOPRISM_DISABLE_MCP` | `--disable-mcp` | Disables the `/api/v1/mcp` endpoint and the `photoprism mcp serve` command                  |
| `PHOTOPRISM_OAUTH_APPS`  | `--oauth-apps`  | Controls which apps and MCP clients users can [connect with OAuth](oauth2.md#configuration) |

## Contributing

We welcome contributions that extend the MCP server, for example with tools that search the library. Tools that read or change library data must check the permissions of the user or client for each call, with the same rules as the matching REST API endpoints. Please open an issue or a discussion before you start, so we can agree on the tool names and behavior. The source code is in [`internal/mcp`](https://github.com/photoprism/photoprism/tree/develop/internal/mcp), and the issue that tracks MCP support is [#5024](https://github.com/photoprism/photoprism/issues/5024).

## Related Issues

- [AI: Add support for Model Context Protocol (MCP) #5024](https://github.com/photoprism/photoprism/issues/5024)
- [Auth: Add `authorize` API endpoint to implement the authorization code flow #4368](https://github.com/photoprism/photoprism/issues/4368)
- [MCP: Add `--disable-mcp` flag to optionally disable the MCP API endpoint #5536](https://github.com/photoprism/photoprism/issues/5536)
- [MCP: Add reference tools for CLI commands, file formats, metadata, and thumbnails #5910](https://github.com/photoprism/photoprism/issues/5910)

## Protocol References

- https://modelcontextprotocol.io/specification/
- https://modelcontextprotocol.io/specification/draft/basic/authorization
- https://datatracker.ietf.org/doc/html/rfc9728
