from abc import ABC, abstractmethod
from Crypto.PublicKey import RSA
from typing import Union


class SignatureAlgorithm(ABC):
    @abstractmethod
    def verify(
        self, public_key: RSA.RsaKey, msg: Union[str, bytes], signature: str
    ) -> bool:
        """Verifies a signature"""
        pass

    @abstractmethod
    def sign(self, private_key: RSA.RsaKey, msg: Union[str, bytes]) -> str:
        """Signs a message"""
        pass
