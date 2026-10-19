import d from './clinics.json';
export const KANSAI = ['大阪','京都','兵庫','滋賀'];
export const AREAS = {
  osaka: { name: '大阪', match: c => c.prefectures.includes('大阪') },
  tokyo: { name: '東京', match: c => c.prefectures.includes('東京') },
  kyoto: { name: '京都', match: c => c.prefectures.includes('京都') },
  hyogo: { name: '兵庫・神戸', match: c => c.prefectures.includes('兵庫') },
  kansai: { name: '関西（大阪・京都・兵庫・滋賀）', match: c => c.prefectures.some(p => KANSAI.includes(p)) },
};
export const METHODS = {
  miradry: { t: ['miradry'], name: 'ミラドライ', h1: 'ミラドライの値段・料金一覧', kw: 'ミラドライ 値段' },
  senjo: { t: ['senjo_ins','senjo'], name: 'ワキガ手術（剪除法）', h1: 'ワキガ手術（剪除法）の費用一覧：保険適用と自費', kw: 'ワキガ手術 費用' },
  botox: { t: ['botox'], name: 'ワキのボトックス注射', h1: 'ワキのボトックス注射の料金一覧', kw: 'ワキ ボトックス 料金' },
};
export function rows(filterClinic = () => true, types = null) {
  const out = [];
  for (const c of d.clinics) {
    if (!filterClinic(c)) continue;
    for (const p of c.prices) {
      if (types && !types.includes(p.t)) continue;
      out.push({ c, p, checked: c.checked_at || d.checked_at });
    }
  }
  return out.sort((a, b) => a.p.price - b.p.price || a.c.name.localeCompare(b.c.name, 'ja'));
}
export function stats(vals) {
  if (!vals.length) return null;
  const s = [...vals].sort((a, b) => a - b), n = s.length;
  const med = n % 2 ? s[(n - 1) / 2] : (s[n / 2 - 1] + s[n / 2]) / 2;
  return { min: s[0], med: Math.round(med), max: s[n - 1], n };
}
// 比較用に「両脇」に揃えた値（片側表記は×2の単純計算、単位不明は除外）
export function bothSides(p) { return p.unit === '両脇' ? p.price : p.unit === '片側' ? p.price * 2 : null; }
export { d };
