// Dernière release de Seventh OS sur GitHub (gardée 5 min en cache par Cloudflare).
const REPO = 'se7enclaude/seventh-os';
export const RELEASES = `https://github.com/${REPO}/releases/latest`;

export async function latest() {
  try {
    const r = await fetch(`https://api.github.com/repos/${REPO}/releases/latest`, {
      headers: { 'User-Agent': 'seventh-os-site', Accept: 'application/vnd.github+json' },
      cf: { cacheTtl: 300, cacheEverything: true },
    });
    if (!r.ok) return null;
    const rel = await r.json();
    const exe = rel.assets?.find((a) => /^SeventhOS-Setup-.*\.exe$/i.test(a.name));
    if (!exe) return null;
    return { version: rel.tag_name.replace(/^v/, ''), size: exe.size, url: exe.browser_download_url, date: rel.published_at };
  } catch {
    return null;
  }
}
