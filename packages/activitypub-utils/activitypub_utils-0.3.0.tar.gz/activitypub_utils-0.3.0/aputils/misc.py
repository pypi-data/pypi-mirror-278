from __future__ import annotations

import base64
import json
import typing

from Crypto.Hash import SHA256, SHA512
from blib import HttpDate
from typing import Any

from .enums import AlgorithmType

if typing.TYPE_CHECKING:
	from collections.abc import Sequence
	from datetime import datetime

	try:
		from typing import Self

	except ImportError:
		from typing_extensions import Self


HASHES = {
	"sha256": SHA256,
	"sha512": SHA512
}


class Digest:
	"Represents a body digest"

	__slots__ = {"digest", "algorithm"}

	def __init__(self, digest: str, algorithm: str) -> None:
		"""
			Create a new digest object from an already existing digest

			:param digest: Base64 encoded hash
			:param algorithm: Algorithm used for hash in the format of ``{type}-{bytes}``
		"""

		self.digest = digest
		self.algorithm = algorithm


	def __repr__(self) -> str:
		return f"Digest({self.digest}, {self.algorithm})"


	def __str__(self) -> str:
		return self.compile()


	def __eq__(self, value: object) -> bool:
		if isinstance(value, Digest):
			return self.algorithm == value.algorithm and self.digest == value.digest

		if isinstance(value, (dict, str, bytes)):
			return self.validate(value)

		raise TypeError(f"Cannot compare '{type(value).__name__}' to 'Digest'")


	@classmethod
	def new(cls: type[Self],
			body: dict[str, Any] | str | bytes,
			size: int = 256) -> Self:
		"""
			Generate a new body digest

			:param body: Message body to hash
			:param size: SHA hash size
		"""

		if isinstance(body, dict):
			body = json.dumps(body).encode("utf-8")

		elif isinstance(body, str):
			body = body.encode("utf-8")

		if size >= 1024:
			size = int(size / 8)

		raw_hash = HASHES[f"sha{size}"].new(data=body)
		digest = base64.b64encode(raw_hash.digest()).decode("utf-8")

		return cls(digest, f"SHA-{size}")


	@classmethod
	def parse(cls: type[Self], digest: str | None) -> Self | None:
		"""
			Create a new digest from a digest header

			:param digest: Digest header
		"""

		if not digest:
			return None

		alg, digest = digest.split("=", 1)
		return cls(digest, alg)


	@property
	def hashalg(self) -> str:
		"Hash function used when creating the signature as a string"

		return self.algorithm.replace("-", "").lower()


	def compile(self) -> str:
		"Turn the digest object into a ``str`` for the Digest header"

		return "=".join([self.algorithm, self.digest])


	def validate(self, body: dict[str, Any] | str | bytes, hash_size: int = 256) -> bool:
		"""
			Check if the body digest matches the body

			:param body: Message body to verify
			:param hash_size: Size of the hashing algorithm
		"""

		return self == Digest.new(body, hash_size)


class MessageDate(HttpDate):
	"""
		Datetime object with convenience methods for parsing and creating ActivityPub message date
		strings
	"""

	FORMAT: str = "%Y-%m-%dT%H:%M:%SZ"
	"Format to pass to datetime when (de)serializing a raw message date"


class Signature:
	"""
		Represents a signature header value
	"""

	__slots__ = {"keyid", "algorithm", "headers", "signature", "created", "expires"}

	def __init__(self,
				signature: str,
				keyid: str,
				algorithm: AlgorithmType | str,
				headers: Sequence[str] | str,
				created: HttpDate | datetime | str | int | float | None = None,
				expires: HttpDate | datetime | str | int | float | None = None) -> None:
		"""
			Create a new signature object. This should not be initiated directly.

			:param signature: Generated signature hash
			:param keyid: URL of the public key
			:param algorithm: Hashing and signing algorithms used to create the signature
			:param headers: Header keys used to create the signature
			:param created: Unix timestamp representing the signature creation date
			:param expires: Unix timestamp representing the date the signature expires
		"""

		self.signature: str = signature
		"Generated signature hash"

		self.keyid: str = keyid
		"URL of the public key"

		self.algorithm: AlgorithmType = algorithm # type: ignore[assignment]
		"Hashing and signing algorithms used to create the signature"

		self.headers: Sequence[str] = headers
		"Header keys used to create the signature"

		self.created: HttpDate | None = created # type: ignore[assignment]
		"Signature creation date"

		self.expires: HttpDate | None = expires # type: ignore[assignment]
		"Signature expiration date"


	def __setattr__(self, key: str, value: Any) -> None:
		if key == "headers" and isinstance(value, str):
			value = value.split()

		elif key == "algorithm":
			value = AlgorithmType.parse(value)

		elif key in {"created", "expires"} and value is not None:
			if isinstance(value, str):
				try:
					value = int(value)

				except ValueError:
					pass

			value = HttpDate.parse(value)

		object.__setattr__(self, key, value)


	def __repr__(self) -> str:
		data = {
			"keyid": repr(self.keyid),
			"algorithm": self.algorithm,
			"headers": self.headers,
			"created": self.created.timestamp() if self.created is not None else None,
			"expires": self.expires.timestamp() if self.expires is not None else None
		}

		str_data = ", ".join(f"{key}={value}" for key, value in data.items())
		return f"Signature({str_data})"


	@classmethod
	def new_from_headers(cls: type[Self], headers: dict[str, str]) -> Self:
		"""
			Parse the signature from a header dict

			:param dict[str,str] headers: Header key/value pairs
			:raises KeyError: When the signature header(s) cannot be found
			:raises NotImplementedError: When a newer unsupported signature standard is provided
		"""

		headers = {key.lower(): value for key, value in headers.items()}

		if "signature-input" in headers:
			raise NotImplementedError("Newer signature spec not supported yet")

		signature = headers["signature"]
		data: dict[str, str] = {}

		for chunk in signature.strip().split(","):
			key, value = chunk.split("=", 1)
			data[key.lower()] = value.strip("\"")

		return cls(**data)


	@classmethod
	def parse(cls: type[Self], data: str) -> Self:
		"""
			Parse a Signature in string format

			:param str data: Signature string
		"""

		return cls.new_from_headers({"signature": data})


	@property
	def algs(self) -> tuple[str, str]:
		"Return the algorithms used for signing [0] and hashing [1]"
		return self.algorithm.value.split("-", 1) # type: ignore


	@property
	def hashalg(self) -> str:
		"Algorithm used for hashing"
		return self.algs[1]


	@property
	def signalg(self) -> str:
		"Algorithm used for signing"
		return self.algs[0]


	def compile(self) -> str:
		"Generate a string for a Signature header"

		data = {
			"keyId": self.keyid,
			"algorithm": self.algorithm.value,
			"headers": " ".join(self.headers),
			"created": self.created.timestamp() if self.created is not None else None,
			"expires": self.expires.timestamp() if self.expires is not None else None,
			"signature": self.signature
		}

		return ",".join([f"{k}=\"{v}\"" for k, v in data.items() if v is not None])
