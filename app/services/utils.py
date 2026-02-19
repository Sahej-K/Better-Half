def list_to_csv(items: list[str] | None) -> str | None:
    if not items:
        return None
    return ",".join(sorted(set(x.strip().lower() for x in items if x)))

<<<<<<< HEAD

=======
>>>>>>> 095922fdc5ba1e9dd0b202cabbfe004f07a944a0
def csv_to_list(s: str | None) -> list[str]:
    if not s:
        return []
    return [x.strip() for x in s.split(",") if x.strip()]
