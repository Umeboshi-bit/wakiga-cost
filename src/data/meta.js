export const T = { senjo:'剪除法(自費)', senjo_ins:'剪除法(保険適用)', miradry:'ミラドライ', botox:'ボトックス注射' };
export const yen = n => n.toLocaleString('ja-JP') + '円';
export const tax = v => v === true ? '税込' : v === false ? '税抜' : '税表記未確認';
