"""Snippets the contract is tested against.

Six carry a real seeded defect. Two are correct — those are the control, and the
reason this suite catches the failure mode a "does it find bugs?" test cannot:
a contract that fires at everything scores perfectly on buggy code and lies.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Case:
    id: str
    lang: str
    code: str
    bug: str | None  # None => the code is correct; the case is a control


CASES: list[Case] = [
    Case(
        id="ts-stampede",
        lang="typescript",
        bug="cache stampede: the entry is written AFTER the await, so N concurrent "
            "calls for the same id all miss and all hit the database",
        code='''const cache = new Map<string, {value: User; expires: number}>();
const TTL_MS = 30_000;

export async function getUser(id: string): Promise<User> {
  const hit = cache.get(id);
  if (hit && hit.expires > Date.now()) return hit.value;
  const user = await db.users.findById(id);
  cache.set(id, {value: user, expires: Date.now() + TTL_MS});
  return user;
}

export async function renderTeam(memberIds: string[]) {
  const members = await Promise.all(memberIds.map(getUser));
  return members.map(toCard);
}''',
    ),
    Case(
        id="py-mutable-default",
        lang="python",
        bug="mutable default argument: the list is evaluated once at definition time "
            "and shared across every call",
        code='''def add_tag(name, tags=[]):
    tags.append(name)
    return tags


def build_report(items):
    out = []
    for it in items:
        out.append({"name": it.name, "tags": add_tag(it.kind)})
    return out''',
    ),
    Case(
        id="py-except-pass",
        lang="python",
        bug="swallowed exception: the bare except returning None erases the error, so "
            "the caller cannot tell 'no data' from 'the read failed'",
        code='''def load_config(path):
    try:
        with open(path) as f:
            return json.load(f)
    except:
        return None


def start():
    cfg = load_config("/etc/app/config.json")
    port = (cfg or {}).get("port", 8080)
    serve(port)''',
    ),
    Case(
        id="sql-nplusone",
        lang="python",
        bug="N+1 queries: one query per row in the loop instead of a join or an IN clause",
        code='''def list_orders(user_ids):
    rows = []
    for uid in user_ids:
        user = db.query("SELECT * FROM users WHERE id = ?", uid)
        orders = db.query("SELECT * FROM orders WHERE user_id = ?", uid)
        rows.append({"user": user, "orders": orders})
    return rows''',
    ),
    Case(
        id="js-off-by-one",
        lang="javascript",
        bug="off-by-one: the loop uses <= against length, so the last iteration reads "
            "undefined and throws on .price",
        code='''function totalCart(items) {
  let total = 0;
  for (let i = 0; i <= items.length; i++) {
    total += items[i].price * items[i].qty;
  }
  return total;
}''',
    ),
    Case(
        id="go-concurrent-map",
        lang="go",
        bug="data race: the goroutines write to a shared map without a mutex, which is "
            "a concurrent map write",
        code='''func fetchAll(urls []string) map[string]string {
    results := make(map[string]string)
    var wg sync.WaitGroup
    for _, u := range urls {
        wg.Add(1)
        go func(u string) {
            defer wg.Done()
            results[u] = get(u)
        }(u)
    }
    wg.Wait()
    return results
}''',
    ),
    # ---- controls: correct code ----
    Case(
        id="ctrl-py-slug",
        lang="python",
        bug=None,
        code='''def slugify(title: str) -> str:
    text = unicodedata.normalize("NFKD", title)
    text = text.encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"[^a-zA-Z0-9]+", "-", text).strip("-").lower()
    return text or "untitled"''',
    ),
    Case(
        id="ctrl-ts-clamp",
        lang="typescript",
        bug=None,
        code='''export function clamp(value: number, min: number, max: number): number {
  if (Number.isNaN(value)) return min;
  if (min > max) [min, max] = [max, min];
  return Math.min(Math.max(value, min), max);
}''',
    ),
]

BUGGY = [c for c in CASES if c.bug]
CONTROLS = [c for c in CASES if not c.bug]
