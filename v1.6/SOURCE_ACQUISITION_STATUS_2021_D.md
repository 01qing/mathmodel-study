# 2021 D Source Acquisition Status

## Source hierarchy

| Source | Role | Can directly serve as real benchmark input? |
|---|---|---|
| zhanwen/MathModel XLSX | contest attachment mirror | Yes, after local hash verification + data audit |
| Bureaux-Tao CSV | participant converted mirror | No, until XLSX-vs-CSV cross-check passes |

## Current runtime

GitHub metadata and text-source access work, but the model container cannot currently materialize the large remote binaries/text blobs. Therefore real dataset execution remains `NOT_RUN`.

The Skill now contains an acquisition manifest and scripts so the same step can run automatically when executed in a network-enabled Codex/local environment.
