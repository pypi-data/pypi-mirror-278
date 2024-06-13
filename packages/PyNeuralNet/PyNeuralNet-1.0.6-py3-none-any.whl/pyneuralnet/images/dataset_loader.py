import os
from PIL import Image
from torch.utils.data import Dataset


class DatasetLoader(Dataset):
    def __init__(self, metadata_file, root_dir, transform=None):
        with open(metadata_file, 'r') as file:
            self.image_paths = file.readlines()
        self.image_paths = [os.path.join(root_dir, path.strip()) for path in self.image_paths]
        self.transform = transform
        print(f"Loaded {len(self.image_paths)} images")
        print(f"Example path: {self.image_paths[0]}")

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx):
        img_path = self.image_paths[idx]
        if not os.path.exists(img_path):
            raise FileNotFoundError(f"File not found: {img_path}")
        img = Image.open(img_path).convert('RGB')
        if self.transform:
            img = self.transform(img)
        return img
