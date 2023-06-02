function u(t, n) {
    if (null == t)
        throw new Error("Illegal argument " + t);
    var r = e_wordsToBytes(s(t, n));
    return n && n.asBytes ? r : n && n.asString ? i.bytesToString(r) : e_bytesToHex(r)
}

function e_wordsToBytes(t) {
    for (var e = [], n = 0; n < 32 * t.length; n += 8)
        e.push(t[n >>> 5] >>> 24 - n % 32 & 255);
    return e
}

function e_bytesToHex(t) {
    for (var e = [], n = 0; n < t.length; n++)
        e.push((t[n] >>> 4).toString(16)),
            e.push((15 & t[n]).toString(16));
    return e.join("")
}

function n_stringToBytes(t) {
    return i_stringToBytes(unescape(encodeURIComponent(t)))
}

function i_stringToBytes(t) {
    for (var e = [], n = 0; n < t.length; n++)
        e.push(255 & t.charCodeAt(n));
    return e
}

function e_bytesToWords(t) {
    for (var e = [], n = 0, r = 0; n < t.length; n++,
        r += 8)
        e[r >>> 5] |= t[n] << 24 - r % 32;
    return e
}

function e_endian(t) {
    if (t.constructor == Number)
        return 16711935 & n_rotl(t, 8) | 4278255360 & n_rotl(t, 24);
    for (var e = 0; e < t.length; e++)
        t[e] = e_endian(t[e]);
    return t
}

function n_rotl(t, e) {
    return t << e | t >>> 32 - e
}

