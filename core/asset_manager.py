import pygame
import os


class AssetManager:
    def __init__(self):
        """Initializes a new AssetManager"""
        self.empty()

    def load(self, file_path: str) -> None:
        """Loads the specified file from the specified file path. Use file name as key.

        Args:
            file_path (str): Path from current working directory to the specified file
        """
        file_name = os.path.basename(file_path)
        self._assets[file_name] = pygame.image.load(file_path)

    def load_folder(self, folder_path: str) -> None:
        """Load all the assets from the specified folder

        Args:
            folder_path (str): Path from current working directory to the specified folder
        """
        file_paths = os.listdir(folder_path)
        for file_path in file_paths:
            self.load(file_path)

    def _find_asset(self, asset_file_name: str) -> pygame.surface.Surface:
        """Find asset from asset name. If it doesn't exist then raise an exception.

        Args:
            asset_file_name (str): Asset file name with file extension

        Raises:
            ValueError: Could not find asset name

        Returns:
            pygame.surface.Surface: Asset surface object
        """
        for asset_name in self._assets.keys():
            if asset_name == asset_file_name:
                return self._assets[asset_file_name]
        raise KeyError(f"Could not find asset name: {asset_file_name}")

    def remove_asset(self, asset_file_name: str) -> None:
        """Remove asset using asset name. Raise exception if can not find asset.

        Args:
            asset_file_name (str): _description_

        Raises:
            ValueError: Can not remove asset
        """
        if not self.has(asset_file_name):
            raise ValueError("Can not remove asset")
        del self._assets[asset_file_name]

    def has(self, asset_file_name: str) -> bool:
        """Check if the asset exists in the asset list

        Args:
            asset_file_name (str): Asset file name with file extension

        Returns:
            bool: True if exists, False otherwise
        """
        return asset_file_name in self._assets.keys()

    def get_asset(self, asset_file_name: str) -> pygame.surface.Surface:
        return self._find_asset(asset_file_name)

    def empty(self):
        self._assets: dict[str, pygame.surface.Surface] = {}
