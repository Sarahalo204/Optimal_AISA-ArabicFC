# Results

Dataset revision: `1a5e5f8a9eeadd996118a8a86f72c4285047a00e`
Evaluator revision: `f73d1f95d2ccd3219e01cf2aa68173018acd9e0d`

| Run | Split | FnAcc | ArgEM | Track A | Track B |
| --- | --- | ---: | ---: | ---: | ---: |
| G0 raw | public dev | 0.996330 | 0.782333 | 0.867732 | 0.686699 |
| G0 legacy postprocess | public dev | 0.996330 | 0.814000 | 0.886932 | 0.705899 |
| G0 legacy postprocess plus Track B think | public dev | 0.996330 | 0.814000 | 0.886932 | 0.905899 |
| G0 accepted postprocess | public dev | 0.996330 | 0.782000 | 0.867732 | 0.689899 |
| G0 accepted postprocess plus Track B think | public dev | 0.996330 | 0.782000 | 0.867732 | 0.889899 |
| G0 surface_v2 public-dev candidate | public dev | 0.996330 | 0.834000 | 0.898932 | 0.715899 |
| G0 surface_v2 plus Track B think | public dev | 0.996330 | 0.834000 | 0.898932 | 0.915899 |
| G0 raw | internal tune | 1.000000 | 0.817748 | 0.890649 | 0.708874 |
| G0 accepted postprocess | internal tune | 1.000000 | 0.819656 | 0.891794 | 0.709828 |
| G0 raw | internal lockbox | 0.999052 | 0.813397 | 0.887659 | 0.706414 |
| G0 accepted postprocess | internal lockbox | 1.000000 | 0.815311 | 0.889187 | 0.707656 |
| G0 surface_v2 | internal lockbox | 1.000000 | 0.807656 | 0.884593 | 0.703828 |
| A0 RunPod no-arg Qwen | internal lockbox | 0.999052 | 0.762679 | 0.857229 | 0.681055 |
| A1 RunPod arg-weighted Qwen | internal lockbox | n/a | n/a | 0.807678 | n/a |
| A6b RunPod ALLaM no-arg | internal lockbox | n/a | n/a | 0.004940 | n/a |
| B1 RunPod Track B continuation | internal lockbox | 0.709953 | 0.581818 | 0.633072 | 0.703895 |

The selected private solution artifact is G0. `accepted` is the principled
default ruleset; `surface_v2` is the public-dev leaderboard candidate and should
not be treated as hidden-test safe without new internal evidence.

The internal split is deterministic; regenerate the full split manifest with
`scripts/make_splits.py` when needed instead of tracking the full JSONL package
artifact.