function s(t, o) {
    t.constructor == String ? t = o && "binary" === o.encoding ? i_stringToBytes(t) : n_stringToBytes(t) : r(t) ? t = Array.prototype.slice.call(t, 0) : Array.isArray(t) || t.constructor === Uint8Array || (t = t.toString());
    for (var a = e_bytesToWords(t), c = 8 * t.length, u = 1732584193, l = -271733879, f = -1732584194, p = 271733878, d = 0; d < a.length; d++)
        a[d] = 16711935 & (a[d] << 8 | a[d] >>> 24) | 4278255360 & (a[d] << 24 | a[d] >>> 8);
    a[c >>> 5] |= 128 << c % 32,
        a[14 + (c + 64 >>> 9 << 4)] = c;
    var h = s._ff
        , v = s._gg
        , m = s._hh
        , y = s._ii;
    for (d = 0; d < a.length; d += 16) {
        var g = u
            , b = l
            , w = f
            , x = p;
        u = h(u, l, f, p, a[d + 0], 7, -680876936),
            p = h(p, u, l, f, a[d + 1], 12, -389564586),
            f = h(f, p, u, l, a[d + 2], 17, 606105819),
            l = h(l, f, p, u, a[d + 3], 22, -1044525330),
            u = h(u, l, f, p, a[d + 4], 7, -176418897),
            p = h(p, u, l, f, a[d + 5], 12, 1200080426),
            f = h(f, p, u, l, a[d + 6], 17, -1473231341),
            l = h(l, f, p, u, a[d + 7], 22, -45705983),
            u = h(u, l, f, p, a[d + 8], 7, 1770035416),
            p = h(p, u, l, f, a[d + 9], 12, -1958414417),
            f = h(f, p, u, l, a[d + 10], 17, -42063),
            l = h(l, f, p, u, a[d + 11], 22, -1990404162),
            u = h(u, l, f, p, a[d + 12], 7, 1804603682),
            p = h(p, u, l, f, a[d + 13], 12, -40341101),
            f = h(f, p, u, l, a[d + 14], 17, -1502002290),
            u = v(u, l = h(l, f, p, u, a[d + 15], 22, 1236535329), f, p, a[d + 1], 5, -165796510),
            p = v(p, u, l, f, a[d + 6], 9, -1069501632),
            f = v(f, p, u, l, a[d + 11], 14, 643717713),
            l = v(l, f, p, u, a[d + 0], 20, -373897302),
            u = v(u, l, f, p, a[d + 5], 5, -701558691),
            p = v(p, u, l, f, a[d + 10], 9, 38016083),
            f = v(f, p, u, l, a[d + 15], 14, -660478335),
            l = v(l, f, p, u, a[d + 4], 20, -405537848),
            u = v(u, l, f, p, a[d + 9], 5, 568446438),
            p = v(p, u, l, f, a[d + 14], 9, -1019803690),
            f = v(f, p, u, l, a[d + 3], 14, -187363961),
            l = v(l, f, p, u, a[d + 8], 20, 1163531501),
            u = v(u, l, f, p, a[d + 13], 5, -1444681467),
            p = v(p, u, l, f, a[d + 2], 9, -51403784),
            f = v(f, p, u, l, a[d + 7], 14, 1735328473),
            u = m(u, l = v(l, f, p, u, a[d + 12], 20, -1926607734), f, p, a[d + 5], 4, -378558),
            p = m(p, u, l, f, a[d + 8], 11, -2022574463),
            f = m(f, p, u, l, a[d + 11], 16, 1839030562),
            l = m(l, f, p, u, a[d + 14], 23, -35309556),
            u = m(u, l, f, p, a[d + 1], 4, -1530992060),
            p = m(p, u, l, f, a[d + 4], 11, 1272893353),
            f = m(f, p, u, l, a[d + 7], 16, -155497632),
            l = m(l, f, p, u, a[d + 10], 23, -1094730640),
            u = m(u, l, f, p, a[d + 13], 4, 681279174),
            p = m(p, u, l, f, a[d + 0], 11, -358537222),
            f = m(f, p, u, l, a[d + 3], 16, -722521979),
            l = m(l, f, p, u, a[d + 6], 23, 76029189),
            u = m(u, l, f, p, a[d + 9], 4, -640364487),
            p = m(p, u, l, f, a[d + 12], 11, -421815835),
            f = m(f, p, u, l, a[d + 15], 16, 530742520),
            u = y(u, l = m(l, f, p, u, a[d + 2], 23, -995338651), f, p, a[d + 0], 6, -198630844),
            p = y(p, u, l, f, a[d + 7], 10, 1126891415),
            f = y(f, p, u, l, a[d + 14], 15, -1416354905),
            l = y(l, f, p, u, a[d + 5], 21, -57434055),
            u = y(u, l, f, p, a[d + 12], 6, 1700485571),
            p = y(p, u, l, f, a[d + 3], 10, -1894986606),
            f = y(f, p, u, l, a[d + 10], 15, -1051523),
            l = y(l, f, p, u, a[d + 1], 21, -2054922799),
            u = y(u, l, f, p, a[d + 8], 6, 1873313359),
            p = y(p, u, l, f, a[d + 15], 10, -30611744),
            f = y(f, p, u, l, a[d + 6], 15, -1560198380),
            l = y(l, f, p, u, a[d + 13], 21, 1309151649),
            u = y(u, l, f, p, a[d + 4], 6, -145523070),
            p = y(p, u, l, f, a[d + 11], 10, -1120210379),
            f = y(f, p, u, l, a[d + 2], 15, 718787259),
            l = y(l, f, p, u, a[d + 9], 21, -343485551),
            u = u + g >>> 0,
            l = l + b >>> 0,
            f = f + w >>> 0,
            p = p + x >>> 0
    }
    return e_endian([u, l, f, p])
};
s._ff = function (t, e, n, r, o, i, a) {
    var c = t + (e & n | ~e & r) + (o >>> 0) + a;
    return (c << i | c >>> 32 - i) + e
}
    ,
    s._gg = function (t, e, n, r, o, i, a) {
        var c = t + (e & r | n & ~r) + (o >>> 0) + a;
        return (c << i | c >>> 32 - i) + e
    }
    ,
    s._hh = function (t, e, n, r, o, i, a) {
        var c = t + (e ^ n ^ r) + (o >>> 0) + a;
        return (c << i | c >>> 32 - i) + e
    }
    ,
    s._ii = function (t, e, n, r, o, i, a) {
        var c = t + (n ^ (e | ~r)) + (o >>> 0) + a;
        return (c << i | c >>> 32 - i) + e
    }
var _input1 = process.argv[2];
// var t = _input1 + "ce6d4422ece814c69d256fa9617e4acc" // 这个值好像是固定的有问题再说
var t = _input1
// console.log(t)
var a = u(t)

console.log(a)