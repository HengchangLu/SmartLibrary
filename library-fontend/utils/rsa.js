var RSA = require('./wx_rsa.js')
/**
 * 封装RSA加密
 */
export default function rsa(input_rsa) {
    // 获取时间戳
    var timestamp = new Date().getTime();
    input_rsa = timestamp + "," + input_rsa

    // 公钥 pk
    var publicKey = '-----BEGIN PUBLIC KEY-----\
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCjZoAkJB9vPcihNuDKum2RNM/B\
6eIcKcbCZyllTOoPfhcQeWLvyAdjcwj8/luoeu8ahvsCoo7v+ZOUWXmTNxtt8mDK\
SMWWlHq0tn5dujEUEqRPwoaw2xwTXZBkgrtrZpmwtcUvWcXd5mXYJn5McJHY4pAC\
Sy3dNT90ul3fngefSQIDAQAB\
-----END PUBLIC KEY-----'
    // 加密
    var encrypt_rsa = new RSA.RSAKey();
    var encrypt_rsa = RSA.KEYUTIL.getKey(publicKey);
    var encStr = encrypt_rsa.encrypt(input_rsa)
    encStr = RSA.hex2b64(encStr);
    encStr = encStr.replace(/\+/g, '%2b')
    return encStr
}