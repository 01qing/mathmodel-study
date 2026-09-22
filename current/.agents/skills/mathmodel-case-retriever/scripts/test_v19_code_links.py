from search_cases import _links_for_case_group, search

links=_links_for_case_group("2025-E")
assert len(links)==2
assert any(x["case_id"]=="2025-E-GTeacher2-code" for x in links)
r=search("2025 E 高速列车轴承 无标签目标域 迁移学习 MMD CORAL",mode="evaluation",top=10)
hits=[x for x in r["matches"] if x["case_group"]=="2025-E"]
assert hits, r
assert hits[0]["supplemental_code_cases"], hits[0]
assert "not proof" in r["supplemental_code_boundary"]
print("v1.9 code-link regression PASS")
