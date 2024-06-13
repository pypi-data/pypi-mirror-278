"""
Implement application-layer encryption using the aws-encryption-sdk.

"""
from collections.abc import Mapping, Sequence
from typing import Union

from aws_encryption_sdk import CommitmentPolicy, EncryptionSDKClient
from aws_encryption_sdk.materials_managers.base import CryptoMaterialsManager
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, hmac

from microcosm_postgres.encryption.constants import ENCRYPTION_V1_DEFAULT_KEY
from microcosm_postgres.encryption.v2.beacons import BeaconHashAlgorithm


class SingleTenantEncryptor:
    """
    A single tenant encryptor.

    """
    def __init__(
        self,
        encrypting_materials_manager: CryptoMaterialsManager | None,
        decrypting_materials_manager: CryptoMaterialsManager,
        beacon_key: str | None = None
    ):
        self.encrypting_materials_manager = encrypting_materials_manager
        self.decrypting_materials_manager = decrypting_materials_manager
        self.encryption_client = EncryptionSDKClient(
            commitment_policy=CommitmentPolicy.FORBID_ENCRYPT_ALLOW_DECRYPT,
        )
        self._beacon_key = beacon_key.encode("utf-8") if beacon_key else None

    def __contains__(self, encryption_context_key: str) -> bool:
        return True

    def encrypt(self,
                encryption_context_key: str,
                plaintext: str) -> tuple[bytes, Sequence[str]] | None:
        """
        Encrypt a plaintext string value.

        The return value will include *both* the resulting binary ciphertext and the
        master key ids used for encryption. In the likely case that the encryptor was initialized
        with master key aliases, these master key ids returned will represent the unaliased key.

        """
        if self.encrypting_materials_manager is None:
            return None

        encryption_context = dict(
            microcosm=encryption_context_key,
        )

        ciphertext, header = self.encryption_client.encrypt(
            source=plaintext,
            materials_manager=self.encrypting_materials_manager,
            encryption_context=encryption_context,
        )

        key_ids = [
            self.unpack_key_id(encrypted_data_key.key_provider)
            for encrypted_data_key in header.encrypted_data_keys
        ]
        return ciphertext, key_ids

    def decrypt(self, encryption_context_key: str, ciphertext: bytes) -> str:

        plaintext, header = self.encryption_client.decrypt(
            source=ciphertext,
            materials_manager=self.decrypting_materials_manager,
        )
        return plaintext.decode("utf-8")

    def beacon(self, value: str, algorithm: BeaconHashAlgorithm | None = None) -> str | None:
        if algorithm in [BeaconHashAlgorithm.SHA_256, None]:
            # Note that this is the default behaviour
            # Create a SHA-256 hash object
            digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
            digest.update(value.encode("utf-8"))
            return digest.finalize().hex()

        elif algorithm == BeaconHashAlgorithm.HMAC_SHA_256:
            if self._beacon_key is None:
                return None

            h = hmac.HMAC(self._beacon_key, hashes.SHA256())
            h.update(value.encode("utf-8"))
            return h.finalize().hex()

        else:
            return None

    def unpack_key_id(self, key_provider):
        key_info = key_provider.key_info
        try:
            # KMS case: the wrapped key id *is* the key id
            return key_info.decode("utf-8")
        except UnicodeDecodeError:
            # static case: the wrapped key id is the key id followed by two four byte integers (tags)
            # followed by a twelve byte initialization vectors (IV)
            #
            # see: aws_encryption_sdk.internal.formatting.serialize:serialize_wrapped_key
            return key_info[:-(4 + 4 + 12)].decode("utf-8")


class MultiTenantEncryptor:

    def __init__(self,
                 encryptors: Mapping[str, SingleTenantEncryptor],
                 default_key=ENCRYPTION_V1_DEFAULT_KEY):
        self.encryptors = encryptors
        self.default_key = default_key

    def __contains__(self, encryption_context_key: str) -> bool:
        return encryption_context_key in self.encryptors or self.default_key in self.encryptors

    def __getitem__(self, encryption_context_key: str) -> SingleTenantEncryptor | None:
        try:
            return self.encryptors[encryption_context_key]
        except KeyError:
            try:
                return self.encryptors[self.default_key]
            except KeyError:
                return None

    def encrypt(self, encryption_context_key: str, plaintext: str) -> tuple[bytes, Sequence[str]] | None:
        encryptor = self[encryption_context_key]
        if encryptor is None:
            return None
        return encryptor.encrypt(encryption_context_key, plaintext)

    def decrypt(self, encryption_context_key: str, ciphertext: bytes) -> str | None:
        encryptor = self[encryption_context_key]
        if encryptor is None:
            return None
        return encryptor.decrypt(encryption_context_key, ciphertext)

    def beacon(
        self,
        encryption_context_key: str,
        value: str,
        algorithm: BeaconHashAlgorithm | None = None
    ) -> str | None:
        encryptor = self[encryption_context_key]
        if encryptor is None:
            return None
        return encryptor.beacon(value, algorithm=algorithm)


Encryptor = Union[
    SingleTenantEncryptor,
    MultiTenantEncryptor,
]
