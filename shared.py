"""Shared data + helpers for all space widgets."""
import json, urllib.request, os, hashlib, random, math, datetime

random.seed(42)

CACHE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".cache")
COLORS = ["#00e5a0","#00b4d8","#8338ec","#ff006e","#fb5607","#ffbe0b","#3a86ff","#06d6a0","#ef476f","#118ab2"]

SAMPLE_REPOS = [
    {"name": "OpenSearch", "stargazers_count": 12800, "open_issues_count": 2800, "forks_count": 2200, "pushed_at": "2026-05-01T00:00:00Z", "language": "Java"},
    {"name": "OpenSearch-Dashboards", "stargazers_count": 2049, "open_issues_count": 1570, "forks_count": 980, "pushed_at": "2026-05-01T00:00:00Z", "language": "TypeScript"},
    {"name": "data-prepper", "stargazers_count": 366, "open_issues_count": 769, "forks_count": 310, "pushed_at": "2026-05-01T00:00:00Z", "language": "Java"},
    {"name": "opensearch-build", "stargazers_count": 199, "open_issues_count": 246, "forks_count": 180, "pushed_at": "2026-04-30T00:00:00Z", "language": "Shell"},
    {"name": "neural-search", "stargazers_count": 114, "open_issues_count": 125, "forks_count": 60, "pushed_at": "2026-05-01T00:00:00Z", "language": "Java"},
    {"name": "index-management", "stargazers_count": 76, "open_issues_count": 191, "forks_count": 95, "pushed_at": "2026-05-01T00:00:00Z", "language": "Kotlin"},
    {"name": "opensearch-migrations", "stargazers_count": 71, "open_issues_count": 88, "forks_count": 45, "pushed_at": "2026-04-30T00:00:00Z", "language": "Java"},
    {"name": "flow-framework", "stargazers_count": 55, "open_issues_count": 46, "forks_count": 38, "pushed_at": "2026-05-01T00:00:00Z", "language": "Java"},
    {"name": "opensearch-py", "stargazers_count": 462, "open_issues_count": 120, "forks_count": 150, "pushed_at": "2026-04-28T00:00:00Z", "language": "Python"},
    {"name": "opensearch-js", "stargazers_count": 229, "open_issues_count": 102, "forks_count": 88, "pushed_at": "2026-04-29T00:00:00Z", "language": "TypeScript"},
]

def fetch_json(url):
    os.makedirs(CACHE_DIR, exist_ok=True)
    cache_file = os.path.join(CACHE_DIR, hashlib.md5(url.encode()).hexdigest() + ".json")
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "opensearch-pulse"})
        with urllib.request.urlopen(req) as r:
            data = r.read()
        with open(cache_file, "wb") as f:
            f.write(data)
        return json.loads(data)
    except Exception:
        if os.path.exists(cache_file):
            with open(cache_file) as f:
                return json.load(f)
        return None

def get_repos():
    data = fetch_json("https://api.github.com/orgs/opensearch-project/repos?sort=pushed&per_page=10")
    return data if data else SAMPLE_REPOS

def fmt(n):
    return f"{n/1000:.1f}k" if n >= 1000 else str(n)

def now_str():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%b %d, %Y %H:%M UTC")

def starfield(w, h, count=100):
    s = ""
    for _ in range(count):
        sx, sy = random.uniform(0, w), random.uniform(0, h)
        sr, so = random.uniform(0.3, 1.1), random.uniform(0.15, 0.5)
        dur = random.uniform(2, 7)
        s += (f'<circle cx="{sx:.0f}" cy="{sy:.0f}" r="{sr:.1f}" fill="#fff" opacity="{so:.2f}">'
              f'<animate attributeName="opacity" values="{so:.2f};{so*0.2:.2f};{so:.2f}" dur="{dur:.1f}s" repeatCount="indefinite"/>'
              f'</circle>\n')
    return s
