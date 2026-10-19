import { METHODS, AREAS, d } from '../data/util.js';
export async function GET({ site }) {
  const base = new URL(import.meta.env.BASE_URL.replace(/\/?$/, '/'), site).href;
  const paths = ['', 'clinics/', 'simulator/', 'check/', 'guide/', 'insurance/', 'senjo-recovery/', 'products/', 'policy/', 'compare/', 'insurance-conditions/', 'student/',
    ...Object.keys(METHODS).map(m => `price/${m}/`), ...Object.keys(AREAS).map(a => `area/${a}/`), ...d.clinics.map(c => `clinics/${c.id}/`)];
  const lastmod = new Date().toISOString().slice(0, 10);
  const xml = `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${paths.map(p => `<url><loc>${base}${p}</loc><lastmod>${lastmod}</lastmod></url>`).join('\n')}\n</urlset>\n`;
  return new Response(xml, { headers: { 'Content-Type': 'application/xml' } });
}
