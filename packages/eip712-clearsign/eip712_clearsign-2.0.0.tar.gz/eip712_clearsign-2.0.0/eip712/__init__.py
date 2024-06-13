import hashlib
import json
from dataclasses import dataclass
from enum import Enum
from functools import cached_property
from typing import ClassVar, Iterator, List, Optional

from pydantic import BaseModel, Field, model_validator

# For more details on the serialisation spec, head over to
# https://github.com/LedgerHQ/app-ethereum/blob/develop/doc/ethapp.adoc#eip712-filtering


class EIP712Version(Enum):
    V1 = 1
    V2 = 2

    def __repr__(self):
        return "EIP712Version" + self.name


class EIP712Format(Enum):
    TOKEN = "token"
    AMOUNT = "amount"
    RAW = "raw"
    DATETIME = "datetime"


@dataclass
class EIP712BaseMapper:
    chain_id: int
    contract_address: str
    schema: dict
    display_name: str
    TYPE_PREFIX: ClassVar[int]

    def type_prefix_hash(self, version: EIP712Version) -> str:
        return self.TYPE_PREFIX.to_bytes(1, byteorder="big").hex()

    @cached_property
    def chain_id_hash(self) -> str:
        return self.chain_id.to_bytes(8, byteorder="big").hex()

    @cached_property
    def contract_address_hash(self) -> str:
        return self.contract_address[2:].lower()

    @cached_property
    def schema_hash(self) -> str:
        # Remove all spaces and new lines from the json schema
        schema_str = json.dumps(self.schema, separators=(",", ":"), indent=None)
        return hashlib.sha224(schema_str.encode("utf-8")).hexdigest()

    @cached_property
    def display_name_hash(self) -> str:
        return self.display_name.encode("utf-8").hex()

    def additional_hash(self, version: EIP712Version) -> str:
        return ""

    def identifier(self, version: EIP712Version = EIP712Version.V1) -> str:
        return (
            f"{self.type_prefix_hash(version)}"
            f"{self.chain_id_hash}"
            f"{self.contract_address_hash}"
            f"{self.schema_hash}"
            f"{self.additional_hash(version)}"
        )


@dataclass
class EIP712FieldMapper(EIP712BaseMapper):
    field_path: str
    format: ClassVar[EIP712Format]

    def type_prefix_hash(self, version: EIP712Version) -> str:
        match version:
            case EIP712Version.V1:
                return (72).to_bytes(1, byteorder="big").hex()
            case _:
                return self.TYPE_PREFIX.to_bytes(1, byteorder="big").hex()

    def additional_hash(self, version: EIP712Version) -> str:
        return f"{self.field_path.encode('utf-8').hex()}" f"{self.display_name_hash}"


@dataclass
class EIP712RawFieldMapper(EIP712FieldMapper):
    TYPE_PREFIX: ClassVar[int] = 72
    format: ClassVar[EIP712Format] = EIP712Format.RAW


@dataclass
class EIP712AmountJoinTokenFieldMapper(EIP712FieldMapper):
    TYPE_PREFIX: ClassVar[int] = 11
    format: ClassVar[EIP712Format] = EIP712Format.TOKEN

    coin_ref: int

    def additional_hash(self, version: EIP712Version) -> str:
        if version == EIP712Version.V1:
            return super().additional_hash(version)
        else:
            return (
                f"{self.field_path.encode('utf-8').hex()}"
                f"{self.coin_ref.to_bytes(1, byteorder='big').hex()}"
            )


@dataclass
class EIP712AmountJoinValueFieldMapper(EIP712FieldMapper):
    TYPE_PREFIX: ClassVar[int] = 22
    format: ClassVar[EIP712Format] = EIP712Format.AMOUNT

    coin_ref: int

    def additional_hash(self, version: EIP712Version) -> str:
        if version == EIP712Version.V1:
            return super().additional_hash(version)
        else:
            return (
                f"{self.field_path.encode('utf-8').hex()}"
                f"{self.display_name_hash}"
                f"{self.coin_ref.to_bytes(1, byteorder='big').hex()}"
            )


@dataclass
class EIP712DatetimeFieldMapper(EIP712FieldMapper):
    TYPE_PREFIX: ClassVar[int] = 33
    format: ClassVar[EIP712Format] = EIP712Format.DATETIME


@dataclass
class EIP712MessageNameMapper(EIP712BaseMapper):
    field_mappers_count: int
    TYPE_PREFIX: ClassVar[int] = 183

    def additional_hash(self, version: EIP712Version) -> str:
        return (
            f"{self.field_mappers_count.to_bytes(1, byteorder='big').hex()}"
            f"{self.display_name_hash}"
        )


