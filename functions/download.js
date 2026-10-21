// GET /download : redirige vers l'installateur de la dernière release (lien court à partager).
import { latest, RELEASES } from '../lib/release.js';

export async function onRequestGet() {
  const rel = await latest();
  return Response.redirect(rel?.url || RELEASES, 302);
}
