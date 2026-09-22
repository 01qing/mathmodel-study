# Core Identity Gate — EMBEDDED / VERIFIED

Benchmark: ROLE-P1-2022C-v0.2

This run pack embeds the exact sealed wrapper:

- `release-v141.zip`
- wrapper SHA256: `a4ef5b69d31ab2b5de032e9fa9e8c78f15a09b773bfca3ace57870cdb418016f`

Wrapper audit performed before packaging:

- wrapper `unzip -t`: PASS
- embedded Core: `Graduate-MathModel-Learning-Skill-v1.41.zip`
- embedded Core SHA256: `191c4dad37c811049516c66862bd2d45d1364784ff277ec73e5667d07cb64d6f`
- embedded Core bytes: `206263605`
- embedded Core ZIP entries: `2341`
- embedded Core `unzip -t`: PASS
- release JSON version: `1.41.0`
- release JSON status: `SEALED`

At run start, verify `sha256sum release-v141.zip` against `release-v141.zip.sha256` before using the Core.
If it does not match, stop with `CORE_IDENTITY_GATE_FAIL`.

Do not replace this Core with v1.38/v1.40 or any reconstructed package.
