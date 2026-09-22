# v1.36 S043 specialist first-fail

The first specialist run failed on a test-string assertion for the new SKILL.md rule. The semantic rule was already present as `启发式收敛不能证明 Gap=0/global optimum`, while the test searched for the shorter exact substring ending at `Gap=0`. This is a harness wording mismatch, not loss of the rule or a modeling failure. The failed run is preserved; the test is adjusted to match the actual rule heading/text without weakening any S043 semantic, split, reproduction, arithmetic or Test/Dev boundary assertion.
