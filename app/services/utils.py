def list_to_csv(items: list[str] | None) -> str | None:
    if not items:
        return None
    return ",".join(sorted(set(x.strip().lower() for x in items if x)))


def csv_to_list(s: str | None) -> list[str]:
    if not s:
        return []
    return [x.strip() for x in s.split(",") if x.strip()]
