





import sha3
from ecdsa import SigningKey, SECP256k1
import qrcode

keccak = sha3.keccak_256()
private = SigningKey.generate(curve=SECP256k1)
public = private.get_verifying_key().to_string()
keccak.update(public)
address = "0x{}".format(keccak.hexdigest()[24:])


print(private.to_string().hex())
print(address)
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)
qr.add_data(address)
qr.make(fit=True)

img = qr.make_image(fill_color="red", back_color="green")

img.save('y.png')