"""Registry factory module for a codebase."""

from typing import Any, Dict, List, Optional, Tuple

from registry_factory.index import HashTable, RegistryTable
from registry_factory.patterns.facade import ObserverFacade
from registry_factory.patterns.mediator import HashMediator
from registry_factory.patterns.observer import RegistryObserver
from registry_factory.registry import AbstractRegistry


class Factory:
    """A factory class for creating registries."""

    _hash_map: RegistryTable
    _shared_hash: int
    _shared_hash_table: HashTable
    _registries: List[AbstractRegistry]

    def __init__(self):
        raise ValueError("Factory is not meant to be instantiated.")

    @classmethod
    def hash_map(cls) -> RegistryTable:
        """Return the hash map."""
        if not hasattr(cls, "_hash_map"):
            cls.init_hash_map()
        return cls._hash_map

    @classmethod
    def shared_hash(cls) -> int:
        """Return the shared hash."""
        if not hasattr(cls, "_shared_hash"):
            cls.init_hash_map()
        return cls._shared_hash

    @classmethod
    def shared_hash_table(cls) -> HashTable:
        """Return the shared hash table."""
        if not hasattr(cls, "_shared_hash_table"):
            cls._shared_hash_table = HashTable()
        return cls._shared_hash_table

    @classmethod
    def init_hash_map(cls, bitsize=256, max_generation=1000) -> None:
        """Initialize the hash map."""
        cls._hash_map = RegistryTable(bitsize, max_generation)
        cls._shared_hash = cls._hash_map.generate_hash()

    @classmethod
    def create_registry(
        cls,
        name: str,
        shared: bool = False,
        skip_validation: bool = False,
        checks: Optional[List[RegistryObserver]] = None,
    ) -> AbstractRegistry:
        registry_hash = cls.shared_hash() if shared else cls.hash_map().generate_hash()

        class Registry(AbstractRegistry):
            mediator = HashMediator(registry_hash, ObserverFacade(skip_validation, observers=checks))

            _name = name
            _registry_hash = registry_hash

        if not shared:
            cls.hash_map().set(registry_hash)
        else:
            Registry.mediator.hash_table = cls.shared_hash_table()

        if not hasattr(cls, "_registries"):
            cls._registries = []
        cls._registries.append(Registry)

        return Registry  # type: ignore

    @classmethod
    def view_called(cls) -> None:
        """View the accreditation information."""
        print("Called objects:")
        # Tracker().show()

    @classmethod
    def get_registries(cls) -> Dict[str, AbstractRegistry]:
        """Return the choices for the subclass."""
        return {reg._name: reg for reg in cls._registries} if hasattr(cls, "_registries") else {}

    @classmethod
    def items(cls) -> List[Tuple[str, Any]]:
        """Return the items for the subclass."""
        return [(name, reg) for name, reg in cls.get_registries().items()]

    @classmethod
    def keys(cls) -> List[str]:
        """Return the keys for the subclass."""
        return [name for name, reg in cls.get_registries().items()]

    @classmethod
    def values(cls) -> List[Any]:
        """Return the values for the subclass."""
        return [reg for name, reg in cls.get_registries().items()]

    @classmethod
    def get_options(cls, registries_names: Optional[List[str]] = None) -> List[str]:
        """Get the options for the registry."""
        registries = (
            cls.get_registries()
            if registries_names is None
            else {name: cls.get_registries()[name] for name in registries_names}
        )

        options = {}
        for name, registry in registries.items():
            options[name] = [k for k in registry.keys()]

        options_listed: List[str] = list(*options.values())
        return options_listed

    @classmethod
    def get_registry_arguments(cls, registries_names: Optional[List[str]] = None) -> Dict[str, Any]:
        """Return the arguments for the subclass."""
        cls_registries = cls.get_registries()
        arguments = {}
        if registries_names is None:
            registries_names = list(cls_registries.keys())
        for name in registries_names:
            options = cls.get_options([name])
            for option in options:
                arguments[name] = cls_registries[name].get_arguments(option)
        return arguments

    @classmethod
    def get_arguments(cls, registry: str, key: str, key_dict: Optional[Dict] = None, **kwargs) -> Any:
        cls_registries = cls.get_registries()
        return cls_registries[registry].get_arguments(key, key_dict, **kwargs)