class EIP712Field(BaseModel):
    path: str
    label: str
    assetPath: Optional[str] = None
    format: Optional[EIP712Format] = None
    coinRef: Optional[int] = None

    def mapper(self, **mapper_data) -> EIP712FieldMapper:
        match self.format:
            case EIP712Format.TOKEN:
                if self.coinRef is None:
                    raise ValueError(
                        f"EIP712 amount token field should have coin_ref: {self}"
                    )
                return EIP712AmountJoinTokenFieldMapper(
                    field_path=self.path,
                    display_name=self.label,
                    coin_ref=self.coinRef,
                    **mapper_data,
                )

            case EIP712Format.AMOUNT:
                if self.coinRef is None:
                    raise ValueError(
                        f"EIP712 amount value should have coin_ref: {self}"
                    )
                return EIP712AmountJoinValueFieldMapper(
                    field_path=self.path,
                    display_name=self.label,
                    coin_ref=self.coinRef,
                    **mapper_data,
                )

            case EIP712Format.DATETIME:
                return EIP712DatetimeFieldMapper(
                    field_path=self.path, display_name=self.label, **mapper_data
                )
            case _:
                return EIP712RawFieldMapper(
                    field_path=self.path, display_name=self.label, **mapper_data
                )


class EIP712Mapper(BaseModel):
    label: str
    fields: List[EIP712Field]

    def update_field_index(self):

        coin_refs = dict()
        idx: int = 0

        for field in self.fields:
            path: str | None = None
            if field.format == EIP712Format.TOKEN:
                path = field.path
            elif field.format == EIP712Format.AMOUNT:
                path = field.assetPath

            if path is not None:
                if path in coin_refs:
                    field.coinRef = coin_refs[path]
                else:
                    coin_refs[path] = idx
                    field.coinRef = idx
                    idx += 1

        return self

    @model_validator(mode="after")
    def _update_field_index(self):
        return self.update_field_index()

    def mappers(self, **mapper_data) -> Iterator[EIP712BaseMapper]:
        yield EIP712MessageNameMapper(
            field_mappers_count=len(self.fields),
            display_name=self.label,
            **mapper_data,
        )
        for field in self.fields:
            yield field.mapper(**mapper_data)


class EIP712MessageDescriptor(BaseModel):
    schema_: dict = Field(alias="schema")
    mapper: EIP712Mapper

    def mappers(self, **mapper_data) -> Iterator[EIP712BaseMapper]:
        return self.mapper.mappers(schema=self.schema_, **mapper_data)

    @classmethod
    def _schema_top_level_type(cls, schema: dict):
        """Given a schema, generate a new message descriptor"""
        filtered_schema: dict = {
            type_name: type_fields
            for type_name, type_fields in schema.items()
            if type_name != "EIP712Domain"
        }
        all_type_names = {
            type_field["type"]
            for type_fields in filtered_schema.values()
            for type_field in type_fields
        }
        return next(
            type_name
            for type_name in filtered_schema.keys()
            if type_name not in all_type_names
        )

    @classmethod
    def _type_names(cls, schema: dict, target_type_name: str) -> Iterator[List[str]]:
        """Recursively generate the list of fields to reach an object with a basic type"""
        for type_fields in schema[target_type_name]:
            name_list = [type_fields["name"]]
            short_type = type_fields["type"].removesuffix("[]")
            if short_type != type_fields["type"]:
                name_list.append("[]")
            if short_type in schema:
                for recursive_name_list in cls._type_names(
                    schema=schema, target_type_name=short_type
                ):
                    yield name_list + recursive_name_list
            else:
                yield name_list

    @classmethod
    def from_schema(cls, schema: dict):
        top_level_type_name = cls._schema_top_level_type(schema)

        mapper_fields = []

        for name_list in cls._type_names(
            schema=schema, target_type_name=top_level_type_name
        ):
            field_label = f"{top_level_type_name} {' '.join(name_list)}"
            field_path = f"{'.'.join(name_list)}"
            mapper_fields.append(EIP712Field(path=field_path, label=field_label))

        mapper = EIP712Mapper(label=top_level_type_name, fields=mapper_fields)
        mapper.update_field_index()
        clazz = cls(schema=schema, mapper=mapper)
        return clazz


class EIP712ContractDescriptor(BaseModel):
    address: str
    name: str = Field(alias="contractName")
    messages: List[EIP712MessageDescriptor]

    def mappers(self, **mapper_data) -> Iterator[EIP712BaseMapper]:
        for message in self.messages:
            for mapper in message.mappers(contract_address=self.address, **mapper_data):
                yield mapper

    def add_message(self, schema: dict):
        message = EIP712MessageDescriptor.from_schema(schema=schema)
        self.messages.append(message)


class EIP712DAppDescriptor(BaseModel):
    blockchain_name: str = Field(alias="blockchainName")
    chain_id: int = Field(alias="chainId")
    name: str
    contracts: List[EIP712ContractDescriptor]

    def mappers(self) -> Iterator[EIP712BaseMapper]:
        for contract in self.contracts:
            for mapper in contract.mappers(chain_id=self.chain_id):
                yield mapper

    def add_message(self, target_contract: EIP712ContractDescriptor, schema: dict):
        contract = next(
            (c for c in self.contracts if c.address == target_contract.address), None
        )
        if not contract:
            contract = target_contract
            self.contracts.append(contract)
        contract.add_message(schema=schema)
