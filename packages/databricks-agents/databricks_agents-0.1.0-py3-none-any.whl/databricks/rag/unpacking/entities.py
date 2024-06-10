from abc import ABC
from dataclasses import dataclass
from itertools import chain


@dataclass(init=False, repr=False, frozen=True)
class UnityCatalogEntity(ABC):
    """Abstraction for Unity Catalog Entity, such as Table, Volume, Model, Vector Search Index"""

    catalog_name: str
    schema_name: str

    _entity_name: str
    """
    Name of the entity.
    Given the fully-qualified name "a.b.c" then this method should return "c".
    For each UC entity type, it has different meaning, such as table_name, volume_name, model_name, index_name etc.
    """

    def __init__(self, catalog_name: str, schema_name: str, entity_name: str):
        super().__init__()
        # We set frozen=True in the dataclass decorator, so we need to use object.__setattr__ to set the attributes
        object.__setattr__(
            self,
            "catalog_name",
            UnityCatalogEntity._unsanitize_identifier(catalog_name),
        )
        object.__setattr__(
            self, "schema_name", UnityCatalogEntity._unsanitize_identifier(schema_name)
        )
        object.__setattr__(
            self, "_entity_name", UnityCatalogEntity._unsanitize_identifier(entity_name)
        )

    @classmethod
    def from_full_name(cls, full_name: str):
        identifiers = full_name.split(".")
        if len(identifiers) != 3:
            raise ValueError(
                f"Qualified UC entity full name {full_name} should be in the format 'catalog.schema.entity'"
            )
        catalog_name, schema_name, entity_name = identifiers
        return cls(catalog_name, schema_name, entity_name)

    def _get_sanitized_catalog_name(self) -> str:
        """Get the sanitized catalog name."""
        return UnityCatalogEntity._sanitize_identifier(self.catalog_name)

    def _get_sanitized_schema_name(self) -> str:
        """Get the sanitized schema name."""
        return UnityCatalogEntity._sanitize_identifier(self.schema_name)

    def _get_sanitized_entity_name(self) -> str:
        """Get the sanitized entity name."""
        return UnityCatalogEntity._sanitize_identifier(self._entity_name)

    def full_name(
            self, *, use_backtick_delimiters: bool = True, escape: bool = True
    ) -> str:
        """
        Get the full name of a UC entity, optionally using backticks to delimit the identifiers.

        :param use_backtick_delimiters: Whether to use backticks to delimit the identifiers.
        :param escape: (deprecated, use `use_backtick_delimiters`) Whether to use backticks to delimit the identifiers.
        """
        if not escape or not use_backtick_delimiters:
            return f"{self.catalog_name}.{self.schema_name}.{self._entity_name}"
        return f"{self._get_sanitized_catalog_name()}.{self._get_sanitized_schema_name()}.{self._get_sanitized_entity_name()}"

    @staticmethod
    def _sanitize_identifier(identifier: str) -> str:
        """
        Escape special characters and delimit an identifier with backticks.
        For example, "a`b" becomes "`a``b`".
        Use this function to sanitize identifiers such as table/column names in SQL and PySpark.
        """
        return f"`{identifier.replace('`', '``')}`"

    @staticmethod
    def _unsanitize_identifier(identifier: str) -> str:
        """
        Unsanitize an identifier. Useful when we get a possibly sanitized identifier from Spark or
        somewhere else, but we need an unsanitized one.
        Note: This function does not check the correctness of the identifier passed in. e.g. `foo``
        is not a valid sanitized identifier. When given such invalid input, this function returns
        invalid output.
        """
        if len(identifier) >= 2 and identifier[0] == "`" and identifier[-1] == "`":
            return identifier[1:-1].replace("``", "`")
        else:
            return identifier

    def _public_fields(self):
        """
        Get a list of public fields. Public field's name does not start with "_".
        """
        return [a for a in self.__dict__.keys() if not a.startswith("_")]

    @classmethod
    def _properties(cls):
        """
        Get a list of properties.
        """
        return sorted(
            [p for p in cls.__dict__ if isinstance(getattr(cls, p), property)]
        )

    def __repr__(self):
        """
        Get the representation of the object.
        Show only public fields and properties.
        The representation is in the format of `ClassName(field1=value1, field2=value2, ...)`.
        """
        kws = [
            f"{key}={self.__getattribute__(key)!r}"
            for key in chain(self._public_fields(), self._properties())
        ]
        return f"{type(self).__name__}({', '.join(kws)})"


@dataclass(init=False, repr=False, frozen=True)
class UnityCatalogTable(UnityCatalogEntity):
    """Abstraction for Unity Catalog Table"""

    def __init__(self, catalog_name: str, schema_name: str, table_name: str):
        super().__init__(catalog_name, schema_name, table_name)

    @property
    def table_name(self) -> str:
        return self._entity_name

    def get_table_url_in_workspace(self, workspace_url: str) -> str:
        """
        Get the URL for the table in the provided workspace.

        :param workspace_url: URL of the workspace to link to
        :return: URL of the table in the Catalog Explorer
        """
        return f"{workspace_url}/explore/data/{self.catalog_name}/{self.schema_name}/{self.table_name}"
