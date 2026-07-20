# Ready-To-Upload Dev Submissions

The official leaderboard accepts prediction JSONL files, not model uploads.
These files are the frozen public-dev candidate outputs generated from the
selected adapter and `surface_v2` ruleset.

| File | Track | Public-dev score |
| --- | --- | ---: |
| `track_a_public_dev_candidate.jsonl` | A | `0.898932` |
| `track_b_public_dev_candidate.jsonl` | B | `0.915899` |

Use these only for the public development leaderboard. For a hidden/final split,
generate fresh predictions from the adapter and configs instead of reusing these
dev-row files.
