import base64
import json

from Crypto.Hash import SHA1, SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Util.asn1 import DerSequence, DerObjectId, DerNull, DerOctetString
from cryptography import x509
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization

# JetBrains CA
# 来自 https://github.com/JetBrains/marketplace-makemecoffee-plugin/blob/master/src/main/java/com/company/license/CheckLicense.java
ROOT_CERTIFICATES = ("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\n")

def create_power_file(active_code):
    subcert = x509.load_der_x509_certificate(base64.b64decode(active_code.split('-')[3]))
    s = int.from_bytes(subcert.signature, byteorder='big', signed=False)

    digest_cert = SHA256.new(subcert.tbs_certificate_bytes)
    digest_info = create_digest_info(digest_cert)

    # 使用标准的 PKCS#1 v1.5 填充构造
    key_size_bytes = subcert.public_key().key_size // 8  # 转换为字节数
    padded_data = create_pkcs1v15_padding(digest_info, key_size_bytes)
    r = int.from_bytes(padded_data, byteorder='big', signed=False)
    
    # 写入 power.conf 文件
    with open('power.conf', 'w', encoding='utf-8') as f:
        jb_ca = x509.load_der_x509_certificate(base64.b64decode(ROOT_CERTIFICATES))
        jb_ca_public_key = jb_ca.public_key()
        jb_ca_public_key_n = jb_ca_public_key.public_numbers().n
        jb_ca_public_key_e = jb_ca_public_key.public_numbers().e

        f.write("[Result]\n")
        f.write(f"EQUAL,{s},{jb_ca_public_key_e},{jb_ca_public_key_n}->{r}")


def create_digest_info(hash_obj):
    # 构造 AlgorithmIdentifier
    algorithm_id = DerSequence([
        DerObjectId(hash_obj.oid),  # 哈希算法的 OID
        DerNull()  # NULL 参数
    ])
    
    # 构造完整的 DigestInfo
    digest_info = DerSequence([
        algorithm_id,
        DerOctetString(hash_obj.digest())
    ])
    
    return digest_info.encode()


def create_pkcs1v15_padding(digest_info, key_size_bytes):
    # 计算所需的填充长度
    padding_length = key_size_bytes - len(digest_info) - 3
    
    # 验证填充长度（PKCS#1 要求至少8字节填充）
    if padding_length < 8:
        raise ValueError(f"Key size ({key_size_bytes * 8} bits) too small for hash digest")
    
    # 构造标准的 PKCS#1 v1.5 填充格式
    return b'\x00\x01' + b'\xff' * padding_length + b'\x00' + digest_info

# 从 ca.cer 文件中读取证书 (PEM 格式)
with open('ca.cer', 'rb') as cert_file:
    cert = x509.load_pem_x509_certificate(cert_file.read())
    cert_der = cert.public_bytes(encoding=serialization.Encoding.DER)
    my_cert_content = base64.b64encode(cert_der).decode('utf-8')

# 从 license.json 文件中读取许可证数据
with open('license.json', 'r', encoding='utf-8') as f:
    license_config = json.load(f)

licenseId = license_config['licenseId']
licensePart = json.dumps(license_config)

with open('ca.key') as prifile:
    # 使用私钥对HASH值进行签名
    private_key = RSA.import_key(prifile.read())
    digest = SHA1.new(licensePart.encode('utf-8'))
    signature = pkcs1_15.new(private_key).sign(digest)

    sig_results = base64.b64encode(signature)
    licensePartBase64 = base64.b64encode(licensePart.encode('utf-8'))

    # 验签
    cert.public_key().verify(
        base64.b64decode(sig_results),
        base64.b64decode(licensePartBase64),
        padding=padding.PKCS1v15(),
        algorithm=hashes.SHA1(),
    )

    # 将激活码写入 key.txt 文件
    active_code = licenseId + "-" + licensePartBase64.decode('utf-8') + "-" + sig_results.decode('utf-8') + "-" + my_cert_content
    with open('key.txt', 'w', encoding='utf-8') as f:
        f.write(active_code)

    # 生成 power.conf 文件
    create_power_file(active_code)
