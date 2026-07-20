# Selected Model

Selected finalist for the private solution package: `G0-qwen2.5-7b-qlora-3ep`.

- Base: `Qwen/Qwen2.5-7B-Instruct@a09a35458c702b33eeacc393d103063234e8bc28`
- Adapter: `arabic-aisa/arabicfc-7b@57aa2ab514e8fca42a5643df3fec8b0157b5437d`
- Default ruleset: `accepted`
- Public-dev candidate ruleset: `surface_v2`

The adapter is stored in a private Hugging Face model repository. Grant
authorized recipients read access there before expecting `configs/*.yaml` to run
remotely.

`HF_POINTER.json` records the exact base model, adapter repository, and revision.
