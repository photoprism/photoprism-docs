# CLI Conventions

**Last Updated:** September 28, 2026

CLI commands are implemented in [`internal/commands`](https://github.com/photoprism/photoprism/tree/develop/internal/commands) (Community Edition), with Plus, Pro, and Portal registering their own commands and extending the shared ones under their own `internal/cmd`. This page covers the conventions new commands are expected to follow so that scripts, CI, and automation can rely on consistent behavior across editions.

## Confirmation Prompts

A command that performs a destructive or hard-to-reverse action (delete, reset, rotate credentials) asks for confirmation before proceeding, using [`commands.ConfirmAction`](https://github.com/photoprism/photoprism/blob/develop/internal/commands/commands.go):

- **`--yes`, `-y`** — added via [`YesFlag()`](https://github.com/photoprism/photoprism/blob/develop/internal/commands/flags.go) — skips the prompt and proceeds. Every command that prompts must offer it, or it cannot be run from a script at all.
- **`PHOTOPRISM_CLI=noninteractive`** has the same effect globally, without changing the command line. Prefer it in CI and tests; scripts should still pass `--yes` explicitly.
- Answering "no" at the prompt, or Ctrl-C, is not a failure: nothing is done and the command exits `0`.
- Without a terminal attached and without `--yes`, the prompt cannot be shown at all. That is a usage problem, not a completed run, so the command exits `2` with a message naming `--yes` — it never silently succeeds without doing the work.

```go
if proceed, err := commands.ConfirmAction(ctx.Bool("yes"), "Remove everything?"); err != nil {
    return err
} else if !proceed {
    log.Infof("nothing was removed")
    return nil
}
```

## Restoring a Deleted Record

`users add`, `users mod`, and `clients mod` offer to restore a soft-deleted account or client when the identifier they were given matches one. This is a different kind of prompt: it offers an *alternative* to the action requested, rather than confirming it. Declining it (or being unable to ask) leaves the requested add or modify undone, so these commands exit `1`, and the offer is accepted with its own **`--restore`** flag rather than `--yes`. Carrying `--yes` over from an unrelated command like `users rm --yes` must never bring back a record nobody asked to restore. A restored record keeps its previous role, credentials, and settings unless the command's own flags change them, so an account deleted by mistake comes back the way it was.

## Exit Codes

Scripts can rely on the exit code without parsing the message:

| Code    | Meaning                                                                                                                         |
|---------|---------------------------------------------------------------------------------------------------------------------------------|
| `0`     | Success, a declined confirmation, or a user-initiated cancel                                                                    |
| `1`     | Runtime failure (database, I/O, configuration, or a declined restore offer — see above)                                         |
| `2`     | Usage error or unmet precondition (invalid flags, a missing required flag, a confirmation that cannot be shown without `--yes`) |
| `3`     | The named user, client, session, or other resource does not exist or was already deleted                                        |
| `4`–`6` | Portal-specific: unauthorized, conflict, and rate-limited, mirroring the HTTP status the Portal returned                        |

The full table with examples for each code lives in [`internal/commands/README.md`](https://github.com/photoprism/photoprism/blob/develop/internal/commands/README.md#exit-codes).

## Positional Arguments Before Flags

Because flag parsing stops at the first non-flag token, a flag placed after a positional argument (for example `photoprism users mod bob --role guest`, with `--role` last) is silently ignored rather than rejected. Commands that take a positional call [`commands.RejectTrailingFlags(ctx)`](https://github.com/photoprism/photoprism/blob/develop/internal/commands/README.md#positional-arguments--flag-order) near the top of their action so a misplaced flag becomes a clear error instead of a no-op that still reports success.

## Testing

Wrap CLI invocations in tests with `RunWithTestContext(cmd, args)` so `urfave/cli` exit codes do not call `os.Exit` mid-test. See [Running Tests](tests.md) for the broader test setup, and the [`internal/commands/README.md`](https://github.com/photoprism/photoprism/blob/develop/internal/commands/README.md#testing-strategy) testing section for CLI-specific helpers.
