// GET /api/latest : version, taille et lien de l'installateur de la dernière release de Seventh OS.
import { latest } from '../../lib/release.js';

export async function onRequestGet() {
  const rel = await latest();
  if (!rel) return Response.json({ error: 'indisponible' }, { status: 502 });
  return Response.json(rel, { headers: { 'Cache-Control': 'public, max-age=300' } });
}
